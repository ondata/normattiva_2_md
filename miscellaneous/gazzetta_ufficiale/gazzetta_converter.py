#!/usr/bin/env python3
"""
Gazzetta Ufficiale Converter

Converte atti della Gazzetta Ufficiale in formato Markdown partendo da URL ELI.

Workflow:
1. Parse URL ELI per estrarre data e codice
2. Download HTML versione stampa tramite session HTTP
3. Convert HTML → Markdown con struttura preservata

Esempio uso:
    >>> from gazzetta_converter import GazzettaConverter
    >>> converter = GazzettaConverter()
    >>> markdown = converter.convert_to_markdown(
    ...     "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg"
    ... )
    >>> print(markdown)

Dipendenze:
    - requests
    - beautifulsoup4

Author: Based on reverse engineering of gazzettaufficiale.it
"""

import re
import requests
from bs4 import BeautifulSoup, NavigableString
from typing import Dict, Optional, List
from urllib.parse import urljoin


class GazzettaConverter:
    """Converter for Gazzetta Ufficiale documents to Markdown"""

    def __init__(self, base_url: str = "https://www.gazzettaufficiale.it"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
            }
        )

    def parse_eli_url(self, eli_url: str) -> Dict[str, str]:
        """
        Estrae parametri da URL ELI.

        Args:
            eli_url: URL formato https://www.gazzettaufficiale.it/eli/id/YYYY/MM/DD/CODICE/sg

        Returns:
            Dictionary con 'data' (YYYY-MM-DD) e 'codice'

        Raises:
            ValueError: se URL non valido
        """
        match = re.search(r"/eli/id/(\d{4})/(\d{2})/(\d{2})/([^/]+)/sg", eli_url)
        if not match:
            raise ValueError(f"URL ELI non valido: {eli_url}")

        return {
            "data": f"{match.group(1)}-{match.group(2)}-{match.group(3)}",
            "codice": match.group(4),
        }

    def build_menu_url(self, data: str, codice: str) -> str:
        """
        Costruisce URL menu atto completo.

        Args:
            data: Data formato YYYY-MM-DD
            codice: Codice redazionale

        Returns:
            URL completo
        """
        return (
            f"{self.base_url}/atto/vediMenuHTML?"
            f"atto.dataPubblicazioneGazzetta={data}&"
            f"atto.codiceRedazionale={codice}&"
            f"tipoSerie=serie_generale&"
            f"tipoVigenza=originario"
        )

    def build_stampa_url(self) -> str:
        """
        Costruisce URL stampa atto completo.

        Returns:
            URL completo
        """
        return f"{self.base_url}/atto/stampa/serie_generale/originario"

    def download_html(self, eli_url: str, include_note: bool = False) -> str:
        """
        Scarica HTML atto completo.

        Args:
            eli_url: URL ELI dell'atto
            include_note: Se True, include note (default: False)

        Returns:
            HTML contenuto atto completo

        Raises:
            requests.RequestException: errore download
        """
        # Parse URL ELI
        params = self.parse_eli_url(eli_url)

        # Step 1: GET menu per stabilire session e ottenere form
        menu_url = self.build_menu_url(params["data"], params["codice"])
        try:
            menu_response = self.session.get(menu_url)
            menu_response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(f"Errore accesso menu atto: {e}")

        # Step 2: Parse HTML menu per estrarre dati necessari
        soup = BeautifulSoup(menu_response.text, "html.parser")

        # Costruisci form data come lista di tuple (supporta chiavi duplicate)
        form_data = [
            ("_noteSelected", "1" if include_note else ""),
            ("creaHTML", "Visualizza"),
            ("annoVigenza", params["data"].split("-")[0]),
            ("meseVigenza", params["data"].split("-")[1]),
            ("giornoVigenza", params["data"].split("-")[2]),
            ("dataPubblicazioneGazzetta", params["data"]),
            ("codiceRedazionale", params["codice"]),
        ]

        # Trova tutti i checkbox articoli (name="articoliSelected")
        checkboxes = soup.find_all("input", {"name": "articoliSelected"})

        # Aggiungi ogni articolo al form data
        for checkbox in checkboxes:
            value = checkbox.get("value")
            if value:
                # Aggiungi hidden field _articoliSelected
                form_data.append(("_articoliSelected", "1"))
                # Aggiungi articolo selezionato
                form_data.append(("articoliSelected", value))

        # Step 3: POST stampa con form data
        stampa_url = self.build_stampa_url()

        try:
            stampa_response = self.session.post(stampa_url, data=form_data)
            stampa_response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(f"Errore download atto completo: {e}")

        return stampa_response.text

    def html_to_markdown(self, html_content: str) -> str:
        """
        Converte HTML Gazzetta Ufficiale in Markdown.

        Args:
            html_content: HTML atto completo

        Returns:
            Testo Markdown formattato
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Estrai tutto il testo dal body
        body = soup.find("body")
        if not body:
            return ""

        # Estrai testo con get_text() per semplicità
        text = body.get_text(separator="\n", strip=True)

        # Pulisci righe vuote multiple
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        markdown_lines = lines

        # Unisci e formatta
        markdown_text = "\n\n".join(line for line in markdown_lines if line)

        # Post-processing: identifica sezioni strutturali
        markdown_text = self._format_sections(markdown_text)

        return markdown_text

    def _format_sections(self, text: str) -> str:
        """
        Formatta sezioni specifiche del documento.

        Args:
            text: Testo grezzo

        Returns:
            Testo formattato con heading markdown
        """
        lines = text.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue  # Salta righe vuote

            # Identifica heading (tutto maiuscolo, corto)
            if line.isupper() and len(line) < 100 and not line.startswith("ART"):
                # Heading principale
                formatted_lines.append(f"# {line}")
            # Identifica articoli
            elif re.match(r"^Art\.\s+\d+", line, re.IGNORECASE):
                formatted_lines.append(f"## {line}")
            # Identifica "Delibera:", "Decretano:", etc
            elif re.match(
                r"^(Delibera|Decretano|Vista|Visto|Considerato|Ritenuto|Atteso|Preso\s+atto):",
                line,
                re.IGNORECASE,
            ):
                formatted_lines.append(f"\n**{line}**")
            # Testo normale
            else:
                formatted_lines.append(line)

        # Rimuovi righe vuote multiple
        result = "\n\n".join(formatted_lines)
        # Pulisci righe vuote triple o più
        result = re.sub(r"\n{3,}", "\n\n", result)

        return result

    def convert_to_markdown(self, eli_url: str, include_note: bool = False) -> str:
        """
        Converte atto Gazzetta Ufficiale da URL ELI a Markdown.

        Args:
            eli_url: URL ELI dell'atto
            include_note: Se True, include note (default: False)

        Returns:
            Testo Markdown

        Raises:
            ValueError: URL non valido
            requests.RequestException: errore download
        """
        # Download HTML
        html_content = self.download_html(eli_url, include_note)

        # Convert to Markdown
        markdown = self.html_to_markdown(html_content)

        return markdown

    def convert_to_file(
        self,
        eli_url: str,
        output_file: str,
        include_note: bool = False,
    ) -> None:
        """
        Converte atto e salva in file.

        Args:
            eli_url: URL ELI dell'atto
            output_file: Path file output
            include_note: Se True, include note (default: False)
        """
        markdown = self.convert_to_markdown(eli_url, include_note)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Atto convertito salvato in: {output_file}")


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python gazzetta_converter.py <URL_ELI> [output.md]")
        print(
            "\nExample:\n  python gazzetta_converter.py "
            "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg output.md"
        )
        sys.exit(1)

    eli_url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    converter = GazzettaConverter()

    try:
        if output_file:
            converter.convert_to_file(eli_url, output_file)
        else:
            markdown = converter.convert_to_markdown(eli_url)
            print(markdown)
    except Exception as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
