# 📚 Indice Documentazione API Programmabile

**Data creazione**: 2025-12-04
**Stato**: Pianificazione completa

---

## 📖 Documenti

### 🎯 Overview
- **[README.md](README.md)** - Introduzione e overview generale
- **[INDEX.md](INDEX.md)** - Questo file

### 🏗️ Architettura e Design
1. **[01-architecture.md](01-architecture.md)** - Design architetturale
   - Principi guida (Non-breaking, Separation of Concerns, DRY)
   - Struttura file (nuovi e modificati)
   - Pattern: gestione errori, logging, async-ready
   - Diagrammi di flusso

2. **[02-api-specification.md](02-api-specification.md)** - Specifiche API complete
   - Funzioni standalone: `convert_url()`, `convert_xml()`, `search_law()`
   - Classe `Converter` con tutti i metodi
   - Oggetti ritornati: `ConversionResult`, `SearchResult`
   - Eccezioni e gestione errori
   - Type hints

3. **[03-models.md](03-models.md)** - Dataclasses e modelli dati
   - `ConversionResult` - struttura e metodi
   - `SearchResult` - struttura
   - Properties e helper methods
   - Compatibilità Python 3.7+

4. **[04-exceptions.md](04-exceptions.md)** - Sistema eccezioni
   - Gerarchia completa
   - Strategia errori gravi vs soft
   - Pattern di utilizzo
   - Best practices messaggi errore

### 🚀 Implementazione
5. **[05-implementation-plan.md](05-implementation-plan.md)** - Piano implementazione
   - 6 fasi dettagliate con checklist
   - Timeline e durata stimata (14-21h totali)
   - Dipendenze tra fasi
   - Rischi e mitigazioni
   - Success criteria

### 💡 Esempi e Guide
6. **[06-examples.md](06-examples.md)** - Esempi codice completi
   - 11 esempi pratici
   - Pattern comuni
   - Tips & tricks
   - Notebook Jupyter examples

---

## 🗂️ Navigazione Veloce

### Per Use Case

**Voglio capire l'architettura:**
→ [01-architecture.md](01-architecture.md)

**Voglio vedere le API disponibili:**
→ [02-api-specification.md](02-api-specification.md)

**Voglio sapere cosa ritornano le funzioni:**
→ [03-models.md](03-models.md)

**Voglio gestire gli errori correttamente:**
→ [04-exceptions.md](04-exceptions.md)

**Voglio iniziare l'implementazione:**
→ [05-implementation-plan.md](05-implementation-plan.md)

**Voglio esempi pratici:**
→ [06-examples.md](06-examples.md)

---

## 📋 Quick Reference

### Decisioni Chiave

| Aspetto | Decisione |
|---------|-----------|
| **Stile API** | Misto: funzioni standalone + classe Converter |
| **Output** | Oggetto `ConversionResult` con markdown + metadata |
| **Errori** | Ibrido: eccezioni (gravi) + None (soft) |
| **Search** | Lista `SearchResult` ordinata per relevance |
| **API Key** | Parametro override ENV variable |
| **Type Hints** | Sì, con `from __future__ import annotations` |
| **Logging** | Modulo `logging` invece di `print()` |
| **Async** | Struttura preparata, implementazione futura |

### File da Creare

```
src/normattiva2md/
├── exceptions.py          # NUOVO
├── models.py              # NUOVO
├── api.py                 # NUOVO
└── __init__.py           # MODIFICARE

tests/
├── test_exceptions.py     # NUOVO
├── test_models.py         # NUOVO
└── test_api.py           # NUOVO

examples/
├── notebook_quickstart.ipynb  # NUOVO
├── basic_usage.py            # NUOVO
├── batch_processing.py       # NUOVO
└── error_handling.py         # NUOVO

docs/
└── notebook_examples.md      # NUOVO
```

### Fasi Implementazione

1. **Foundation** (1-2h) - Exceptions + Models
2. **Core API** (4-6h) - Funzioni standalone
3. **Converter Class** (3-4h) - Classe avanzata
4. **Documentation** (3-4h) - Docs + exports
5. **Examples** (2-3h) - Notebook + esempi
6. **Release** (1-2h) - Version bump + publish

**Totale**: 14-21 ore

---

## ✅ Checklist Generale

### Completamento Pianificazione
- [x] Definire architettura
- [x] Specificare API complete
- [x] Definire modelli dati
- [x] Definire sistema eccezioni
- [x] Creare piano implementazione
- [x] Scrivere esempi
- [x] Creare indice navigazione

### Prossimi Step
- [ ] Review pianificazione
- [ ] Approvazione design
- [ ] Start implementazione Fase 1
- [ ] ...

---

## 📞 Contatti e Note

**Progetto**: normattiva2md
**Repository**: https://github.com/ondata/normattiva_2_md
**Versione target**: 2.1.0
**Compatibilità**: 100% backward compatible con CLI esistente

---

## 🔄 Aggiornamenti

| Data | Documento | Modifiche |
|------|-----------|-----------|
| 2025-12-04 | Tutti | Creazione iniziale pianificazione |

