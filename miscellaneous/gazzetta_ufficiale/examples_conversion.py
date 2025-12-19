#!/usr/bin/env python3
"""
Esempi conversione Gazzetta Ufficiale → Markdown

Dimostra come utilizzare GazzettaConverter per convertire atti
della Gazzetta Ufficiale in formato Markdown.
"""

from gazzetta_converter import GazzettaConverter


def esempio_1_conversione_base():
    """
    ESEMPIO 1: Conversione base URL ELI → Markdown file

    Converte un atto dalla Gazzetta Ufficiale in file Markdown.
    """
    print("=" * 60)
    print("ESEMPIO 1: Conversione base")
    print("=" * 60)

    # URL ELI dell'atto
    eli_url = "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg"

    # Crea converter
    converter = GazzettaConverter()

    # Converti e salva in file
    try:
        converter.convert_to_file(eli_url, "esempio1_output.md")
        print("\n✓ Conversione completata: esempio1_output.md")
    except Exception as e:
        print(f"\n✗ Errore conversione: {e}")


def esempio_2_conversione_stdout():
    """
    ESEMPIO 2: Conversione con output su stdout

    Converte un atto e stampa il risultato su console.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 2: Output su stdout")
    print("=" * 60)

    eli_url = "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg"

    converter = GazzettaConverter()

    try:
        # Converti e ottieni markdown come stringa
        markdown = converter.convert_to_markdown(eli_url)

        # Mostra prime 50 righe
        lines = markdown.split("\n")[:50]
        print("\nPrime 50 righe del markdown:\n")
        print("\n".join(lines))
        print("\n... (output troncato)")
    except Exception as e:
        print(f"\n✗ Errore conversione: {e}")


def esempio_3_con_note():
    """
    ESEMPIO 3: Conversione con note incluse

    Converte un atto includendo le note (se disponibili).
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 3: Conversione con note")
    print("=" * 60)

    eli_url = "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg"

    converter = GazzettaConverter()

    try:
        # Converti includendo le note
        converter.convert_to_file(eli_url, "esempio3_con_note.md", include_note=True)
        print("\n✓ Conversione con note completata: esempio3_con_note.md")
    except Exception as e:
        print(f"\n✗ Errore conversione: {e}")


def esempio_4_parsing_url():
    """
    ESEMPIO 4: Parsing URL ELI

    Dimostra come estrarre parametri da URL ELI.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 4: Parsing URL ELI")
    print("=" * 60)

    converter = GazzettaConverter()

    # Esempi di URL ELI
    urls = [
        "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg",
        "https://www.gazzettaufficiale.it/eli/id/2024/03/15/24A01234/sg",
        "https://www.gazzettaufficiale.it/eli/id/2023/01/01/23A00001/sg",
    ]

    print("\nParsing URL ELI:\n")
    for url in urls:
        try:
            params = converter.parse_eli_url(url)
            print(f"URL: {url}")
            print(f"  Data: {params['data']}")
            print(f"  Codice: {params['codice']}\n")
        except ValueError as e:
            print(f"URL: {url}")
            print(f"  Errore: {e}\n")


def esempio_5_batch_conversion():
    """
    ESEMPIO 5: Conversione batch di più atti

    Converte più atti in sequenza.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 5: Conversione batch")
    print("=" * 60)

    # Lista di URL ELI da convertire
    urls = [
        "https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg",
        # Aggiungi altri URL qui
    ]

    converter = GazzettaConverter()

    print(f"\nConversione {len(urls)} atti:\n")
    for i, url in enumerate(urls, 1):
        try:
            # Estrai codice per nome file
            params = converter.parse_eli_url(url)
            filename = f"atto_{params['codice']}.md"

            converter.convert_to_file(url, filename)
            print(f"{i}. ✓ {filename}")
        except Exception as e:
            print(f"{i}. ✗ Errore: {e}")


def esempio_6_gestione_errori():
    """
    ESEMPIO 6: Gestione errori

    Dimostra come gestire errori comuni.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 6: Gestione errori")
    print("=" * 60)

    converter = GazzettaConverter()

    # Test 1: URL non valido
    print("\nTest 1: URL non valido")
    try:
        converter.parse_eli_url("https://example.com/invalid")
        print("  ✗ Dovrebbe generare errore")
    except ValueError as e:
        print(f"  ✓ Errore gestito correttamente: {e}")

    # Test 2: Atto inesistente
    print("\nTest 2: Atto inesistente (se fallisce)")
    try:
        # URL con codice inventato
        eli_url = "https://www.gazzettaufficiale.it/eli/id/2025/12/06/99X99999/sg"
        converter.convert_to_markdown(eli_url)
        print("  ✓ Atto trovato (oppure gestito)")
    except Exception as e:
        print(f"  ✓ Errore gestito: {type(e).__name__}")


def main():
    """
    Esegui tutti gli esempi in sequenza.
    """
    print("\n" + "=" * 60)
    print("ESEMPI CONVERSIONE GAZZETTA UFFICIALE → MARKDOWN")
    print("=" * 60)

    esempi = [
        esempio_1_conversione_base,
        esempio_2_conversione_stdout,
        esempio_3_con_note,
        esempio_4_parsing_url,
        esempio_5_batch_conversion,
        esempio_6_gestione_errori,
    ]

    try:
        for i, esempio in enumerate(esempi, 1):
            esempio()

            # Pausa tra esempi (solo se non è l'ultimo)
            if i < len(esempi):
                input(f"\n[Premi INVIO per esempio {i + 1}/{len(esempi)}...]")

    except KeyboardInterrupt:
        print("\n\nInterrotto dall'utente.")

    print("\n" + "=" * 60)
    print("Esempi completati!")
    print("=" * 60)


if __name__ == "__main__":
    main()
