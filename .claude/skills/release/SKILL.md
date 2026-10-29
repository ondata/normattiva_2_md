---
name: release
description: Rilascia una nuova versione di normattiva2md - bump versione, LOG.md, test, reinstallazione e smoke test dal vivo della CLI installata, commit e tag, PyPI con twine, release GitHub, verifica CI dei binari e installazione da PyPI. Da usare quando l'utente chiede di rilasciare, pubblicare o fare una nuova versione.
disable-model-invocation: true
---

# Release di normattiva2md

Argomento opzionale: la versione (`2.1.17`) oppure `patch`/`minor`/`major`. Senza argomento: `patch`.

Ogni passo ha il suo controllo. Se un controllo fallisce ci si ferma e lo si dice: niente pubblicazione con un controllo rosso o saltato.

## 1. Stato di partenza

```bash
git status --short
git log --oneline "$(git describe --tags --abbrev=0)"..HEAD
```

- Si rilascia da `main`, allineato con `origin/main` (`git fetch` e confronto).
- Se non ci sono commit dopo l'ultimo tag e nessuna modifica da includere, non c'è niente da rilasciare: dirlo e fermarsi.
- Annotare i file modificati o non tracciati che **non** fanno parte del rilascio: restano fuori dal commit. Nel dubbio chiedere quali includere.

## 2. Test unitari

```bash
source .venv/bin/activate && make test
```

Controllo: `OK` e nessun `FAIL`. Poi `deactivate`.

## 3. Versione e LOG.md

- Nuova versione in **due** file: `pyproject.toml` (`version = "X.Y.Z"`) e `setup.py` (`version="X.Y.Z"`). Controllo: `grep -n 'X.Y.Z' pyproject.toml setup.py` restituisce due righe.
- `LOG.md`: voce in testa sotto `## AAAA-MM-GG` (data di oggi), titolo `### Fix vX.Y.Z: ...` o `### Feature vX.Y.Z: ...`, punti brevi presi dai commit dopo l'ultimo tag. Ogni punto su una riga sola.

## 4. Reinstallazione e smoke test della CLI installata

Lo smoke test va fatto sul binario installato, **mai** con il venv attivo: col venv attivo `normattiva2md` è quello editable del venv, con metadati vecchi.

```bash
deactivate 2>/dev/null; uv tool install . --reinstall
.claude/skills/release/scripts/smoke.sh X.Y.Z
```

Lo script usa `~/.local/bin/normattiva2md`, lavora in una cartella temporanea e controlla versione, file XML locale, `--no-notes`, conversione da URL, `--art`, URN codificato, vigenza storica, `--provvedimenti` e `--search` (L. 4/2004 per "legge stanca", DL 87/2018 per "decreto dignità").

- Exit `0`: tutto passato.
- Exit `1`: qualcosa è fallito. Ci si ferma.
- Exit `2`: ricerca saltata per `EXA_API_KEY` assente. Lo smoke test non è completo: chiedere all'utente se procedere comunque.

Se il rilascio introduce una funzione nuova, provarla anche a mano con la CLI installata e riportare il comando e l'esito.

## 5. Conferma prima di pubblicare

Da qui in poi le azioni sono pubbliche e non si annullano (una versione caricata su PyPI non si può ricaricare). Mostrare all'utente in un unico messaggio:

- versione;
- `git diff --cached --stat` dopo aver aggiunto i file del rilascio (`git add` con i percorsi espliciti, mai `git add -A`);
- il testo delle note di rilascio;

e attendere il via esplicito.

## 6. Commit, tag, push

```bash
git commit -m "<tipo>: <sintesi> (vX.Y.Z)"   # conciso, più le righe di attribuzione previste
git tag vX.Y.Z
git push && git push origin vX.Y.Z
```

## 7. PyPI

```bash
source .venv/bin/activate
rm -f dist/*
python3 setup.py sdist bdist_wheel
twine check dist/*.tar.gz dist/*.whl
twine upload dist/*.tar.gz dist/*.whl
deactivate
```

Controllo: `twine check` restituisce `PASSED` per entrambi i file, e l'upload stampa `https://pypi.org/project/normattiva2md/X.Y.Z/`.

## 8. Release GitHub

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<note>"
```

Note in italiano, nello stile delle precedenti (`gh release view` dell'ultima): sezione `## Fix` o `## Novità`, un punto per modifica, con il nome della funzione in grassetto e cosa cambia per chi usa la CLI.

## 9. Verifiche finali

- CI dei binari, avviata dal tag: `gh run list --limit 1` e poi `gh run watch <id> --exit-status`, da lanciare in background. Controllo: `Linux Binary`, `Windows Binary` e `Publish Release` con esito `success`.
- Installazione da PyPI: `uv tool install normattiva2md==X.Y.Z --reinstall --refresh` (se l'indice non è ancora aggiornato, riprovare dopo qualche decina di secondi) e poi `smoke.sh X.Y.Z`.

## 10. Resoconto

Riportare: versione, commit e tag, link PyPI, link della release, esito della CI, esito dello smoke test su PyPI, file lasciati fuori dal commit. Se un passo è stato saltato o è fallito, dirlo per primo.
