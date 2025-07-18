#!/bin/bash

# Script di distribuzione per akoma2md
# Crea tutte le versioni distribuite del convertitore

set -e  # Exit on any error

echo "🔄 Akoma2MD - Script di Distribuzione Completa"
echo "=============================================="

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzioni helper
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Pulizia iniziale
print_step "1. Pulizia file temporanei..."
make clean > /dev/null 2>&1
print_success "Pulizia completata"

# 2. Verifica dipendenze
print_step "2. Verifica dipendenze..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 non trovato"
    exit 1
fi

if ! python3 -c "import PyInstaller" 2>/dev/null; then
    print_warning "PyInstaller non trovato, installazione..."
    pip3 install pyinstaller --break-system-packages || {
        print_error "Impossibile installare PyInstaller"
        exit 1
    }
fi
print_success "Dipendenze verificate"

# 3. Build eseguibile
print_step "3. Creazione eseguibile standalone..."
make build > /dev/null 2>&1
print_success "Eseguibile creato: dist/akoma2md"

# 4. Test funzionalità
print_step "4. Test funzionalità..."
if [ -f "20050516_005G0104_VIGENZA_20250130.xml" ]; then
    # Test eseguibile
    if ./dist/akoma2md 20050516_005G0104_VIGENZA_20250130.xml test_final.md > /dev/null 2>&1; then
        print_success "Test eseguibile: OK"
        rm -f test_final.md
    else
        print_error "Test eseguibile fallito"
        exit 1
    fi

    # Test script Python
    if python3 convert_akomantoso.py 20050516_005G0104_VIGENZA_20250130.xml test_final.md > /dev/null 2>&1; then
        print_success "Test script Python: OK"
        rm -f test_final.md
    else
        print_error "Test script Python fallito"
        exit 1
    fi
else
    print_warning "File di test XML non trovato, saltando test funzionali"
fi

# 5. Informazioni file
print_step "5. Informazioni sui file generati..."
echo ""
echo "📁 File disponibili per la distribuzione:"
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ ESEGUIBILI STANDALONE (non richiedono Python)              │"
echo "├─────────────────────────────────────────────────────────────┤"

if [ -f "dist/akoma2md" ]; then
    size=$(ls -lh dist/akoma2md | awk '{print $5}')
    echo "│ 🔧 dist/akoma2md                    Linux/WSL    ($size) │"
fi

echo "└─────────────────────────────────────────────────────────────┘"
echo ""
echo "📁 File sorgente (richiedono Python):"
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ SCRIPT PYTHON                                               │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ 🐍 convert_akomantoso.py             Script principale       │"
echo "│ 📦 setup.py                          Setup per pip install   │"
echo "│ 📖 README.md                         Documentazione          │"
echo "│ 📄 LICENSE                           Licenza MIT             │"
echo "│ 🔨 Makefile                          Build automation        │"
echo "└─────────────────────────────────────────────────────────────┘"

# 6. Istruzioni d'uso
echo ""
print_step "6. Istruzioni d'uso:"
echo ""
echo "🚀 ESEGUIBILE STANDALONE (Raccomandato):"
echo "   ./dist/akoma2md input.xml output.md"
echo ""
echo "🐍 SCRIPT PYTHON:"
echo "   python3 convert_akomantoso.py input.xml output.md"
echo ""
echo "📦 INSTALLAZIONE LOCALE (richiede virtual environment):"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -e ."
echo "   akoma2md input.xml output.md"
echo ""

# 7. Build completa (opzionale)
read -p "🔄 Vuoi creare anche i pacchetti di distribuzione (wheel/sdist)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "7. Creazione pacchetti di distribuzione..."
    make package > /dev/null 2>&1
    print_success "Pacchetti creati in dist/"

    echo ""
    echo "📦 Pacchetti aggiuntivi creati:"
    ls -la dist/*.whl dist/*.tar.gz 2>/dev/null | while read line; do
        echo "   $line"
    done
fi

echo ""
print_success "🎉 Distribuzione completata con successo!"
echo ""
echo "💡 Suggerimenti:"
echo "   • Per distribuire: copia dist/akoma2md su altri sistemi Linux"
echo "   • Per Windows: usa 'pyinstaller --onefile' su sistema Windows"
echo "   • Per macOS: usa 'pyinstaller --onefile' su sistema macOS"
echo "   • Il file è autocontenuto e non richiede Python installato"
echo ""
print_success "Pronto per l'uso! 🚀"
