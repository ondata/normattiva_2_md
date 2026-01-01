#!/bin/bash
# Test dettaglio atto API con curl

# Directory relativa allo script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../output"
mkdir -p "$OUTPUT_DIR"

curl -X POST 'https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/atto/dettaglio-atto' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"dataGU":"2004-01-17","codiceRedazionale":"004G0015","formatoRichiesta":"V"}' \
  -o "$OUTPUT_DIR/dettaglio_response.json" \
  -w "\nStatus: %{http_code}\n"

echo ""
echo "=== Response preview ==="
head -50 "$OUTPUT_DIR/dettaglio_response.json"
