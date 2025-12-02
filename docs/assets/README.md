# Assets - Immagini e Risorse

## Generare l'immagine Open Graph

### Metodo 1: Screenshot da Browser (Raccomandato)

1. Apri `og-image-generator.html` nel browser
2. Imposta zoom al 100% (Ctrl+0 o Cmd+0)
3. Premi F11 per fullscreen (o nascondi le istruzioni con il bottone)
4. Fai screenshot della card blu centrata (1200x630px)
   - **Windows**: Windows + Shift + S (Snipping Tool)
   - **Mac**: Cmd + Shift + 4 (seleziona area)
   - **Linux**: Screenshot app con selezione area
5. Salva come `og-image.png` in questa directory
6. Commit e push

### Metodo 2: Tool Online

Puoi anche usare servizi online come:
- [OG Image Generator](https://og-image.vercel.app/)
- [Cloudinary Social Card Generator](https://cloudinary.com/tools/social-cards)
- [Canva](https://www.canva.com/) (template 1200x630px)

### Metodo 3: Headless Browser (Automatico)

Se hai Node.js e Puppeteer:

```bash
npm install -g puppeteer screenshot-cli
screenshot-cli file://$(pwd)/og-image-generator.html og-image.png 1200x630
```

## Specifiche Immagine

- **Formato**: PNG (preferito) o JPG
- **Dimensioni**: 1200x630px (ratio 1.91:1)
- **Peso massimo**: < 5MB (consigliato < 1MB)
- **Colori**: RGB
- **Nome file**: `og-image.png`

## Test OG Tags

Dopo aver caricato l'immagine su GitHub Pages, testa con:

- **Facebook**: https://developers.facebook.com/tools/debug/
- **Twitter**: https://cards-dev.twitter.com/validator
- **LinkedIn**: https://www.linkedin.com/post-inspector/

## File Assets

```
assets/
├── README.md                  # Questo file
├── og-image-generator.html    # Generatore HTML per OG image
└── og-image.png              # Immagine OG finale (da creare)
```
