# Struttura URL Normattiva.it

Questa guida documenta la struttura degli URL per accedere alle norme su normattiva.it.

## Formato Base

```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:[tipo]:[data];[numero]
```

## Componenti URN

- **urn:nir:stato** - Prefisso standard per atti dello Stato italiano
- **[tipo]** - Tipologia dell'atto (vedi sotto)
- **[data]** - Data in formato `AAAA-MM-GG` (anno-mese-giorno)
- **[numero]** - Numero dell'atto

## Tipi di Atti Supportati

### Decreto Legge
```
urn:nir:stato:decreto.legge:AAAA-MM-GG;NNN
```
Esempio:
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2013-08-14;93
```

### Legge
```
urn:nir:stato:legge:AAAA-MM-GG;NNN
```
Esempio:
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53
```

### Decreto Legislativo
```
urn:nir:stato:decreto.legislativo:AAAA-MM-GG;NNN
```
Esempio:
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2006-01-24;36
```

### Costituzione
```
urn:nir:stato:costituzione:1947-12-27
```
Esempio:
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:costituzione:1947-12-27
```

## Modalità di Visualizzazione e Puntamento Articoli

### Modalità di Visualizzazione

Gli URL possono includere suffissi per specificare la versione e puntare a specifici articoli:

| Modalità | Sintassi | Descrizione |
|----------|----------|-------------|
| **Multivigente** (default) | Nessun suffisso | Mostra tutte le versioni nel tempo |
| **Originale** | `@originale` | Testo come pubblicato in GU |
| **Vigente corrente** | `!vig=` | Versione vigente alla data di consultazione |
| **Vigente a data specifica** | `!vig=AAAA-MM-GG` | Versione vigente alla data indicata |

### Puntamento agli Articoli

La sintassi `~artN` permette di posizionarsi su un articolo specifico:

```
~art2    # Posiziona sull'articolo 2
~art5    # Posiziona sull'articolo 5
```

### Combinazioni Sintassi

#### 1. Multivigente (default)
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180
```
Mostra l'atto multivigente, posizionato sul primo articolo.

#### 2. Multivigente + Articolo specifico
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180~art2
```
Mostra l'atto multivigente, posizionato sull'articolo 2.

#### 3. Versione Originale
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180@originale
```
Mostra l'atto nella versione originale pubblicata in GU.

#### 4. Versione Originale + Articolo
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180@originale~art2
```
Versione originale, posizionata sull'articolo 2.

#### 5. Vigente alla data di consultazione
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180!vig=
```
Mostra l'atto nella versione vigente oggi.

#### 6. Vigente alla data di consultazione + Articolo
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180~art2!vig=
```
Versione vigente oggi, posizionata sull'articolo 2.

#### 7. Vigente a data specifica
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180!vig=2009-11-10
```
Mostra l'atto nella versione vigente al 10 novembre 2009.

#### 8. Vigente a data specifica + Articolo
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180~art2!vig=2009-11-10
```
Versione vigente al 10/11/2009, posizionata sull'articolo 2.

### Articoli con Estensioni

Per articoli con estensioni (bis, ter, quater, etc.), omettere il trattino:

```
~art16bis          # Articolo 16-bis
~art16ter          # Articolo 16-ter
~art16quater       # Articolo 16-quater
```

#### Esempio completo:
```
https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-29;185~art16bis
```

#### Estensioni comuni degli articoli:

| N. | Estensione | Sintassi URN |
|----|------------|--------------|
| 2 | bis | `bis` |
| 3 | ter/tris | `ter` o `tris` |
| 4 | quater | `quater` |
| 5 | quinquies/quinques | `quinquies` o `quinques` |
| 6 | sexies | `sexies` |
| 7 | septies | `septies` |
| 8 | octies | `octies` |
| 9 | novies | `novies` |
| 10 | decies | `decies` |
| 20 | vices | `vices` |
| 30 | tricies | `tricies` |
| 40 | quadragies | `quadragies` |

**Nota**: Per l'elenco completo fino a 49, vedere la documentazione ufficiale normattiva.it.

## ⚠️ Avvertenze e Best Practices

### Ambiguità negli URN

Alcuni URN possono restituire risultati multipli a causa di incongruenze storiche:

**Esempio**: `urn:nir:stato:decreto.legge:2000-01-07;1` può restituire:
- Legge Costituzionale 17 gennaio 2000, n. 1
- Decreto-Legge 7 gennaio 2000, n. 1

**Raccomandazione**: Verificare sempre l'URL prima della pubblicazione o utilizzo automatizzato.

### Articoli Inesistenti

Se si specifica un articolo inesistente o errato, il sistema si posiziona automaticamente sul primo articolo dell'atto.

### Compatibilità con `normattiva2md`

Il comando `normattiva2md` supporta **tutti i formati** di URL normattiva.it:
- Multivigente, originale, vigente (con o senza data)
- Con o senza puntamento ad articoli specifici
- Articoli con estensioni (bis, ter, quater, etc.)
- Filtro per singolo articolo con opzione `--art`

Il download dell'XML Akoma Ntoso è indipendente dal puntamento all'articolo nell'URL: viene scaricato sempre l'atto completo (a meno di usare `--art`).

## Standard Implementati

Normattiva.it implementa due standard principali:

1. **URN:NIR** - Standard di naming uniforme per documenti normativi
   - Pubblicato in GU 262/2001
   - RFC 2141 per URN (Uniform Resource Name)

2. **XML:NIR** - Formato elettronico di rappresentazione (Akoma Ntoso)
   - Pubblicato in GU 102/2002

## Esempi Pratici con `normattiva2md`

### Esempi Base

```bash
# Decreto Legge 93/2013 (multivigente) - output a file
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2013-08-14;93" -o dl_93_2013.md

# Legge 53/2022 - output a stdout
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" > legge_53_2022.md

# Decreto Legislativo 36/2006 (versione vigente)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2006-01-24;36!vig=" -o dlgs_36_2006.md

# Costituzione
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:costituzione:1947-12-27" -o costituzione.md
```

### Esempi con Versioni Specifiche

```bash
# Versione originale (come pubblicato in GU)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180@originale" -o dl_180_2008_orig.md

# Vigente a data specifica (10 novembre 2009)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180!vig=2009-11-10" -o dl_180_2008_vig_2009.md
```

### Esempi con Puntamento Articoli

```bash
# Articolo 2 (multivigente) - URL include ~art2 (opzionale, scarica comunque tutto l'atto)
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180~art2" -o dl_180_art2.md

# Articolo 16-bis - URL include ~art16bis
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-29;185~art16bis" -o dl_185_art16bis.md

# Articolo 2, versione vigente a data specifica
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180~art2!vig=2009-11-10" -o dl_180_art2_vig2009.md

# Filtrare SOLO l'articolo 2 con --art (scarica solo quell'articolo)
normattiva2md --art 2 "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-10;180" -o dl_180_solo_art2.md

# Filtrare articolo 16-bis (input user-friendly, senza trattino)
normattiva2md --art 16bis "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2008-11-29;185" > art16bis.md
```

### Salvataggio XML

```bash
# Salva XML mantenendolo dopo conversione
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" -o legge_53.md --keep-xml

# Per salvare solo XML, reindirizzare e usare l'XML temporaneo
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" --keep-xml > /dev/null
# Il file XML rimane in formato: legge_AAAA_NNN.xml
```

## Note Tecniche

- I documenti sono scaricabili in formato XML (Akoma Ntoso) dal database
- Il comando `normattiva2md` estrae automaticamente i parametri dalla pagina HTML
- Non è necessario conoscere i parametri interni (dataGU, codiceRedaz, dataVigenza)
- Basta fornire l'URL completo della norma come argomento
- Output predefinito: stdout (permette piping e composizione con altri tool)
