#!/usr/bin/env bash
# Smoke test dal vivo della CLI installata (non quella del venv).
# Uso: smoke.sh [versione_attesa]
# Exit 0 solo se tutti i controlli passano. Con EXA_API_KEY assente i controlli
# di ricerca risultano SALTATI e l'exit è 2: lo smoke test non è completo.

set -u

BIN="${NORMATTIVA2MD_BIN:-$HOME/.local/bin/normattiva2md}"
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
XML="$REPO/test_data/20050516_005G0104_VIGENZA_20250130.xml"
URN="https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK" || exit 1

pass=0; fail=0; skip=0
ok()   { echo "PASS  $1"; pass=$((pass+1)); }
ko()   { echo "FAIL  $1 ($2)"; fail=$((fail+1)); }
check() { # nome, condizione già valutata (0/1), dettaglio
  if [ "$2" -eq 0 ]; then ok "$1"; else ko "$1" "$3"; fi
}
arts() { grep -cE '^#+ Art' "$1" 2>/dev/null || echo 0; }
redaz() { sed -n 's/^codiceRedaz: //p' "$1" 2>/dev/null | head -1; }

[ -x "$BIN" ] || { echo "FAIL  binario non trovato: $BIN"; exit 1; }

v="$("$BIN" --version 2>&1 | awk '{print $NF}')"
if [ -n "${1:-}" ]; then
  [ "$v" = "$1" ]; check "versione installata $v" $? "attesa $1"
else
  echo "INFO  versione installata $v"
fi

# File locale: output deterministico
"$BIN" "$XML" -o local.md >/dev/null 2>&1
[ "$(arts local.md)" -eq 121 ]; check "file XML locale: 121 articoli" $? "trovati $(arts local.md)"
n="$("$BIN" --no-notes "$XML" 2>/dev/null | grep -c AGGIORNAMENTO)"
[ "$n" -eq 0 ]; check "--no-notes: nessun AGGIORNAMENTO" $? "trovati $n"

# Da URL (normattiva.it)
"$BIN" "$URN:legge:2022;53" -o l53.md >/dev/null 2>&1
[ "$(redaz l53.md)" = "22G00062" ] && [ "$(arts l53.md)" -gt 0 ]
check "URL L. 53/2022" $? "codiceRedaz '$(redaz l53.md)', articoli $(arts l53.md)"

"$BIN" --art 3quater "$URN:legge:2004-01-09;4" -o art.md >/dev/null 2>&1
grep -q '^## Art. 3-quater' art.md 2>/dev/null; check "--art 3quater L. 4/2004" $? "articolo assente"

"$BIN" "https://www.normattiva.it/uri-res/N2Ls?urn%3Anir%3Astato%3Alegge%3A2004-01-09%3B4%21vig=" -o enc.md >/dev/null 2>&1
[ "$(redaz enc.md)" = "004G0015" ]; check "URN percent-encoded" $? "codiceRedaz '$(redaz enc.md)'"

"$BIN" "$URN:legge:2004-01-09;4!vig=2010-01-01" -o vig.md >/dev/null 2>&1
grep -q '^dataVigenza: 20100101' vig.md 2>/dev/null; check "vigenza storica !vig=2010-01-01" $? "dataVigenza diversa"

"$BIN" --provvedimenti "$URN:legge:2024;207" prov.md </dev/null >/dev/null 2>&1
rows="$(wc -l < 2024_207_provvedimenti.csv 2>/dev/null || echo 0)"
[ "$rows" -gt 1 ]; check "--provvedimenti L. 207/2024" $? "righe CSV $rows"

# Ricerca (Exa)
if [ -z "${EXA_API_KEY:-}" ]; then
  echo "SKIP  ricerca --search: EXA_API_KEY assente"; skip=$((skip+2))
else
  for pair in "legge stanca|004G0015" "decreto dignità|18G00112"; do
    q="${pair%|*}"; want="${pair#*|}"
    "$BIN" -s "$q" --auto-select -o s.md </dev/null >/dev/null 2>&1
    [ "$(redaz s.md)" = "$want" ]; check "--search \"$q\"" $? "codiceRedaz '$(redaz s.md)', atteso $want"
    rm -f s.md
  done
fi

echo "---"
echo "passati $pass, falliti $fail, saltati $skip"
[ "$fail" -gt 0 ] && exit 1
[ "$skip" -gt 0 ] && exit 2
exit 0
