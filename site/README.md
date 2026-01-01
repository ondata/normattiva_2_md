# Landing Page normattiva2md

Questa directory contiene la landing page del progetto normattiva2md, costruita con Jekyll e Tailwind CSS.

## Struttura

```
site/
├── _config.yml              # Configurazione Jekyll
├── _layouts/
│   └── default.html         # Template principale con Tailwind CDN
├── assets/                  # Immagini e risorse statiche
├── index.md                 # Landing page content
├── Gemfile                  # Dipendenze Ruby (per test locale)
└── README.md               # Questo file
```

## Deployment su GitHub Pages

### Attivazione (solo la prima volta)

1. Vai su **Settings** del repository GitHub
2. Sezione **Pages** (nel menu laterale)
3. In **Source** seleziona **Deploy from a branch**:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
4. Clicca **Save**
5. Attendi qualche minuto per il deploy

GitHub Pages genererà automaticamente il sito all'URL:
**https://aborruso.github.io/normattiva_2_md/**

### Aggiornamenti

Ogni volta che fai push su `main`, il workflow GitHub Actions pubblica il sito su `gh-pages`.

## Test Locale (Opzionale)

Per testare il sito in locale prima del deploy:

```bash
# Installa dipendenze (solo la prima volta)
cd site
bundle install

# Avvia server Jekyll locale
bundle exec jekyll serve

# Apri nel browser
# http://localhost:4000/normattiva_2_md/
```

**Nota:** Il test locale non è obbligatorio. GitHub Pages funzionerà anche senza test locale.

## Stack Tecnologico

- **Jekyll 4.x**: Generatore di siti statici
- **Tailwind CSS 3.x**: Framework CSS via CDN
- **Prism.js**: Syntax highlighting per esempi di codice
- **Heroicons**: Icone SVG inline
- **Google Fonts (Inter)**: Typography

## Sezioni della Landing Page

1. **Hero**: Headline, CTA, quick install
2. **Features Grid**: 6 feature cards con icone
3. **Use Cases**: 4 scenari d'uso dettagliati
4. **Before/After Demo**: Confronto XML vs Markdown
5. **Installation**: Tab con pip/uv/source + esempi
6. **CTA Final**: Call-to-action finale

## Personalizzazione

### Colori
Modifica i colori in `_layouts/default.html`, sezione `tailwind.config`:

```javascript
colors: {
    primary: '#2563eb',    // Blu primario
    secondary: '#4f46e5',  // Indigo secondario
}
```

### Contenuto
Modifica `index.md` per aggiornare testo e sezioni.

### Layout
Modifica `_layouts/default.html` per cambiare header, footer o struttura HTML.

## Link Utili

- **Sito live**: https://aborruso.github.io/normattiva_2_md/
- **Repository**: https://github.com/ondata/normattiva_2_md
- **PyPI Package**: https://pypi.org/project/normattiva2md/
- **Documentazione**: https://github.com/ondata/normattiva_2_md/blob/main/README.md
