#!/bin/bash

# Script per testare la compatibilità con diverse tipologie di documenti Normattiva

echo "🧪 Test di Compatibilità Akoma2MD"
echo "=================================="

# Lista di documenti di test da Normattiva (diversi tipi)
TEST_DOCUMENTS=(
    # Decreto Legislativo (già testato)
    "005G0104"  # Codice Amministrazione Digitale

    # Costituzione
    "001R0001"  # Costituzione Italiana

    # Codici
    "004U0262"  # Codice Civile
    "000U1398"  # Codice Penale

    # Legge ordinaria
    "012G0257"  # Legge Privacy

    # Regolamento
    "021G0166"  # Regolamento GDPR
)

SUCCESS_COUNT=0
TOTAL_COUNT=${#TEST_DOCUMENTS[@]}

echo "📋 Testando $TOTAL_COUNT documenti..."
echo ""

for doc in "${TEST_DOCUMENTS[@]}"; do
    echo "🔄 Testing documento $doc..."

    # URL del file XML da Normattiva
    url="https://www.normattiva.it/do/atto/caricaAKN?codiceRedaz=${doc}"

    # Download (simulato - richiederebbe implementazione reale)
    echo "   📥 Download XML... (simulato)"

    # Test conversione
    if ./dist/akoma2md "test_${doc}.xml" "test_${doc}.md" 2>/dev/null; then
        echo "   ✅ Conversione riuscita"
        ((SUCCESS_COUNT++))
    else
        echo "   ❌ Conversione fallita"
    fi

    echo ""
done

echo "📊 Risultati:"
echo "   Successi: $SUCCESS_COUNT/$TOTAL_COUNT"
echo "   Percentuale: $(( SUCCESS_COUNT * 100 / TOTAL_COUNT ))%"

if [ $SUCCESS_COUNT -eq $TOTAL_COUNT ]; then
    echo "🎉 Tutti i test passati! Compatibilità ottima."
elif [ $SUCCESS_COUNT -ge $(( TOTAL_COUNT * 8 / 10 )) ]; then
    echo "✅ Buona compatibilità (80%+)"
else
    echo "⚠️  Compatibilità limitata - necessari miglioramenti"
fi
