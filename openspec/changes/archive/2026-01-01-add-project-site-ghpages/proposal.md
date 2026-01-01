## Why
La pagina HTML del sito di progetto è mischiata in `docs/` con altri materiali, creando confusione e ostacolando la pubblicazione pulita del sito.

## What Changes
- Separare il sito in una cartella dedicata `site/`.
- Aggiungere un workflow GitHub Actions che pubblichi il sito su GitHub Pages tramite branch `gh-pages`.
- Aggiornare la documentazione per riflettere il nuovo percorso del sito.

## Impact
- Affected specs: project-website
- Affected code: struttura repository (`site/`), workflow GitHub Actions per Pages
