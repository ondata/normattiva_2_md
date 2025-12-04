# 📄 Executive Summary - API Programmabile normattiva2md

**Data**: 2025-12-04  
**Versione target**: 2.1.0  
**Effort stimato**: 14-21 ore  
**Compatibilità**: 100% backward compatible

---

## 🎯 Obiettivo

Trasformare normattiva2md da **solo CLI** a **CLI + API Python usabile da notebook** mantenendo compatibilità totale.

---

## 💡 Valore Aggiunto

### Prima (solo CLI)
```bash
normattiva2md "https://www.normattiva.it/..." output.md
```

### Dopo (CLI + API)
```python
# API semplice
from normattiva2md import convert_url
result = convert_url("https://www.normattiva.it/...")
print(result.markdown)

# Ricerca
from normattiva2md import search_law
results = search_law("legge stanca")

# Avanzato
from normattiva2md import Converter
conv = Converter(exa_api_key="...", quiet=True)
result = conv.search_and_convert("decreto dignità")
result.save("decreto.md")
```

---

## 🏗️ Design Principles

1. **Non-Breaking**: Zero breaking changes al CLI esistente
2. **Progressive Disclosure**: Semplice per casi comuni, potente per casi avanzati
3. **Pythonic**: Eccezioni, type hints, logging, dataclasses
4. **Future-Ready**: Struttura preparata per async

---

## 📦 Deliverables

### Codice

**Nuovi file:**
- `src/normattiva2md/exceptions.py` - Eccezioni custom
- `src/normattiva2md/models.py` - Dataclasses (ConversionResult, SearchResult)
- `src/normattiva2md/api.py` - API funzioni + classe Converter

**File modificati:**
- `src/normattiva2md/__init__.py` - Export API pubblica

### Test

- `tests/test_exceptions.py`
- `tests/test_models.py`
- `tests/test_api.py`

### Documentazione

- `README.md` - Sezione uso programmabile
- `docs/notebook_examples.md` - Guida completa esempi

### Esempi

- `examples/notebook_quickstart.ipynb` - Jupyter notebook
- `examples/basic_usage.py`
- `examples/batch_processing.py`
- `examples/error_handling.py`

---

## 🔑 Decisioni Chiave

| Aspetto | Scelta | Rationale |
|---------|--------|-----------|
| **Stile API** | Funzioni standalone + Classe Converter | Semplicità per uso veloce, potenza per batch |
| **Output** | Oggetto ConversionResult | Accesso a markdown + metadata + metodi helper |
| **Errori** | Eccezioni (gravi) + None (soft) | Pythonic per errori critici, graceful per soft |
| **Search** | Lista SearchResult | Visibilità tutte opzioni, accesso facile al best |
| **Type Hints** | Sì | IDE support, documentation, Python 3.7+ compatible |
| **Logging** | logging module | Standard Python, configurabile da utente |
| **Async** | Struttura preparata | Facile aggiungere in futuro senza breaking changes |

---

## 📋 Piano Implementazione

### Fase 1: Foundation (1-2h)
Crea exceptions.py e models.py con test

### Fase 2: Core API (4-6h)
Implementa convert_url(), convert_xml(), search_law()

### Fase 3: Converter Class (3-4h)
Classe avanzata con config persistente

### Fase 4: Documentation (3-4h)
Aggiorna README, crea docs/notebook_examples.md

### Fase 5: Examples (2-3h)
Jupyter notebook + script Python esempi

### Fase 6: Release (1-2h)
Version bump, changelog, publish PyPI

---

## ✅ Success Criteria

- [ ] Tutte le API documentate e testate
- [ ] Almeno 3 esempi funzionanti
- [ ] CLI funziona identicamente a prima
- [ ] Tutti i test passano (vecchi + nuovi)
- [ ] Documentazione completa
- [ ] Release su PyPI

---

## 🎬 Getting Started

1. **Review**: Leggi INDEX.md per navigare documentazione
2. **Approve**: Valida design in 01-architecture.md
3. **Implement**: Segui 05-implementation-plan.md fase per fase
4. **Test**: Esegui esempi da 06-examples.md
5. **Release**: Follow checklist Fase 6

---

## 📊 Metriche

**Documentazione pianificazione:**
- 8 file markdown dettagliati
- ~75KB documentazione tecnica
- 11 esempi codice completi
- 6 fasi implementazione con checklist

**Codice stimato da scrivere:**
- ~400 righe API core
- ~150 righe models
- ~100 righe exceptions  
- ~500 righe test
- ~200 righe esempi

**Totale**: ~1350 righe codice nuovo

---

## 🔗 Link Rapidi

- **[INDEX.md](INDEX.md)** - Navigazione completa
- **[01-architecture.md](01-architecture.md)** - Architettura
- **[02-api-specification.md](02-api-specification.md)** - Specifiche API
- **[05-implementation-plan.md](05-implementation-plan.md)** - Piano dettagliato
- **[06-examples.md](06-examples.md)** - Esempi pratici

---

## 💬 Q&A Rapido

**Q: Rompe il CLI esistente?**  
A: No, 100% compatibile. CLI continua a funzionare esattamente come prima.

**Q: Quanto tempo serve implementare?**  
A: 14-21 ore totali, dividibile in 6 fasi incrementali.

**Q: Serve aggiungere dipendenze?**  
A: No, usa solo librerie standard Python (typing, logging, dataclasses).

**Q: Compatibile con Python 3.7?**  
A: Sì, usa `from __future__ import annotations` per compatibility.

**Q: Supporta async?**  
A: Non ancora, ma architettura preparata per aggiungerlo facilmente in futuro.

**Q: Come gestisce gli errori?**  
A: Strategia ibrida - eccezioni per errori gravi (URL invalido), None per soft errors (articolo non trovato).

---

## 📞 Next Steps

1. ✅ **Pianificazione completa** - FATTO
2. ⏳ **Review e approvazione** - IN ATTESA
3. ⏹️ **Implementazione Fase 1** - DA INIZIARE
4. ⏹️ **Testing continuo** - DA INIZIARE
5. ⏹️ **Release 2.1.0** - DA PIANIFICARE

---

**Ready to proceed?** Start with [05-implementation-plan.md](05-implementation-plan.md) Fase 1!
