"""
High-level API for programmatic use of normattiva2md.

Provides two interfaces:
1. Standalone functions for quick usage: convert_url(), convert_xml(), search_law()
2. Converter class for advanced usage with persistent configuration

Examples:
    >>> from normattiva2md import convert_url
    >>> result = convert_url("https://www.normattiva.it/uri-res/N2Ls?urn:...")
    >>> print(result.markdown[:100])

    >>> from normattiva2md import Converter
    >>> conv = Converter(quiet=True)
    >>> result = conv.search_and_convert("legge stanca")
    >>> result.save("legge.md")
"""

from __future__ import annotations

import logging
import os
import tempfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from .constants import AKN_NAMESPACE
from .exceptions import (
    APIKeyError,
    ConversionError,
    InvalidURLError,
    XMLFileNotFoundError,
)
from .markdown_converter import generate_markdown_text
from .models import ConversionResult, SearchResult
from .normattiva_api import (
    download_akoma_ntoso,
    download_akoma_ntoso_via_export,
    download_akoma_ntoso_via_opendata,
    extract_params_from_normattiva_url,
    is_normattiva_url,
    normalize_normattiva_url,
    validate_normattiva_url,
)
from .utils import load_env_file
from .xml_parser import (
    construct_article_eid,
    extract_metadata_from_xml,
    filter_xml_to_article,
)

logger = logging.getLogger(__name__)


def convert_url(
    url: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    force_opendata: bool = False,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    """
    Converte documento da URL normattiva.it a Markdown.

    Args:
        url: URL normattiva.it del documento
        article: Articolo specifico da estrarre (es: "4", "16bis")
        with_urls: Genera link markdown per riferimenti normativi
        quiet: Disabilita logging info

    Returns:
        ConversionResult con markdown e metadata, oppure None se conversione fallisce

    Raises:
        InvalidURLError: URL non valido o dominio non permesso
        ConversionError: Errore grave durante conversione

    Examples:
        >>> result = convert_url("https://www.normattiva.it/uri-res/N2Ls?urn:...")
        >>> print(result.markdown[:100])
        >>> print(result.metadata['dataGU'])

        >>> # Con articolo specifico
        >>> result = convert_url("https://...", article="16bis")

        >>> # Con link inline
        >>> result = convert_url("https://...", with_urls=True)

        >>> # Forza download via OpenData
        >>> result = convert_url("https://...", force_opendata=True)
    """
    # Load .env file for API keys
    load_env_file()

    normalized_url = normalize_normattiva_url(url)

    # Validate URL
    try:
        validate_normattiva_url(normalized_url)
    except ValueError as e:
        raise InvalidURLError(
            f"URL non valido: {e}. L'URL deve essere HTTPS e dominio normattiva.it"
        )

    if not quiet:
        logger.info(f"Conversione URL: {normalized_url}")

    # Extract parameters from URL
    params = None
    session = None
    if not force_opendata:
        params, session = extract_params_from_normattiva_url(
            normalized_url, quiet=quiet
        )

    # Download XML to temp file
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
        xml_path = tmp.name

    try:
        if params and not force_opendata:
            success = download_akoma_ntoso(params, xml_path, session, quiet=quiet)
            if not success:
                logger.warning(f"Download fallito per {url}")
                return None

            # Build metadata
            metadata = {
                "dataGU": params["dataGU"],
                "codiceRedaz": params["codiceRedaz"],
                "dataVigenza": params["dataVigenza"],
                "url": normalized_url,
                "url_xml": (
                    "https://www.normattiva.it/do/atto/caricaAKN"
                    f"?dataGU={params['dataGU']}"
                    f"&codiceRedaz={params['codiceRedaz']}"
                    f"&dataVigenza={params['dataVigenza']}"
                ),
            }
        else:
            success, metadata, session = download_akoma_ntoso_via_opendata(
                normalized_url, xml_path, session=session, quiet=quiet
            )
            if not success:
                success, metadata, session = download_akoma_ntoso_via_export(
                    normalized_url, xml_path, session=session, quiet=quiet
                )
            if not success:
                logger.warning(f"Download fallito per {url}")
                return None

        # Add article to metadata if specified
        if article:
            metadata["article"] = article

        # Convert using internal function
        result = _convert_xml_internal(
            xml_path,
            article=article,
            with_urls=with_urls,
            metadata=metadata,
            quiet=quiet,
        )

        if result:
            result.url = normalized_url
            result.url_xml = metadata["url_xml"]

        return result

    finally:
        # Cleanup temp file
        try:
            os.unlink(xml_path)
        except OSError:
            pass


def convert_xml(
    xml_path: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    metadata: Optional[Dict] = None,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    """
    Converte file XML locale a Markdown.

    Args:
        xml_path: Path al file XML Akoma Ntoso
        article: Articolo specifico da estrarre
        with_urls: Genera link markdown per riferimenti
        metadata: Metadata opzionali da includere nel front matter
        quiet: Disabilita logging info

    Returns:
        ConversionResult con markdown e metadata, oppure None se conversione fallisce

    Raises:
        XMLFileNotFoundError: File XML non esiste
        ConversionError: Errore parsing XML

    Examples:
        >>> result = convert_xml("path/to/file.xml")
        >>> result.save("output.md")

        >>> # Con metadata custom
        >>> result = convert_xml(
        ...     "file.xml",
        ...     metadata={'source': 'custom', 'dataGU': '20220101'}
        ... )
    """
    # Check file exists
    if not os.path.exists(xml_path):
        raise XMLFileNotFoundError(
            f"File XML non trovato: '{xml_path}'. Verifica che il path sia corretto."
        )

    if not quiet:
        logger.info(f"Conversione file: {xml_path}")

    return _convert_xml_internal(
        xml_path,
        article=article,
        with_urls=with_urls,
        metadata=metadata,
        quiet=quiet,
    )


def _convert_xml_internal(
    xml_path: str,
    article: Optional[str] = None,
    with_urls: bool = False,
    metadata: Optional[Dict] = None,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    """
    Internal conversion function used by both convert_url and convert_xml.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Build cross references if with_urls
        cross_references = None
        if with_urls:
            from .akoma_utils import akoma_uri_to_normattiva_url

            cross_references = {}
            for ref in root.iter():
                if ref.tag.endswith("ref") and ref.get("href"):
                    href = ref.get("href")
                    if href and href.startswith("/akn/"):
                        normattiva_url = akoma_uri_to_normattiva_url(href)
                        if normattiva_url:
                            cross_references[normattiva_url] = normattiva_url
                    elif href and is_normattiva_url(href):
                        cross_references[href] = href

        # Filter to specific article if requested
        article_eid = None
        if article:
            article_eid = construct_article_eid(article)
            if article_eid:
                filtered_root = filter_xml_to_article(root, article_eid, AKN_NAMESPACE)
                if filtered_root is None:
                    logger.warning(f"Articolo '{article}' non trovato nel documento")
                    return None
                root = filtered_root

        # Extract metadata from XML if not provided
        if metadata is None:
            metadata = extract_metadata_from_xml(root)
        else:
            # Merge XML metadata with provided metadata
            xml_metadata = extract_metadata_from_xml(root)
            merged = {**xml_metadata, **metadata}
            metadata = merged

        # Generate markdown
        markdown = generate_markdown_text(
            root,
            ns=AKN_NAMESPACE,
            metadata=metadata,
            cross_references=cross_references,
        )

        if not quiet:
            logger.info("Conversione completata")

        return ConversionResult(
            markdown=markdown,
            metadata=metadata,
            url=metadata.get("url"),
            url_xml=metadata.get("url_xml"),
        )

    except ET.ParseError as e:
        raise ConversionError(
            f"Errore parsing XML: {e}. "
            f"Il file potrebbe essere corrotto o non essere un documento Akoma Ntoso valido."
        )
    except Exception as e:
        raise ConversionError(f"Errore durante conversione: {e}")


def search_law(
    query: str,
    exa_api_key: Optional[str] = None,
    limit: int = 5,
    quiet: bool = False,
) -> List[SearchResult]:
    """
    Cerca documenti legali usando Exa AI.

    Args:
        query: Query di ricerca in linguaggio naturale
        exa_api_key: Exa API key (default: usa EXA_API_KEY da ENV)
        limit: Numero massimo risultati
        quiet: Disabilita logging info

    Returns:
        Lista di SearchResult ordinata per relevance, lista vuota se nessun risultato

    Raises:
        APIKeyError: API key non configurata o invalida

    Examples:
        >>> results = search_law("legge stanca accessibilità")
        >>> if results:
        ...     best = results[0]
        ...     print(f"{best.title}: {best.url}")

        >>> # Con API key custom
        >>> results = search_law("decreto dignità", exa_api_key="custom-key")

        >>> # Loop su risultati
        >>> for r in results:
        ...     print(f"{r.score:.2f} - {r.title}")
    """
    import json
    import re

    import requests

    from .normattiva_api import is_normattiva_export_url

    # Load .env file
    load_env_file()

    # Get API key
    api_key = exa_api_key or os.getenv("EXA_API_KEY")
    if not api_key:
        raise APIKeyError(
            "Exa API key non configurata. "
            "Configura con: export EXA_API_KEY='your-key' "
            "oppure passa exa_api_key='your-key' come parametro. "
            "Registrati su: https://exa.ai"
        )

    if not quiet:
        logger.info(f"Ricerca: {query}")

    # Prepare Exa API request
    url = "https://api.exa.ai/search"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "query": query,
        "includeDomains": ["normattiva.it"],
        "numResults": limit,
        "type": "auto",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 401 or response.status_code == 403:
            raise APIKeyError(
                f"Exa API key invalida o scaduta (HTTP {response.status_code}). "
                "Verifica la tua API key su https://exa.ai"
            )

        if response.status_code != 200:
            logger.warning(
                f"Errore Exa API (HTTP {response.status_code}): {response.text}"
            )
            return []

        data = response.json()
        raw_results = data.get("results", [])

        if not raw_results:
            if not quiet:
                logger.info(f"Nessun risultato per: {query}")
            return []

        # Filter and score results
        results = []
        query_lower = query.lower()

        # Check if user wants specific article
        article_match = re.search(
            r"\b(?:articolo|art\.?|art)\s+(\d+(?:\s*(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies))?)\b",
            query_lower,
            re.IGNORECASE,
        )
        requested_article = (
            article_match.group(1).replace(" ", "") if article_match else None
        )

        for result in raw_results:
            result_url = result.get("url")
            if not result_url or not is_normattiva_url(result_url):
                continue
            if is_normattiva_export_url(result_url):
                continue

            title = result.get("title", "")

            # Skip error pages
            if "errore" in title.lower():
                continue

            score = result.get("score", 0.0)

            # Adjust URL for full law if no article requested
            if not requested_article and "~art" in result_url:
                result_url = result_url.split("~art")[0]

            results.append(
                SearchResult(
                    url=result_url,
                    title=title,
                    score=score,
                )
            )

        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)

        if not quiet:
            logger.info(f"Trovati {len(results)} risultati")

        return results

    except requests.exceptions.Timeout:
        logger.warning("Timeout nella chiamata a Exa API")
        return []
    except requests.exceptions.RequestException as e:
        logger.warning(f"Errore di connessione a Exa API: {e}")
        return []
    except json.JSONDecodeError:
        logger.warning("Errore nel parsing della risposta Exa API")
        return []


class Converter:
    """
    Converter con configurazione persistente.

    Utile per batch processing o uso ripetuto con stessa configurazione.

    Attributes:
        exa_api_key: Exa API key configurata
        quiet: Flag quiet mode
        keep_xml: Flag per mantenere XML scaricati

    Examples:
        >>> conv = Converter(exa_api_key="...", quiet=True)
        >>> result1 = conv.convert_url("https://...")
        >>> result2 = conv.convert_url("https://...")
        >>> results = conv.search("legge stanca")
    """

    def __init__(
        self,
        exa_api_key: Optional[str] = None,
        quiet: bool = False,
        keep_xml: bool = False,
    ):
        """
        Inizializza converter con configurazione.

        Args:
            exa_api_key: Exa API key (default: usa EXA_API_KEY da ENV)
            quiet: Disabilita tutti i log info
            keep_xml: Mantiene file XML scaricati temporanei
        """
        load_env_file()
        self.exa_api_key = exa_api_key or os.getenv("EXA_API_KEY")
        self.quiet = quiet
        self.keep_xml = keep_xml

    def convert_url(
        self,
        url: str,
        article: Optional[str] = None,
        with_urls: bool = False,
    ) -> Optional[ConversionResult]:
        """
        Converte da URL usando configurazione dell'istanza.

        Stesso comportamento di convert_url() standalone ma usa:
        - self.quiet per logging

        Args:
            url: URL normattiva.it del documento
            article: Articolo specifico da estrarre
            with_urls: Genera link markdown per riferimenti

        Returns:
            ConversionResult o None
        """
        return convert_url(
            url,
            article=article,
            with_urls=with_urls,
            quiet=self.quiet,
        )

    def convert_xml(
        self,
        xml_path: str,
        article: Optional[str] = None,
        with_urls: bool = False,
        metadata: Optional[Dict] = None,
    ) -> Optional[ConversionResult]:
        """
        Converte da XML usando configurazione dell'istanza.

        Args:
            xml_path: Path al file XML
            article: Articolo specifico da estrarre
            with_urls: Genera link markdown per riferimenti
            metadata: Metadata opzionali

        Returns:
            ConversionResult o None
        """
        return convert_xml(
            xml_path,
            article=article,
            with_urls=with_urls,
            metadata=metadata,
            quiet=self.quiet,
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        Ricerca documenti usando configurazione dell'istanza.

        Uses:
        - self.exa_api_key se configurata
        - self.quiet per logging

        Args:
            query: Query di ricerca
            limit: Numero massimo risultati

        Returns:
            Lista di SearchResult
        """
        return search_law(
            query,
            exa_api_key=self.exa_api_key,
            limit=limit,
            quiet=self.quiet,
        )

    def search_and_convert(
        self,
        query: str,
        article: Optional[str] = None,
        with_urls: bool = False,
        use_best: bool = True,
    ) -> Optional[ConversionResult]:
        """
        Cerca e converte il miglior risultato in un passo.

        Args:
            query: Query di ricerca
            article: Articolo specifico da estrarre
            with_urls: Genera link markdown
            use_best: Se True usa miglior risultato automaticamente

        Returns:
            ConversionResult del miglior match, oppure None se ricerca fallisce

        Raises:
            APIKeyError: API key non configurata

        Examples:
            >>> conv = Converter(exa_api_key="...")
            >>> result = conv.search_and_convert("legge stanca")
            >>> result.save("legge_stanca.md")
        """
        results = self.search(query)
        if not results:
            return None

        if use_best:
            url = results[0].url
        else:
            # For now, use best result (interactive selection could be added later)
            url = results[0].url

        return self.convert_url(url, article=article, with_urls=with_urls)
