# project-website Specification

## Purpose
TBD - created by archiving change add-project-site-ghpages. Update Purpose after archive.
## Requirements
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

### Requirement: Project Website Content
Il sito MUST includere una sezione "Uso delle API" che descriva l'API programmabile (api.py, models.py, exceptions.py) e le funzioni standalone convert_url(), convert_xml(), search_law().

#### Scenario: Sezione API visibile
- **WHEN** un utente visita la landing page
- **THEN** trova una sezione dedicata con descrizione ed esempi d'uso delle API

