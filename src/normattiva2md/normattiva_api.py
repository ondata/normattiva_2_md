import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

import requests

from .constants import (
    ALLOWED_DOMAINS,
    DEFAULT_TIMEOUT,
    VERSION,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
)


def normalize_normattiva_url(url):
    """
    Normalizza URL normattiva.it rimuovendo escape backslash.

    Args:
        url: URL string

    Returns:
        str: URL normalizzato
    """
    if not isinstance(url, str):
        return url

    return url.replace("\\", "")


def validate_normattiva_url(url):
    """
    Validates that a URL is from the allowed normattiva.it domain and uses HTTPS.

    Args:
        url: URL string to validate

    Returns:
        bool: True if URL is valid and safe to fetch

    Raises:
        ValueError: If URL is invalid or not from allowed domain
    """
    try:
        url = normalize_normattiva_url(url)
        parsed = urlparse(url)

        # Check scheme is HTTPS
        if parsed.scheme != "https":
            raise ValueError(
                f"Solo HTTPS è consentito. URL fornito usa: {parsed.scheme}"
            )

        # Check domain is in whitelist
        if parsed.netloc.lower() not in ALLOWED_DOMAINS:
            raise ValueError(
                f"Dominio non consentito: {parsed.netloc}. Domini permessi: {', '.join(ALLOWED_DOMAINS)}"
            )

        return True

    except Exception as e:
        raise ValueError(f"URL non valido: {e}")


def is_normattiva_url(input_str):
    """
    Verifica se l'input è un URL di normattiva.it

    Args:
        input_str: stringa da verificare

    Returns:
        bool: True se è un URL normattiva.it valido e sicuro
    """
    if not isinstance(input_str, str):
        return False

    normalized = normalize_normattiva_url(input_str)

    # Check if it looks like a URL
    if not re.match(r"https?://(www\.)?normattiva\.it/", normalized, re.IGNORECASE):
        return False

    # Validate URL for security
    try:
        validate_normattiva_url(normalized)
        return True
    except ValueError:
        return False


def is_normattiva_export_url(url):
    """
    Verifica se l'URL è un URL di esportazione atto intero di normattiva.it

    Questi URL non sono supportati perché richiedono autenticazione per il download XML.
    Si consiglia di usare gli URL permalink (URN) invece.

    Args:
        url: URL da verificare

    Returns:
        bool: True se è un URL di esportazione atto intero
    """
    if not isinstance(url, str):
        return False

    # Check if it's an export URL
    return "/esporta/attoCompleto" in url and is_normattiva_url(url)


def extract_params_from_normattiva_url(url, session=None, quiet=False):
    """
    Scarica la pagina normattiva e estrae i parametri necessari per il download

    Supporta URL permalink (URN) di normattiva.it visitando la pagina HTML
    e estraendo i parametri dagli input hidden.

    Gli URL di esportazione atto intero (/esporta/attoCompleto) non sono supportati
    perché richiedono autenticazione per il download XML. Usa gli URL permalink invece.

    Args:
        url: URL della norma su normattiva.it
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        tuple: (params dict, session)
    """
    url = normalize_normattiva_url(url)

    # Reject export URLs as they require authentication
    if is_normattiva_export_url(url):
        print(
            "❌ ERRORE: Gli URL di esportazione atto intero (/esporta/attoCompleto) non sono supportati",
            file=sys.stderr,
        )
        print(
            "   perché richiedono autenticazione per il download XML.", file=sys.stderr
        )
        print("   Usa invece gli URL permalink (URN) come:", file=sys.stderr)
        print(
            "   https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:AAAA-MM-GG;N",
            file=sys.stderr,
        )
        return None, session

    # For permalink URLs, visit the page and extract parameters from HTML
    if not quiet:
        print(f"Caricamento pagina {url}...", file=sys.stderr)

    if session is None:
        session = requests.Session()

    headers = {
        "User-Agent": f"Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    }

    try:
        response = session.get(
            url, headers=headers, timeout=DEFAULT_TIMEOUT, verify=True
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel caricamento della pagina: {e}", file=sys.stderr)
        return None, session

    html = response.text

    # Estrai parametri dagli input hidden usando regex
    params = {}

    # Cerca atto.dataPubblicazioneGazzetta
    match_gu = re.search(
        r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html
    )
    if match_gu:
        # Converti da formato YYYY-MM-DD a YYYYMMDD
        date_str = match_gu.group(1).replace("-", "")
        params["dataGU"] = date_str

    # Cerca atto.codiceRedazionale
    match_codice = re.search(
        r'name="atto\.codiceRedazionale"[^>]*value="([^"]+)"', html
    )
    if match_codice:
        params["codiceRedaz"] = match_codice.group(1)

    # Cerca la data di vigenza dall'input visibile
    match_vigenza = re.search(r'<input[^>]*value="(\d{2}/\d{2}/\d{4})"[^>]*>', html)
    if match_vigenza:
        # Converti da formato DD/MM/YYYY a YYYYMMDD
        date_parts = match_vigenza.group(1).split("/")
        params["dataVigenza"] = f"{date_parts[2]}{date_parts[1]}{date_parts[0]}"
    else:
        # Usa data odierna se non trovata
        params["dataVigenza"] = datetime.now().strftime("%Y%m%d")

    if not all(k in params for k in ["dataGU", "codiceRedaz", "dataVigenza"]):
        print(
            "Errore: impossibile estrarre tutti i parametri necessari", file=sys.stderr
        )
        print(f"Parametri trovati: {params}", file=sys.stderr)
        return None, session

    return params, session


def download_akoma_ntoso(params, output_path, session=None, quiet=False):
    """
    Scarica il documento Akoma Ntoso usando i parametri estratti

    Args:
        params: dizionario con dataGU, codiceRedaz, dataVigenza
        output_path: percorso dove salvare il file XML
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        bool: True se il download è riuscito
    """
    url = f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={params['dataGU']}&codiceRedaz={params['codiceRedaz']}&dataVigenza={params['dataVigenza']}"

    if not quiet:
        print(f"Download Akoma Ntoso da: {url}", file=sys.stderr)

    if session is None:
        session = requests.Session()

    headers = {
        "User-Agent": f"Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
        "Referer": "https://www.normattiva.it/",
    }

    try:
        response = session.get(
            url,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True,
            verify=True,
        )
        response.raise_for_status()

        # Check file size before processing
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > MAX_FILE_SIZE_BYTES:
            print(
                f"❌ Errore: file troppo grande ({int(content_length) / 1024 / 1024:.1f}MB). Massimo consentito: {MAX_FILE_SIZE_MB}MB",
                file=sys.stderr,
            )
            return False

        # Verifica che sia XML
        if response.content[:5] == b"<?xml" or b"<akomaNtoso" in response.content[:500]:
            with open(output_path, "wb") as f:
                f.write(response.content)
            if not quiet:
                print(f"✅ File XML salvato in: {output_path}", file=sys.stderr)
            return True
        else:
            print(f"❌ Errore: la risposta non è un file XML valido", file=sys.stderr)
            # Salva comunque per debug
            debug_path = output_path + ".debug.html"
            with open(debug_path, "wb") as f:
                f.write(response.content)
            print(f"   Risposta salvata in: {debug_path}", file=sys.stderr)
            return False

    except requests.RequestException as e:
        print(f"❌ Errore durante il download: {e}", file=sys.stderr)
        return False
