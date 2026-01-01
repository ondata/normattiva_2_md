#!/usr/bin/env python3
"""
Basic usage examples for normattiva2md API.

Run with: python examples/basic_usage.py
"""

import sys
sys.path.insert(0, 'src')

from normattiva2md import convert_url, convert_xml, InvalidURLError


def example_convert_url():
    """Example: Convert from normattiva.it URL."""
    print("=== Conversione da URL ===\n")

    url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"

    try:
        result = convert_url(url, quiet=True)

        if result:
            print(f"Titolo: {result.title}")
            print(f"Data GU: {result.data_gu}")
            print(f"Codice Redaz: {result.codice_redaz}")
            print(f"\nPrimi 300 caratteri del markdown:")
            print(result.markdown[:300])
            print("...")
            print(f"\nLunghezza totale: {len(result.markdown)} caratteri")
        else:
            print("Conversione fallita (errore soft)")

    except InvalidURLError as e:
        print(f"URL non valido: {e}")


def example_convert_url_with_article():
    """Example: Extract specific article from URL."""
    print("\n=== Estrazione articolo specifico ===\n")

    url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4"

    result = convert_url(url, article="3", quiet=True)

    if result:
        print(f"Articolo estratto: {result.metadata.get('article', 'N/A')}")
        print(f"\nContenuto articolo:")
        print(result.markdown)
    else:
        print("Articolo non trovato")


def example_convert_xml():
    """Example: Convert local XML file."""
    print("\n=== Conversione da file XML locale ===\n")

    # This requires a local XML file - adjust path as needed
    xml_path = "test_data/20050516_005G0104_VIGENZA_20250130.xml"

    try:
        result = convert_xml(xml_path, quiet=True)

        if result:
            print(f"Titolo: {result.title}")
            print(f"Lunghezza: {len(result.markdown)} caratteri")
        else:
            print("Conversione fallita")

    except FileNotFoundError:
        print(f"File non trovato: {xml_path}")
        print("(Questo esempio richiede un file XML locale)")


if __name__ == "__main__":
    print("=" * 60)
    print("normattiva2md API - Esempi di utilizzo")
    print("=" * 60)

    # Run examples (comment out as needed)
    example_convert_url()
    # example_convert_url_with_article()  # Uncomment to test article extraction
    # example_convert_xml()  # Uncomment if you have local XML files
