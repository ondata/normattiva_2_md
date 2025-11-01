# Product Requirements Document (PRD) - akoma2md

## 1. Introduzione

Questo documento descrive i requisiti per `akoma2md`, uno strumento a riga di comando progettato per convertire file XML conformi allo standard Akoma Ntoso in documenti Markdown leggibili. La finalità di base è produrre file facilmente condivisibili con modelli linguistici di grandi dimensioni (LLM) e altri sistemi di Intelligenza Artificiale, così da semplificare analisi, verifica e automazione dei contenuti normativi.

## 2. Scopo

L'obiettivo principale di `akoma2md` è fornire un modo semplice ed efficiente per convertire le norme pubblicate su `normattiva.it` (esportabili in formato Akoma Ntoso) in documenti Markdown. Questo formato testuale strutturato è ideale per essere utilizzato come input per Large Language Models (LLM) e sistemi di Intelligenza Artificiale, facilitando la creazione di bot specializzati basati su normative legali. In particolare, il progetto mira a rendere immediato il passaggio da XML complessi a Markdown pronto per essere incollato o caricato come contesto in strumenti LLM, riducendo tempi di preparazione e rischio di errori.

## 3. Funzionalità

### 3.1. Conversione da Akoma Ntoso a Markdown

*   **Input:** Il tool accetterà un file XML valido in formato Akoma Ntoso come input.
*   **Output:** Il tool genererà un file Markdown (`.md`) contenente il testo convertito.
*   **Gestione della Struttura:**
    *   **Titolo del Documento:** Estrazione e formattazione del titolo del documento (se presente) come intestazione di primo livello (`#`).
    *   **Preambolo:** Estrazione del contenuto del preambolo, inclusi paragrafi e citazioni.
    *   **Capitoli e Sezioni:** Riconoscimento e formattazione di capitoli e sezioni come intestazioni di secondo (`##`) e terzo livello (`###`) rispettivamente.
    *   **Articoli:** Riconoscimento e formattazione degli articoli. Il numero dell'articolo e l'intestazione (se presente) saranno combinati in un'intestazione di primo livello (`# Art. X - Titolo`).
    *   **Paragrafi:** Estrazione del contenuto dei paragrafi. I paragrafi numerati saranno formattati con il loro numero seguito da un punto (es. `1. Testo del paragrafo`).
    *   **Elenchi:** Riconoscimento e formattazione degli elenchi puntati o numerati all'interno di paragrafi o articoli. Gli elementi dell'elenco saranno preceduti da un trattino (`-`).
*   **Gestione della Formattazione Inline:**
    *   **Grassetto:** Il testo all'interno di tag `<strong>` sarà convertito in grassetto Markdown (`**testo**`).
    *   **Corsivo:** Il testo all'interno di tag `<em>` o `emphasis` sarà convertito in corsivo Markdown (`*testo*`).
    *   **Riferimenti (`<ref>`):** Il contenuto testuale dei tag `<ref>` sarà incluso nel testo convertito.
    *   **Modifiche (`<ins>`, `<del>`):** Il testo all'interno di tag `<ins>` (inserimenti) e `<del>` (cancellazioni) sarà racchiuso tra doppie parentesi `((testo))`.

### 3.2. Interfaccia a Riga di Comando (CLI)

*   **Argomenti Posizionali:** Supporto per l'input e l'output come argomenti posizionali (es. `akoma2md input.xml output.md`).
*   **Argomenti Nominati:** Supporto per argomenti nominati per input e output (es. `akoma2md -i input.xml -o output.md` o `akoma2md --input input.xml --output output.md`).
*   **Messaggi di Errore:** Fornire messaggi di errore chiari in caso di file mancanti, errori di parsing XML o problemi di scrittura del file.
*   **Messaggi di Successo:** Conferma della corretta conversione.

## 4. Requisiti Tecnici

*   **Linguaggio di Programmazione:** Python 3.7 o superiore.
*   **Dipendenze:** Il tool utilizzerà solo librerie standard di Python (es. `xml.etree.ElementTree`, `re`, `argparse`). Non sono previste dipendenze esterne.
*   **Compatibilità del Sistema Operativo:** Indipendente dal sistema operativo (testato su Linux, ma dovrebbe funzionare su Windows e macOS).

## 5. Requisiti di Performance

*   La conversione dovrebbe essere ragionevolmente veloce per file XML di dimensioni medie (fino a qualche MB).
*   L'utilizzo della memoria dovrebbe essere ottimizzato per evitare problemi con file di grandi dimensioni.

## 6. Requisiti di Usabilità

*   La CLI dovrebbe essere intuitiva e facile da usare, anche per utenti non esperti di programmazione.
*   I messaggi di aiuto (`--help`) dovrebbero essere chiari e fornire esempi d'uso.

## 7. Requisiti di Manutenzione

*   Il codice sorgente deve essere ben commentato e seguire le best practice di Python.
*   La struttura del progetto deve essere chiara e modulare per facilitare future modifiche e aggiunte.

## 8. Requisiti di Sicurezza

*   Il tool non dovrebbe eseguire codice arbitrario dai file XML di input.
*   Gestione sicura dei percorsi dei file per prevenire attacchi di directory traversal.

## 9. Futuri Miglioramenti (Out of Scope per la v1.0.0)

*   Supporto per ulteriori elementi Akoma Ntoso non ancora gestiti.
*   Opzioni di configurazione per la formattazione Markdown (es. stili di intestazione, prefissi per elenchi).
*   Validazione dello schema XML Akoma Ntoso.
*   Integrazione con sistemi di gestione documentale.
