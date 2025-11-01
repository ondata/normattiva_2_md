# VERIFICATION_TASKS.md - Task di Verifica per l'Output Markdown

Questo documento elenca i task di verifica e i punti da controllare nell'output Markdown generato dal tool, al fine di assicurare la massima fedeltà al testo consolidato delle norme su Normattiva.it.

## Punti da Verificare nell'Output Markdown

### 1. Intestazioni "Capo" e "Sezione" ✅ COMPLETATO

- **Problema:** Le intestazioni come "Capo I PRINCIPI GENERALI Sezione I Definizioni" combinavano Capo e Sezione su un'unica riga, riducendo la leggibilità e perdendo la gerarchia.
- **Soluzione Implementata (2025-11-01):**
  - Aggiunte funzioni `parse_chapter_heading()` e `format_heading_with_separator()`
  - Gli heading vengono separati automaticamente in due livelli gerarchici
  - Formato: `## Capo I - TITOLO` + `### Sezione I - Titolo`
  - Gestione modifiche legislative `(( ))` negli heading
  - Test positivi su CAD, Codice Appalti
- **File modificato:** `convert_akomantoso.py:6-56,117-130`

### 2. Testo "0a) AgID" ✅ VERIFICATO - NON È PROBLEMA

- **Verifica (2025-11-01):** Il testo "0a) AgID: l'Agenzia per l'Italia digitale..." è effettivamente presente nella visualizzazione web ufficiale di normattiva.it
- **Conclusione:** Non è testo abrogato. È una lettera aggiunta dopo le lettere alfabetiche standard, numerata con "0" per distinguerla
- **Azione:** Nessuna modifica necessaria - il comportamento attuale è corretto

### 3. Testo Preambolo "Sulla proposta del Ministro..." ✅ VERIFICATO - NON È PROBLEMA

- **Verifica (2025-11-01):** Il testo "Sulla proposta del Ministro per l'innovazione e le tecnologie..." è presente nel Markdown generato per il CAD
- **Evidenza:** `grep -i "Sulla proposta" verification_cad.md` trova il testo
- **Conclusione:** Il preambolo è correttamente estratto e incluso nel Markdown
- **Azione:** Nessuna modifica necessaria

## Priorità

Si consiglia di affrontare i task nell'ordine elencato, partendo dalle modifiche più semplici e dirette per poi passare a quelle che richiedono un'analisi più approfondita della struttura del documento.
