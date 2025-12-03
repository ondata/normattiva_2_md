# ⚠️ DEPRECATION NOTICE / AVVISO DI DEPRECAZIONE

> **English**: This package (`akoma2md`) is deprecated. Please use [`normattiva2md`](https://pypi.org/project/normattiva2md/) instead.
> 
> **Italiano**: Questo pacchetto (`akoma2md`) è deprecato. Si prega di usare [`normattiva2md`](https://pypi.org/project/normattiva2md/) al suo posto.

---

## Migration / Migrazione

**Old / Vecchio:**
```bash
pip install akoma2md
```

**New / Nuovo:**
```bash
pip install normattiva2md
```

Both CLI commands (`akoma2md` and `normattiva2md`) are available in the new package.

Entrambi i comandi CLI (`akoma2md` e `normattiva2md`) sono disponibili nel nuovo pacchetto.

---

## Why the change? / Perché il cambiamento?

The package has been renamed to `normattiva2md` to better reflect its purpose and align with the project repository name. The new name is more descriptive and follows Python naming conventions.

Il pacchetto è stato rinominato in `normattiva2md` per riflettere meglio il suo scopo e allinearlo con il nome del repository del progetto. Il nuovo nome è più descrittivo e segue le convenzioni di denominazione Python.

---

## Full Documentation / Documentazione Completa

Please visit the new package page for full documentation:

Per la documentazione completa, visitare la pagina del nuovo pacchetto:

**📦 PyPI:** https://pypi.org/project/normattiva2md/

**📖 GitHub:** https://github.com/aborruso/normattiva_2_md

---

# normattiva2md

Convertitore da XML Akoma Ntoso (formato Normattiva.it) a Markdown, con funzionalità avanzate:

- ✅ Conversione da file XML locale o URL normattiva.it
- 🔍 Ricerca in linguaggio naturale con AI (Exa API)
- 🔗 Download automatico delle leggi citate con `--with-references`
- 📝 Generazione link markdown agli articoli citati con `--with-urls`
- 🎯 Estrazione di singoli articoli da URL specifici
- 🚀 Architettura modulare per facile manutenzione ed estensione

## Installation / Installazione

```bash
# Use the new package / Usa il nuovo pacchetto
pip install normattiva2md
```

## Quick Start / Avvio Rapido

```bash
# Convert from URL / Converti da URL
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-03-07;82" output.md

# Natural language search / Ricerca in linguaggio naturale
normattiva2md -s "codice amministrazione digitale" --auto-select -o output.md

# Download with references / Scarica con riferimenti
normattiva2md --with-references "URL" output_dir/
```

For more examples and documentation, visit the [main package page](https://pypi.org/project/normattiva2md/).

Per altri esempi e documentazione, visita la [pagina del pacchetto principale](https://pypi.org/project/normattiva2md/).

---

**Last update of `akoma2md`:** v2.0.19 (December 2025)

**Ultimo aggiornamento di `akoma2md`:** v2.0.19 (Dicembre 2025)

**Future updates will only be published to `normattiva2md`.**

**Gli aggiornamenti futuri saranno pubblicati solo su `normattiva2md`.**
