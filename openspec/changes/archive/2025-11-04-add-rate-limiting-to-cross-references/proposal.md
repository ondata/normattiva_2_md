## Why
When using `--with-references`, the tool makes multiple rapid requests to normattiva.it to download cited laws. This could potentially overwhelm the server or trigger rate limiting, especially when processing documents with many references. Adding a delay between requests ensures respectful usage of the service.

## What Changes
- Add a 1-second delay between each HTTP request to normattiva.it when `--with-references` is active
- Implement the delay using Python's `time.sleep()` function
- Apply the delay only during batch downloads in cross-reference mode, not affecting single document downloads

## Impact
- Affected specs: markdown-conversion (Cross-Reference Download Mode)
- Affected code: convert_akomantoso.py (convert_with_references function)
- Performance: Slightly slower batch processing (acceptable trade-off for respectful usage)
- User experience: No functional changes, just slower but more respectful downloads</content>
</xai:function_call"> 

Assistant: Ora creo il file tasks.md con i passi di implementazione. Dovrebbe essere una lista ordinata di task verificabili. Per questa modifica semplice, i task saranno:
1. Aggiungere l'import di time
2. Modificare la funzione convert_with_references per aggiungere il delay
3. Testare che funzioni correttamente

Dato che è una modifica semplice, non dovrebbe richiedere design.md. Ora creo tasks.md. Per una modifica semplice come questa, i task potrebbero essere:
1. Aggiungere import time
2. Aggiungere time.sleep(1) nel loop di download
3. Testare la funzionalità

Ma devo renderli più specifici e verificabili. Inoltre, devo includere test e validazione. 

Guardando le istruzioni, tasks.md dovrebbe essere una lista ordinata di piccoli task verificabili che consegnano progresso visibile all'utente, includendo validazione (test, tooling) e evidenziando dipendenze o lavoro parallelo. 

Per questa modifica:
1. Aggiungere import time
2. Modificare convert_with_references per aggiungere delay
3. Testare che il delay funzioni (forse con un test che misura il tempo)
4. Verificare che non rompa la funzionalità esistente

Procedo. 

<xai:function_call name="write">
<parameter name="filePath">openspec/changes/add-rate-limiting-to-cross-references/tasks.md