#!/usr/bin/env python3
"""
Batch processing example for normattiva2md API.

Shows how to convert multiple documents efficiently.

Run with: python examples/batch_processing.py
"""

import sys
sys.path.insert(0, 'src')

from normattiva2md import Converter


def batch_convert():
    """Convert multiple URLs in batch."""
    print("=== Batch Processing ===\n")

    urls = [
        "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2004-01-09;4",
        "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82",
    ]

    # Create converter with persistent configuration
    conv = Converter(quiet=True)

    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Conversione...")

        result = conv.convert_url(url)

        if result:
            # Generate filename from codice_redaz
            filename = f"tmp/legge_{result.codice_redaz or i}.md"

            # Save (uncomment to actually save)
            # result.save(filename)

            results.append((filename, result))
            print(f"  OK: {result.title[:50]}...")
        else:
            print(f"  FALLITO: {url}")

    # Report
    print(f"\n{'='*60}")
    print(f"Completati: {len(results)}/{len(urls)}")
    for filename, result in results:
        print(f"  - {filename}: {result.title[:40]}...")


if __name__ == "__main__":
    batch_convert()
