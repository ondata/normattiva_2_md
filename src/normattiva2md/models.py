"""
Data models per API normattiva2md.

Definisce le strutture dati ritornate dalle funzioni API.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ConversionResult:
    """
    Risultato di una conversione XML → Markdown.

    Contiene sia il contenuto Markdown che i metadata estratti dal documento.
    Può essere usato direttamente come stringa o salvato su file.

    Attributes:
        markdown: Contenuto Markdown completo del documento
        metadata: Dictionary con metadata (dataGU, codiceRedaz, etc.)
        url: URL normattiva.it originale (se conversione da URL)
        url_xml: URL del file XML Akoma Ntoso scaricato

    Examples:
        >>> result = convert_url("https://...")
        >>> print(result.markdown[:100])
        >>> print(result.metadata['dataGU'])
        >>> result.save("output.md")
        >>>
        >>> # Conversione automatica a stringa
        >>> with open("out.md", "w") as f:
        ...     f.write(str(result))
    """

    markdown: str
    metadata: Dict[str, str]
    url: Optional[str] = None
    url_xml: Optional[str] = None

    def __str__(self) -> str:
        """
        Converte automaticamente a stringa = markdown.

        Permette di usare ConversionResult direttamente in contesti
        che si aspettano una stringa (print, f-string, file.write).

        Returns:
            Contenuto markdown completo
        """
        return self.markdown

    def save(self, path: str, encoding: str = "utf-8") -> None:
        """
        Salva contenuto markdown su file.

        Args:
            path: Path del file di output
            encoding: Encoding del file (default: utf-8)

        Raises:
            IOError: Se errore durante scrittura file

        Examples:
            >>> result = convert_url("https://...")
            >>> result.save("legge.md")
            >>> result.save("/path/to/output.md", encoding="utf-8")
        """
        try:
            with open(path, "w", encoding=encoding) as f:
                f.write(self.markdown)
        except IOError as e:
            print(f"Errore durante salvataggio file: {e}", file=sys.stderr)
            raise

    @property
    def title(self) -> Optional[str]:
        """
        Estrae titolo dal markdown (prima riga H1 se presente).

        Returns:
            Titolo del documento o None se non trovato

        Examples:
            >>> result = convert_url("https://...")
            >>> print(result.title)
            "Legge 9 gennaio 2004, n. 4"
        """
        for line in self.markdown.split("\n"):
            if line.startswith("# "):
                return line[2:].strip()
        return None

    @property
    def data_gu(self) -> Optional[str]:
        """Shortcut per metadata['dataGU']."""
        return self.metadata.get("dataGU")

    @property
    def codice_redaz(self) -> Optional[str]:
        """Shortcut per metadata['codiceRedaz']."""
        return self.metadata.get("codiceRedaz")

    @property
    def data_vigenza(self) -> Optional[str]:
        """Shortcut per metadata['dataVigenza']."""
        return self.metadata.get("dataVigenza")


@dataclass
class SearchResult:
    """
    Singolo risultato di ricerca da Exa AI.

    Rappresenta un documento trovato durante la ricerca in linguaggio naturale.

    Attributes:
        url: URL normattiva.it del documento
        title: Titolo del documento
        score: Score di relevance (0.0 - 1.0, più alto = più rilevante)

    Examples:
        >>> results = search_law("legge stanca")
        >>> best = results[0]
        >>> print(f"{best.title} - Score: {best.score:.2f}")
        >>> print(f"URL: {best.url}")
    """

    url: str
    title: str
    score: float

    def __str__(self) -> str:
        """
        Rappresentazione stringa leggibile del risultato.

        Returns:
            Stringa formattata con titolo e score

        Examples:
            >>> result = SearchResult(url="...", title="Legge 4/2004", score=0.95)
            >>> print(result)
            "[0.95] Legge 4/2004"
        """
        return f"[{self.score:.2f}] {self.title}"

    def __repr__(self) -> str:
        """Rappresentazione tecnica del risultato."""
        return f"SearchResult(url={self.url!r}, title={self.title!r}, score={self.score})"


# Type aliases per chiarezza
Metadata = Dict[str, str]
SearchResults = List[SearchResult]
