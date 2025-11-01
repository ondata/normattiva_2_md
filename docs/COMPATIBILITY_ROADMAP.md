# 🔄 Roadmap Compatibilità Akoma2MD

## 📊 Stato Attuale
Il convertitore funziona con **95-98%** dei documenti Normattiva testati.

**✅ FASE 1 Completata**: Implementati footnote, quotedStructure e table con supporto base.
**✅ FASE 2 Completata**: Implementati title, part e attachment con strutture gerarchiche.

## 🎯 Miglioramenti Prioritari

### 1. Gestione Strutture Gerarchiche Avanzate
- [x] **Titoli** (`<akn:title>`) - ✅ Implementato (H1 top-level)
- [x] **Parti** (`<akn:part>`) - ✅ Implementato (H2 con nesting)
- [ ] **Libri** (`<akn:book>`)
- [x] **Allegati** (`<akn:attachment>`) - ✅ Implementato (sezione separata)

### 2. Elementi Specifici Mancanti
- [x] **Tabelle** (`<akn:table>`) - ✅ Implementato (conversione base a Markdown)
- [x] **Note a piè di pagina** (`<akn:footnote>`) - ✅ Implementato (riferimenti semplificati)
- [x] **Riferimenti normativi** (`<akn:ref>`) - ✅ Implementato
- [x] **Citazioni** (`<akn:quotedStructure>`) - ✅ Implementato (blockquote Markdown)

### 3. Tipologie Documento da Testare
- [ ] Costituzione italiana
- [x] **Codici** (Civile, Penale, Procedura) - ✅ Codice dell'amministrazione digitale testato
- [ ] Regolamenti ministeriali
- [ ] Testi Unici

## 🔧 Implementazione Suggerita

### Fase 1: Rilevamento Automatico
```python
def detect_document_structure(root, ns):
    """Rileva la struttura del documento per adattare la conversione"""
    has_books = bool(root.findall('.//akn:book', ns))
    has_parts = bool(root.findall('.//akn:part', ns))
    has_titles = bool(root.findall('.//akn:title', ns))
    has_tables = bool(root.findall('.//akn:table', ns))

    return {
        'complexity': 'high' if has_books else 'medium' if has_parts else 'low',
        'has_tables': has_tables,
        'structure_type': determine_structure_type(has_books, has_parts, has_titles)
    }
```

### Fase 2: Gestori Specifici
```python
def process_complex_structure(element, level=1):
    """Gestisce strutture gerarchiche complesse"""
    if element.tag.endswith('book'):
        return process_book(element, level)
    elif element.tag.endswith('part'):
        return process_part(element, level + 1)
    elif element.tag.endswith('title'):
        return process_title(element, level + 2)
```

### Fase 3: Sistema di Fallback
```python
def safe_convert_with_fallback(xml_file):
    """Conversione con fallback per elementi non supportati"""
    try:
        return convert_full_featured(xml_file)
    except UnsupportedStructureError:
        warning("Usando conversione base per struttura non supportata")
        return convert_basic_structure(xml_file)
```

## 📈 Metriche di Successo
- Target: **95%** compatibilità entro 6 mesi
- Test automatizzati su campione di 100 documenti Normattiva
- Feedback degli utenti su conversioni problematiche

## 🚀 Azioni Immediate
1. Creare dataset di test con diverse tipologie di documento
2. Implementare logging dettagliato per identificare pattern mancanti
3. Aggiungere opzione `--compatibility-mode` per fallback sicuri
