## ADDED Requirements
### Requirement: Project Website Location
Il repository MUST contenere i file del sito in una cartella dedicata `site/` separata da altra documentazione di progetto.

#### Scenario: Sito separato da altri materiali
- **WHEN** un maintainer cerca il sito del progetto
- **THEN** trova i file HTML/CSS/asset in `site/` e non in `docs/`

### Requirement: GitHub Pages Publication
Il sito MUST essere pubblicato su GitHub Pages tramite un workflow che pubblica il contenuto di `site/` nel branch `gh-pages`.

#### Scenario: Pubblicazione automatica su gh-pages
- **WHEN** viene eseguito il workflow di pubblicazione
- **THEN** il contenuto di `site/` è sincronizzato nel branch `gh-pages`
