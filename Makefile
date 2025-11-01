# Makefile per akoma2md - Convertitore Akoma Ntoso to Markdown

.PHONY: help clean build install test package upload

# Variabili
PYTHON := python3
PIP := pip3
PACKAGE_NAME := akoma2md
SCRIPT_NAME := convert_akomantoso.py
MAIN_SCRIPT := convert_akomantoso.py

# Target di default
help:
	@echo "🔄 Akoma2MD - Convertitore Akoma Ntoso to Markdown"
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  help        - Mostra questo help"
	@echo "  clean       - Pulisce i file temporanei"
	@echo "  build       - Crea l'eseguibile con PyInstaller"
	@echo "  install     - Installa il package localmente"
	@echo "  test        - Esegue i test"
	@echo "  package     - Crea i pacchetti per la distribuzione"
	@echo "  upload      - Carica su PyPI (richiede credenziali)"
	@echo "  all         - Esegue clean, build, test e package"

# Pulizia dei file temporanei
clean:
	@echo "🧹 Pulizia file temporanei..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -f *.pyc
	rm -f *.pyo
	rm -f *.spec
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "✅ Pulizia completata"

# Build dell'eseguibile standalone
build: clean
	@echo "🔨 Creazione eseguibile standalone..."
	$(PYTHON) -m PyInstaller --onefile --name $(PACKAGE_NAME) $(MAIN_SCRIPT)
	@echo "✅ Eseguibile creato: dist/$(PACKAGE_NAME)"
	@echo "📊 Dimensione file:"
	@ls -lh dist/$(PACKAGE_NAME)

# Installazione locale del package
install:
	@echo "📦 Installazione locale del package..."
	$(PIP) install -e .
	@echo "✅ Package installato. Usa: $(PACKAGE_NAME) --help"

# Test di base
test:
	@echo "🧪 Esecuzione test..."
	@set -e; \
		echo "Test 1: Unittest"; \
		$(PYTHON) -m unittest discover -s tests; \
		if [ -f "20050516_005G0104_VIGENZA_20250130.xml" ]; then \
			echo "Test 2: Script Python"; \
			$(PYTHON) $(MAIN_SCRIPT) 20050516_005G0104_VIGENZA_20250130.xml test_output_python.md; \
			echo "Test 3: Eseguibile standalone"; \
			./dist/$(PACKAGE_NAME) 20050516_005G0104_VIGENZA_20250130.xml test_output_exe.md; \
			echo "Test 4: Comando installato"; \
			$(PACKAGE_NAME) 20050516_005G0104_VIGENZA_20250130.xml test_output_cmd.md; \
			echo "✅ Test di integrazione completati"; \
			echo "📊 File generati:"; \
			ls -la test_output_*.md; \
		else \
			echo "⚠️  File di test XML non trovato. Eseguiti solo gli unit test."; \
		fi

# Creazione pacchetti per la distribuzione
package: clean
	@echo "📦 Creazione pacchetti per la distribuzione..."
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "✅ Pacchetti creati:"
	@ls -la dist/

# Upload su PyPI (test)
upload-test: package
	@echo "📤 Upload su PyPI Test..."
	$(PYTHON) -m twine upload --repository testpypi dist/*

# Upload su PyPI (produzione)
upload: package
	@echo "📤 Upload su PyPI..."
	$(PYTHON) -m twine upload dist/*

# Build completa
all: clean build test package
	@echo ""
	@echo "🎉 Build completa terminata!"
	@echo "📊 File generati:"
	@ls -la dist/
	@echo ""
	@echo "🚀 Per usare l'eseguibile: ./dist/$(PACKAGE_NAME) input.xml output.md"
	@echo "📦 Per installare: make install"

# Verifica dipendenze
check-deps:
	@echo "🔍 Verifica dipendenze..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "❌ Python non trovato"; exit 1; }
	@command -v $(PIP) >/dev/null 2>&1 || { echo "❌ pip non trovato"; exit 1; }
	@$(PYTHON) -c "import PyInstaller" 2>/dev/null || { echo "❌ PyInstaller non installato. Esegui: pip install pyinstaller"; exit 1; }
	@echo "✅ Tutte le dipendenze sono presenti"

# Info sul progetto
info:
	@echo "ℹ️  Informazioni progetto:"
	@echo "  Nome: $(PACKAGE_NAME)"
	@echo "  Script: $(MAIN_SCRIPT)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  PyInstaller: $(shell $(PYTHON) -c 'import PyInstaller; print(PyInstaller.__version__)' 2>/dev/null || echo 'Non installato')"
	@echo "  Directory corrente: $(PWD)"

# Demo veloce
demo:
	@echo "🎬 Demo del convertitore..."
	@if [ -f "20050516_005G0104_VIGENZA_20250130.xml" ]; then \
		echo "Conversione con eseguibile..."; \
		./dist/$(PACKAGE_NAME) 20050516_005G0104_VIGENZA_20250130.xml demo_output.md; \
		echo "📄 Prime righe del file generato:"; \
		head -n 20 demo_output.md; \
	else \
		echo "⚠️  File XML di esempio non trovato"; \
	fi
