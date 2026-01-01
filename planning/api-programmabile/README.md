# 📋 Piano: API Programmabile per normattiva2md

**Data**: 2025-12-04
**Stato**: COMPLETATO (2026-01-01)
**Obiettivo**: Aggiungere API Python usabile da notebook mantenendo 100% compatibilità CLI

## 🎯 Decisioni Architetturali

### Risposte Raccolte

1. **Use cases prioritari**: A, B, C, D
   - A: Conversione da URL
   - B: Conversione da XML locale
   - C: Ricerca + conversione
   - D: Solo ricerca

2. **Stile API**: **Opzione 3 - Misto**
   - Funzioni standalone per uso veloce
   - Classe `Converter` per uso avanzato

3. **Output conversioni**: **Opzione B - Oggetto**
   - `ConversionResult` con `markdown` + `metadata`

4. **Gestione errori**: **Ibrida**
   - Eccezioni per errori gravi (URL invalido, file non trovato)
   - None per errori soft (articolo non trovato, ricerca senza risultati)

5. **search_law()**: **Opzione B - Lista**
   - Restituisce lista di `SearchResult`

6. **API key**: **Opzione 3 - Parametro override ENV**
   - Default: usa `EXA_API_KEY` da environment
   - Opzionale: override con parametro

7. **Type hints**: **Sì**
   - Compatibile Python 3.7+ con `from __future__ import annotations`

8. **Logging**: **Modulo logging**
   - Invece di `print()` per la nuova API

9. **Async**: **Struttura per futuro async**
   - Codice organizzato per facilitare future versioni async
   - Non implementato ora, ma architettura pronta

10. **Notebook esempio**: **Sì**
    - Jupyter notebook dimostrativo in `examples/`

## 📁 Struttura Cartella Planning

```
planning/api-programmabile/
├── README.md                    # Questo file - overview
├── 01-architecture.md           # Design architetturale dettagliato
├── 02-api-specification.md      # Specifiche API complete
├── 03-models.md                 # Dataclasses e tipi
├── 04-exceptions.md             # Sistema eccezioni
├── 05-implementation-plan.md    # Piano implementazione per fasi
├── 06-examples.md               # Esempi codice
├── 07-documentation-plan.md     # Piano documentazione
└── 08-testing-strategy.md       # Strategia testing
```

## 🚀 Quick Links

- [Architettura](01-architecture.md) - Design patterns e principi
- [Specifiche API](02-api-specification.md) - Firma funzioni e comportamenti
- [Piano Implementazione](05-implementation-plan.md) - Roadmap per fasi
- [Esempi](06-examples.md) - Casi d'uso pratici

## 📊 Checklist Generale

### Fase 1: Core API
- [x] Exceptions (`src/normattiva2md/exceptions.py`)
- [x] Models (`src/normattiva2md/models.py`)
- [x] API Core (`src/normattiva2md/api.py`)
- [x] Init exports (`src/normattiva2md/__init__.py`)

### Fase 2: Testing
- [x] Test exceptions
- [x] Test models
- [x] Test API functions
- [x] Test Converter class
- [x] Test error handling

### Fase 3: Documentazione
- [x] Docstrings complete
- [x] README.md aggiornato
- [ ] `docs/notebook_examples.md` (TODO)
- [x] Type hints

### Fase 4: Esempi
- [ ] `examples/notebook_quickstart.ipynb` (TODO)
- [x] Script esempi in `examples/`

### Fase 5: Release
- [x] Version bump (2.1.0)
- [x] CHANGELOG/LOG.md
- [x] Test finale (15 test passati)
- [ ] PyPI release (pending)

## 🔗 Riferimenti

- Progetto: `/home/aborruso/git/idee/normattiva_2_md`
- Source: `src/normattiva2md/`
- Tests: `tests/`
- Docs: `docs/`
