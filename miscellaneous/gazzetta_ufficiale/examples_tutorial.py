#!/usr/bin/env python3
"""
Tutorial esempi Gazzetta Ufficiale API Client

Esempi progressivi dal più semplice al più complesso.
Adatto per developer junior che vogliono imparare l'uso del client.
"""

from gazzetta_api_client import GazzettaUfficialeClient
import json
import csv


def esempio_1_ricerca_base():
    """
    ESEMPIO 1: Ricerca base

    La ricerca più semplice: cercare una parola nel titolo.
    """
    print("=" * 60)
    print("ESEMPIO 1: Ricerca base - parola nel titolo")
    print("=" * 60)

    # Crea il client
    client = GazzettaUfficialeClient()

    # Cerca "ambiente" nel titolo
    results = client.search(title="ambiente")

    # Mostra quanti risultati abbiamo trovato
    print(f"\nTrovati {results['total_results']} atti con 'ambiente' nel titolo")
    print(f"Risultati in questa pagina: {len(results['results'])}")

    # Mostra i primi 3 risultati
    print("\nPrimi 3 risultati:")
    for i, r in enumerate(results["results"][:3], 1):
        print(f"\n{i}. {r['act_type']}")
        print(f"   Titolo: {r['title'][:80]}...")
        print(f"   {r['gu_reference']}")


def esempio_2_ricerca_tipo_atto():
    """
    ESEMPIO 2: Filtrare per tipo di atto

    Cercare solo un tipo specifico di atto (decreto, legge, ecc.)
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 2: Filtrare per tipo di atto")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    # Cerca solo DECRETI con "covid" nel titolo
    results = client.search(act_type="decreto", title="covid")

    print(f"\nTrovati {results['total_results']} decreti con 'covid' nel titolo")

    # Conta i diversi tipi di decreti
    tipi = {}
    for r in results["results"]:
        tipo = r["act_type"]
        tipi[tipo] = tipi.get(tipo, 0) + 1

    print("\nTipi di atti trovati:")
    for tipo, count in tipi.items():
        print(f"  {tipo}: {count}")


def esempio_3_ricerca_periodo():
    """
    ESEMPIO 3: Ricerca in un periodo temporale

    Cercare atti pubblicati in un intervallo di date specifico.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 3: Ricerca in un periodo")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    # Cerca atti pubblicati a gennaio 2024
    results = client.search(
        title="salute",
        pub_start_day="01",
        pub_start_month="01",
        pub_start_year="2024",
        pub_end_day="31",
        pub_end_month="01",
        pub_end_year="2024",
    )

    print(
        f"\nTrovati {results['total_results']} atti con 'salute' pubblicati a gennaio 2024"
    )

    # Mostra le date di pubblicazione
    print("\nDate pubblicazione trovate:")
    for r in results["results"][:5]:
        print(f"  {r['gu_reference']}")


def esempio_4_modalita_ricerca():
    """
    ESEMPIO 4: Diverse modalità di ricerca testuale

    Differenza tra ALL_WORDS, ENTIRE_STRING, SOME_WORDS
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 4: Modalità di ricerca testuale")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    # Modo 1: TUTTE le parole (AND)
    r1 = client.search(title="ministero salute", title_search_type="ALL_WORDS")
    print(f"\nALL_WORDS ('ministero' AND 'salute'): {r1['total_results']} risultati")

    # Modo 2: FRASE ESATTA
    r2 = client.search(title="ministero salute", title_search_type="ENTIRE_STRING")
    print(f"ENTIRE_STRING ('ministero salute' esatto): {r2['total_results']} risultati")

    # Modo 3: ALMENO UNA parola (OR)
    r3 = client.search(title="ministero salute", title_search_type="SOME_WORDS")
    print(f"SOME_WORDS ('ministero' OR 'salute'): {r3['total_results']} risultati")


def esempio_5_paginazione():
    """
    ESEMPIO 5: Gestire la paginazione

    Come scaricare risultati da più pagine.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 5: Paginazione")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    # Raccogli risultati da più pagine
    all_results = []

    for page in range(3):  # Prime 3 pagine
        results = client.search(title="decreto", page=page)

        if not results["has_results"]:
            print(f"\nNessun risultato a pagina {page}, uscita")
            break

        all_results.extend(results["results"])
        print(f"Pagina {page}: scaricati {len(results['results'])} risultati")

        # Se non ci sono altre pagine, esci
        if str(page + 1) not in results.get("pagination", {}):
            print("Nessuna pagina successiva, uscita")
            break

    print(f"\nTotale risultati scaricati: {len(all_results)}")


def esempio_6_escludi_parole():
    """
    ESEMPIO 6: Escludere parole dalla ricerca

    Cercare qualcosa MA escludendo certi termini.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 6: Escludere parole")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    # Cerca "vaccino" ma ESCLUDI "covid"
    results = client.search(title="vaccino", title_exclude="covid")

    print(f"\nTrovati {results['total_results']} atti con 'vaccino' ma senza 'covid'")

    # Verifica che davvero non ci sia "covid"
    print("\nPrimi 3 risultati (verifica assenza 'covid'):")
    for i, r in enumerate(results["results"][:3], 1):
        title_lower = r["title"].lower()
        ha_covid = "covid" in title_lower
        print(f"\n{i}. {r['title'][:60]}...")
        print(f"   Contiene 'covid': {ha_covid}")


def esempio_7_emettitore():
    """
    ESEMPIO 7: Raggruppare per emettitore

    Analizzare quali enti hanno emesso gli atti trovati.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 7: Raggruppare per emettitore")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    results = client.search(title="farmaco")

    # Conta per emettitore
    emettitori = {}
    senza_emettitore = 0

    for r in results["results"]:
        if "emettitore" in r:
            em = r["emettitore"]
            emettitori[em] = emettitori.get(em, 0) + 1
        else:
            senza_emettitore += 1

    print(f"\nTrovati {results['total_results']} atti con 'farmaco'")
    print(f"Atti senza emettitore specificato: {senza_emettitore}")
    print("\nAtti per emettitore:")

    # Ordina per numero di atti (decrescente)
    for em, count in sorted(emettitori.items(), key=lambda x: x[1], reverse=True):
        print(f"  {count:3d}x {em}")


def esempio_8_esporta_csv():
    """
    ESEMPIO 8: Esportare risultati in CSV

    Salvare i risultati in un file CSV per analisi successive.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 8: Esportare in CSV")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    results = client.search(title="energia", page=0)

    filename = "risultati_energia.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "act_type",
                "act_date",
                "gu_reference",
                "title",
                "emettitore",
                "link",
            ],
        )
        writer.writeheader()

        for r in results["results"]:
            writer.writerow(
                {
                    "act_type": r.get("act_type", ""),
                    "act_date": r.get("act_date", ""),
                    "gu_reference": r.get("gu_reference", ""),
                    "title": r.get("title", ""),
                    "emettitore": r.get("emettitore", ""),
                    "link": f"https://www.gazzettaufficiale.it{r.get('link', '')}",
                }
            )

    print(f"\n✓ Salvati {len(results['results'])} risultati in '{filename}'")
    print(f"  Puoi aprirlo con Excel, LibreOffice Calc, o qualsiasi editor CSV")


def esempio_9_esporta_json():
    """
    ESEMPIO 9: Esportare risultati in JSON

    Salvare i risultati in formato JSON per elaborazioni programmatiche.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 9: Esportare in JSON")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    results = client.search(title="sostenibilità")

    filename = "risultati_sostenibilita.json"

    # Prepara dati per export (rimuovi raw_html per ridurre dimensione file)
    export_data = {
        "total_results": results["total_results"],
        "has_results": results["has_results"],
        "pagination": results["pagination"],
        "results": results["results"],
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Salvati {len(results['results'])} risultati in '{filename}'")
    print(f"  Formato: JSON (facile da leggere con Python, JavaScript, ecc.)")


def esempio_10_ricerca_complessa():
    """
    ESEMPIO 10: Ricerca complessa con più filtri

    Combinare più parametri per una ricerca molto specifica.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 10: Ricerca complessa")
    print("=" * 60)

    client = GazzettaUfficialeClient()

    # Cerca:
    # - DECRETI (non leggi, non determinazioni)
    # - con "ambiente" O "sostenibilità" nel titolo
    # - con "clima" nel testo
    # - pubblicati nel 2024
    results = client.search(
        act_type="decreto",
        title="ambiente sostenibilità",
        title_search_type="SOME_WORDS",  # OR: almeno una parola
        text="clima",
        pub_start_year="2024",
        pub_end_year="2024",
        page=0,
    )

    print(f"\nCriteri ricerca:")
    print("  - Tipo: DECRETO")
    print("  - Titolo: 'ambiente' OR 'sostenibilità'")
    print("  - Testo: 'clima'")
    print("  - Anno: 2024")

    print(f"\nTrovati {results['total_results']} atti")

    if results["results"]:
        print("\nPrimi risultati:")
        for i, r in enumerate(results["results"][:3], 1):
            print(f"\n{i}. {r['act_type']} - {r.get('act_date', 'N/A')}")
            print(f"   {r['title'][:100]}...")
            print(f"   {r['gu_reference']}")


def esempio_11_gestione_errori():
    """
    ESEMPIO 11: Gestire errori e casi limite

    Come gestire situazioni problematiche.
    """
    print("\n" + "=" * 60)
    print("ESEMPIO 11: Gestione errori")
    print("=" * 60)

    from requests.exceptions import RequestException

    client = GazzettaUfficialeClient()

    # Caso 1: Ricerca senza risultati
    print("\nCaso 1: Ricerca senza risultati")
    results = client.search(title="xyzabc123nonexistent")

    if not results["has_results"]:
        print("  ✗ Nessun risultato trovato")
    else:
        print(f"  ✓ Trovati {results['total_results']} risultati")

    # Caso 2: Gestire errori di connessione
    print("\nCaso 2: Gestire errori di rete")
    try:
        # Questo dovrebbe funzionare
        results = client.search(title="test")
        print(f"  ✓ Connessione OK, {results['total_results']} risultati")
    except RequestException as e:
        print(f"  ✗ Errore connessione: {e}")

    # Caso 3: Verificare campi opzionali
    print("\nCaso 3: Campi opzionali nei risultati")
    results = client.search(title="decreto")

    if results["results"]:
        r = results["results"][0]
        print(f"  act_type: {'✓' if 'act_type' in r else '✗'} (sempre presente)")
        print(f"  act_date: {'✓' if 'act_date' in r else '✗'} (opzionale)")
        print(f"  emettitore: {'✓' if 'emettitore' in r else '✗'} (opzionale)")
        print(f"  link: {'✓' if 'link' in r else '✗'} (sempre presente)")


def main():
    """
    Esegui tutti gli esempi in sequenza.

    Per eseguire un solo esempio, commenta gli altri nella lista.
    """
    esempi = [
        esempio_1_ricerca_base,
        esempio_2_ricerca_tipo_atto,
        esempio_3_ricerca_periodo,
        esempio_4_modalita_ricerca,
        esempio_5_paginazione,
        esempio_6_escludi_parole,
        esempio_7_emettitore,
        esempio_8_esporta_csv,
        esempio_9_esporta_json,
        esempio_10_ricerca_complessa,
        esempio_11_gestione_errori,
    ]

    print("\n" + "=" * 60)
    print("TUTORIAL GAZZETTA UFFICIALE API CLIENT")
    print("=" * 60)
    print(f"\nEseguirò {len(esempi)} esempi progressivi...")
    print("Premi Ctrl+C per interrompere in qualsiasi momento\n")

    try:
        for i, esempio in enumerate(esempi, 1):
            esempio()

            # Pausa tra esempi (solo se non è l'ultimo)
            if i < len(esempi):
                input(
                    f"\n[Premi INVIO per continuare con esempio {i + 1}/{len(esempi)}...]"
                )

    except KeyboardInterrupt:
        print("\n\nInterrotto dall'utente.")

    print("\n" + "=" * 60)
    print("Tutorial completato!")
    print("=" * 60)
    print("\nProssimi passi:")
    print("  1. Leggi README.md per documentazione completa")
    print("  2. Modifica questi esempi per le tue esigenze")
    print("  3. Consulta gazzetta_api_client.py per dettagli implementazione")


if __name__ == "__main__":
    main()
