#!/usr/bin/env python3
"""
Gazzetta Ufficiale API Client

Client Python per ricerche programmatiche sulla Gazzetta Ufficiale della Repubblica Italiana.

NOTA: Questo NON è un'API ufficiale. È stato ottenuto tramite reverse engineering
del form di ricerca web (https://www.gazzettaufficiale.it/eli/ricerca).

Esempio uso base:
    >>> from gazzetta_api_client import GazzettaUfficialeClient
    >>> client = GazzettaUfficialeClient()
    >>> results = client.search(title="ambiente")
    >>> print(f"Trovati {results['total_results']} atti")
    >>> for r in results['results']:
    ...     print(f"{r['act_type']}: {r['title'][:50]}...")

Esempio ricerca avanzata:
    >>> results = client.search(
    ...     act_type="decreto",
    ...     title="ambiente",
    ...     pub_start_year="2024",
    ...     page=0
    ... )

Per documentazione completa: vedi README.md

Dipendenze:
    - requests
    - beautifulsoup4

Limitazioni:
    - Max 500 risultati visualizzabili (6 pagine)
    - Richiede sessione valida (gestita automaticamente)
    - Solo Serie Generale supportata

Author: Reverse Engineered from https://www.gazzettaufficiale.it/eli/ricerca
"""

import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlencode
from typing import Dict, List, Optional, NamedTuple, Any
import re
import time


class GazzettaUfficialeClient:
    """Client for Gazzetta Ufficiale search functionality"""

    def __init__(self, base_url: str = "https://www.gazzettaufficiale.it"):
        self.base_url = base_url
        self.session = requests.Session()
        self._last_response = None
        # Set headers to mimic browser behavior
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
        )

    def search(
        self,
        act_type: Optional[str] = None,
        act_number: Optional[str] = None,
        act_day: Optional[str] = None,
        act_month: Optional[str] = None,
        act_year: Optional[str] = None,
        title: Optional[str] = None,
        title_exclude: Optional[str] = None,
        title_search_type: str = "ALL_WORDS",
        text: Optional[str] = None,
        text_exclude: Optional[str] = None,
        text_search_type: str = "ALL_WORDS",
        pub_start_day: Optional[str] = None,
        pub_start_month: Optional[str] = None,
        pub_start_year: Optional[str] = None,
        pub_end_day: Optional[str] = None,
        pub_end_month: Optional[str] = None,
        pub_end_year: Optional[str] = None,
        page: int = 0,
    ) -> Dict:
        """
        Perform search on Gazzetta Ufficiale

        Args:
            act_type: Type of act (e.g., "decreto", "legge")
            act_number: Act number
            act_day: Act day (dd)
            act_month: Act month (mm)
            act_year: Act year (yyyy)
            title: Words in title
            title_exclude: Words to exclude from title
            title_search_type: Title search method ("ALL_WORDS", "ENTIRE_STRING", "SOME_WORDS")
            text: Words in text content
            text_exclude: Words to exclude from text
            text_search_type: Text search method ("ALL_WORDS", "ENTIRE_STRING", "SOME_WORDS")
            pub_start_day: Publication start day (dd)
            pub_start_month: Publication start month (mm)
            pub_start_year: Publication start year (yyyy)
            pub_end_day: Publication end day (dd)
            pub_end_month: Publication end month (mm)
            pub_end_year: Publication end year (yyyy)
            page: Page number (0-based)

        Returns:
            Dictionary containing search results and metadata
        """

        # Build form data - ALL fields must be present, even if empty
        form_data = {
            "numeroProvvedimento": act_number or "",
            "giornoProvvedimento": act_day or "",
            "meseProvvedimento": act_month or "",
            "annoProvvedimento": act_year or "",
            "attiNumerati": "false",
            "descrizioneTipoProvvedimento": act_type or "",
            "codiceTipoProvvedimento": "",
            "descrizioneTipoProvvedimentoHidden": "",
            "descrizioneEmettitore": "",
            "codiceEmettitore": "",
            "descrizioneEmettitoreHidden": "",
            "descrizioneMateria": "",
            "codiceMateria": "",
            "descrizioneMateriaHidden": "",
            "tipoRicercaTitolo": title_search_type,
            "titolo": title or "",
            "titoloNot": title_exclude or "",
            "tipoRicercaTesto": text_search_type,
            "testo": text or "",
            "testoNot": text_exclude or "",
            "giornoPubblicazioneDa": pub_start_day or "",
            "mesePubblicazioneDa": pub_start_month or "",
            "annoPubblicazioneDa": pub_start_year or "",
            "giornoPubblicazioneA": pub_end_day or "",
            "mesePubblicazioneA": pub_end_month or "",
            "annoPubblicazioneA": pub_end_year or "",
            "cerca": "Cerca",
        }

        # First, visit the search page to get a session
        search_page_url = f"{self.base_url}/eli/ricerca"
        try:
            self.session.get(search_page_url)
        except requests.RequestException:
            pass  # Continue even if initial page load fails

        # Construct URL with page number
        url = f"{self.base_url}/do/ricerca/atto/serie_generale/originario/{page}"

        try:
            response = self.session.post(url, data=form_data)
            response.raise_for_status()
            self._last_response = response

            return self._parse_response(response.text)

        except requests.RequestException as e:
            return {
                "error": f"Request failed: {str(e)}",
                "status_code": None,
                "results": [],
            }

    def get_page(self, page: int = 0) -> Dict:
        """Get a specific page of results"""
        url = f"{self.base_url}/do/ricerca/atto/serie_generale/originario/{page}?cerca"

        try:
            response = self.session.get(url)
            response.raise_for_status()

            return self._parse_response(response.text)

        except requests.RequestException as e:
            return {
                "error": f"Request failed: {str(e)}",
                "status_code": None,
                "results": [],
            }

    def _parse_response(self, html_content: str) -> Dict:
        """Parse HTML response to extract structured data"""
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract result count from "Risultati della ricerca: X atti"
        total_results = 0
        count_div = soup.find("div", class_="count_risultati")
        if count_div:
            count_text = count_div.get_text()
            match = re.search(r"Risultati della ricerca:\s*(\d+)\s*att[io]", count_text)
            if match:
                total_results = int(match.group(1))

        # Extract pagination info
        pagination = {}
        pagination_element = soup.find("span", class_="paginatore")
        if pagination_element and isinstance(pagination_element, Tag):
            # Find all page links
            page_links = pagination_element.find_all("a")
            for link in page_links:
                if isinstance(link, Tag):
                    href = link.get("href")
                    if href and isinstance(href, str) and "/originario/" in href:
                        page_num = href.split("/")[-1].split("?")[0]
                        if page_num.isdigit():
                            pagination[page_num] = link.get_text().strip()

        # Extract results from <span class="risultato">
        results = []
        current_emettitore = None

        # Find all risultato and emettitore spans
        all_spans = soup.find_all("span")
        for element in all_spans:
            if not isinstance(element, Tag):
                continue

            classes = element.get("class")
            if not classes or not isinstance(classes, list):
                continue

            # Track current emettitore
            if "emettitore" in classes:
                current_emettitore = element.get_text().strip()
                continue

            # Process risultato spans
            if "risultato" in classes:
                result: Dict[str, str] = {}

                # Find the data span (act type and date)
                data_span = element.find("span", class_="data")
                if data_span:
                    data_text = data_span.get_text().strip()
                    # Split by newlines and clean
                    lines = [l.strip() for l in data_text.split("\n") if l.strip()]
                    if lines:
                        result["act_type"] = lines[0]
                        if len(lines) > 1:
                            result["act_date"] = lines[1]

                # Find the riferimento span (GU reference)
                rif_span = element.find("span", class_="riferimento")
                if rif_span:
                    result["gu_reference"] = rif_span.get_text().strip()

                # Find all links in this risultato
                links = element.find_all("a")
                if links:
                    # First link usually contains href
                    first_link = links[0]
                    if isinstance(first_link, Tag):
                        href = first_link.get("href")
                        if href and isinstance(href, str):
                            result["link"] = href

                        # Second link (if exists) contains the title/description
                        if len(links) > 1:
                            title_link = links[1]
                            if isinstance(title_link, Tag):
                                # Get text and clean it
                                title_text = title_link.get_text()
                                result["title"] = title_text.strip()
                        else:
                            result["title"] = first_link.get_text().strip()

                # Add emettitore if available
                if current_emettitore:
                    result["emettitore"] = current_emettitore

                # Only add if we got useful data
                if result.get("title") or result.get("link"):
                    results.append(result)

        return {
            "total_results": total_results,
            "pagination": pagination,
            "results": results,
            "has_results": len(results) > 0,
            "raw_html": html_content,
        }


class SearchResult(NamedTuple):
    """Structured search result"""

    title: str
    act_type: str
    act_date: str
    gu_reference: str
    publication_date: str
    link: str
    raw_text: str


def main():
    """Example usage of Gazzetta Ufficiale client"""

    client = GazzettaUfficialeClient()

    print("=== Gazzetta Ufficiale API Client Demo ===\n")

    # Example 1: Search by act type
    print("1. Searching for 'decreto' acts...")
    results = client.search(act_type="decreto", page=0)
    print(f"   Found {results['total_results']} total results")
    print(f"   Showing {len(results['results'])} results on page 0")

    if results["has_results"]:
        for i, result in enumerate(results["results"][:3]):  # Show first 3 results
            act_type = result.get("act_type", "N/A")
            act_date = result.get("act_date", "N/A")
            gu_ref = result.get("gu_reference", "N/A")
            print(f"   {i + 1}. {act_type} {act_date}")
            print(f"      {result['title'][:80]}...")
            print(f"      GU: {gu_ref}")
            print()

    # Example 2: Search by title
    print("\n2. Searching for 'ambiente' in title...")
    results = client.search(title="ambiente", page=0)
    print(f"   Found {results['total_results']} total results")

    # Example 3: Search by date range
    print("\n3. Searching for acts from 2023...")
    results = client.search(pub_start_year="2023", page=0)
    print(f"   Found {results['total_results']} total results")

    # Example 4: Get page 2
    print("\n4. Getting page 2 of results...")
    page2_results = client.get_page(page=2)
    print(f"   Page 2 contains {len(page2_results['results'])} results")

    # Example 5: Combined search
    print("\n5. Combined search: 'decreto' + 'ambiente' in 2023...")
    results = client.search(
        act_type="decreto", title="ambiente", pub_start_year="2023", page=0
    )
    print(f"   Found {results['total_results']} total results")

    print("\n=== End of Demo ===")


if __name__ == "__main__":
    main()
