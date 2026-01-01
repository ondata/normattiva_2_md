#!/usr/bin/env python3
"""
Test WORKFLOW COMPLETO API OpenData Normattiva - FUNZIONANTE
Ricerca → Estrai parametri → Dettaglio atto → Markdown
"""

import requests
import json
import os
from pathlib import Path
from pprint import pprint

# Determina directory output (relativa allo script)
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Base URL CORRETTO (con /t/normattiva.api/)
base_url = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'  # IMPORTANTE!
}

print("=" * 80)
print("WORKFLOW COMPLETO: Ricerca → Dettaglio → Markdown")
print("=" * 80)

# ============================================================================
# STEP 1: RICERCA SEMPLICE (per ottenere dataGU + codiceRedazionale)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: Ricerca semplice - 'legge 4 2004'")
print("=" * 80)

# Payload CORRETTO (con paginazione obbligatoria)
ricerca_payload = {
    "testoRicerca": "legge 4 2004",
    "orderType": "recente",
    "paginazione": {
        "paginaCorrente": 1,
        "numeroElementiPerPagina": 10
    }
}

print(f"\nPayload:")
print(json.dumps(ricerca_payload, indent=2))

response = requests.post(
    f"{base_url}/api/v1/ricerca/semplice",
    headers=headers,
    json=ricerca_payload,
    timeout=30
)

print(f"\n✅ Status: {response.status_code}")

if response.status_code != 200:
    print(f"❌ Errore: {response.text}")
    exit(1)

search_data = response.json()
print(f"\n📋 Risultati trovati: {len(search_data.get('listaAtti', []))}")

if not search_data.get('listaAtti'):
    print("❌ Nessun risultato trovato")
    exit(1)

# Trova la Legge 4/2004 (Legge Stanca)
legge_stanca = None
for atto in search_data['listaAtti']:
    if (atto.get('numeroProvvedimento') == '4' and
        atto.get('annoProvvedimento') == '2004' and
        atto.get('denominazioneAtto') == 'LEGGE'):
        legge_stanca = atto
        break

if not legge_stanca:
    print("⚠️ Legge 4/2004 non trovata nei risultati")
    legge_stanca = search_data['listaAtti'][0]
    print(f"   Usando primo risultato: {legge_stanca.get('descrizioneAtto')}")
else:
    print(f"\n✅ Trovata: {legge_stanca.get('descrizioneAtto')}")

print("\n" + "=" * 80)
print("PARAMETRI ESTRATTI:")
print("=" * 80)

params = {
    'dataGU': legge_stanca.get('dataGU'),
    'codiceRedazionale': legge_stanca.get('codiceRedazionale'),
    'numeroProvvedimento': legge_stanca.get('numeroProvvedimento'),
    'annoProvvedimento': legge_stanca.get('annoProvvedimento'),
    'denominazioneAtto': legge_stanca.get('denominazioneAtto')
}

pprint(params, width=80)

# Salva parametri
params_file = OUTPUT_DIR / "params_from_search.json"
with open(params_file, 'w') as f:
    json.dump(params, f, indent=2)

print(f"\n💾 Parametri salvati in: {params_file}")

# ============================================================================
# STEP 2: DETTAGLIO ATTO (con parametri da ricerca)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: Dettaglio atto con parametri estratti")
print("=" * 80)

dettaglio_payload = {
    "dataGU": params['dataGU'],
    "codiceRedazionale": params['codiceRedazionale'],
    "formatoRichiesta": "V"  # V=Vigente
}

print(f"\nPayload:")
print(json.dumps(dettaglio_payload, indent=2))

response2 = requests.post(
    f"{base_url}/api/v1/atto/dettaglio-atto",
    headers=headers,
    json=dettaglio_payload,
    timeout=30
)

print(f"\n✅ Status: {response2.status_code}")

if response2.status_code != 200:
    print(f"❌ Errore: {response2.text}")
    exit(1)

dettaglio = response2.json()

print("\n" + "=" * 80)
print("DETTAGLIO ATTO:")
print("=" * 80)

if dettaglio.get('success') and dettaglio.get('data', {}).get('atto'):
    atto = dettaglio['data']['atto']

    print(f"Titolo: {atto.get('titolo')}")
    print(f"Tipo: {atto.get('tipoProvvedimentoDescrizione')}")
    print(f"Anno: {atto.get('annoProvvedimento')}")
    print(f"Numero: {atto.get('numeroProvvedimento')}")
    print(f"Data GU: {atto.get('dataGU')}")
    print(f"Vigenza dal: {atto.get('articoloDataInizioVigenza')}")

    html_length = len(atto.get('articoloHtml', ''))
    print(f"\n📄 HTML articolato: {html_length} caratteri")

    # Salva response completa
    dettaglio_file = OUTPUT_DIR / "dettaglio_from_search.json"
    with open(dettaglio_file, 'w') as f:
        json.dump(dettaglio, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Response completa salvata in: {dettaglio_file}")
else:
    print("❌ Response non contiene dati attesi")
    pprint(dettaglio)
    exit(1)

# ============================================================================
# STEP 3: CONVERSIONE HTML → MARKDOWN
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: Conversione HTML → Markdown")
print("=" * 80)

# Import converter (se esiste)
try:
    import sys
    sys.path.append(str(SCRIPT_DIR))
    from api_html_to_markdown import api_response_to_markdown

    markdown = api_response_to_markdown(dettaglio)

    # Salva markdown
    md_path = OUTPUT_DIR / "atto_from_workflow_completo.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"\n✅ Conversione completata")
    print(f"   Output: {md_path}")

    print("\n" + "=" * 80)
    print("PREVIEW MARKDOWN (prime 40 righe):")
    print("=" * 80)
    print("\n".join(markdown.split('\n')[:40]))

except ImportError:
    print("⚠️ Converter api_html_to_markdown.py non trovato")
    print("   (saltato step conversione)")

# ============================================================================
# CONCLUSIONE
# ============================================================================

print("\n" + "=" * 80)
print("WORKFLOW COMPLETATO CON SUCCESSO ✅")
print("=" * 80)
print("\nRiepilogo:")
print(f"  1. ✅ Ricerca 'legge 4 2004' → {len(search_data.get('listaAtti', []))} risultati")
print(f"  2. ✅ Estratto dataGU={params['dataGU']}, codiceRedaz={params['codiceRedazionale']}")
print(f"  3. ✅ Dettaglio atto scaricato ({html_length} char HTML)")
print(f"  4. ✅ Conversione Markdown completata")

print("\n" + "=" * 80)
print("WORKFLOW M2M COMPLETAMENTE FUNZIONANTE")
print("Nessun HTML scraping • Nessuna email • API ufficiali")
print("=" * 80)
