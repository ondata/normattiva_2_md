# Workflow Conversione Gazzetta Ufficiale → Markdown

Analisi workflow per estendere API search con conversione markdown.

## Flusso Identificato

### 1. URL Iniziale
```
https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg
```

### 2. Click "Atto Completo"
Porta a:
```
https://www.gazzettaufficiale.it/atto/vediMenuHTML?atto.dataPubblicazioneGazzetta=2025-12-06&atto.codiceRedazionale=25A06635&tipoSerie=serie_generale&tipoVigenza=originario
```

Questa pagina mostra:
- Checkbox per selezionare articoli/allegati (default: tutti selezionati)
- Checkbox "INCLUDI NOTE" (default: non selezionato)
- Pulsante "Visualizza"

### 3. Click "Visualizza"
Porta a:
```
https://www.gazzettaufficiale.it/atto/stampa/serie_generale/originario
```

**Questa è la pagina finale** con testo completo in HTML puro.

## Struttura Pagina Finale

**URL**: `https://www.gazzettaufficiale.it/atto/stampa/serie_generale/originario`
**Title**: `*** ATTO COMPLETO ***`

### Contenuto
- Testo completo pulito (no navigation, no sidebar)
- Include tabelle (rilevate: 2 tabelle)
- No immagini
- Formattazione semplice

### Formato Dati

HTML con struttura:
```
TIPO_ATTO DATA

Titolo completo (numero_atto)

(GU n.X del GG-MM-AAAA)

[Testo preambolo...]

[Articoli...]

[Allegati...]
```

## Pattern URL

Da ELI ID si estrae:
- `dataPubblicazioneGazzetta`: dalla data nell'URL ELI
- `codiceRedazionale`: dall'ID nell'URL ELI
- `tipoSerie`: sempre `serie_generale` (per ora)
- `tipoVigenza`: sempre `originario` (per ora)

### Esempio Parsing
Da: `https://www.gazzettaufficiale.it/eli/id/2025/12/06/25A06635/sg`

Estrai:
- Data: `2025-12-06`
- Codice: `25A06635`

URL Atto Completo:
```
https://www.gazzettaufficiale.it/atto/vediMenuHTML?atto.dataPubblicazioneGazzetta=2025-12-06&atto.codiceRedazionale=25A06635&tipoSerie=serie_generale&tipoVigenza=originario
```

## Implementazione Proposta

### Step 1: Parser URL ELI
```python
def parse_eli_url(eli_url):
    """
    Estrae parametri da URL ELI formato:
    https://www.gazzettaufficiale.it/eli/id/YYYY/MM/DD/CODICE/sg
    """
    match = re.search(r'/eli/id/(\d{4})/(\d{2})/(\d{2})/([^/]+)/sg', eli_url)
    return {
        'data': f"{match.group(1)}-{match.group(2)}-{match.group(3)}",
        'codice': match.group(4)
    }
```

### Step 2: Costruzione URL Stampa
```python
def get_stampa_url(data, codice, include_note=False, selected_parts=None):
    """
    Costruisce URL per versione stampa con POST params.
    """
    # Se selected_parts=None, seleziona tutto (default)
    # Se include_note=True, aggiunge note
    
    base = "https://www.gazzettaufficiale.it/atto/stampa/serie_generale/originario"
    # POST params necessari per selezione
    return base
```

### Step 3: Download HTML
```python
def download_atto_completo(eli_url, include_note=False):
    """
    Scarica HTML atto completo.
    
    Returns:
        str: HTML contenuto atto
    """
    params = parse_eli_url(eli_url)
    
    # Step 1: GET vediMenuHTML (per session)
    session = requests.Session()
    menu_url = f"https://www.gazzettaufficiale.it/atto/vediMenuHTML?atto.dataPubblicazioneGazzetta={params['data']}&atto.codiceRedazionale={params['codice']}&tipoSerie=serie_generale&tipoVigenza=originario"
    session.get(menu_url)
    
    # Step 2: POST stampa (con tutti articoli selezionati)
    stampa_url = "https://www.gazzettaufficiale.it/atto/stampa/serie_generale/originario"
    # POST data con selezioni
    response = session.post(stampa_url, data=...)
    
    return response.text
```

### Step 4: HTML → Markdown
```python
def html_to_markdown(html_content):
    """
    Converte HTML Gazzetta Ufficiale in Markdown.
    
    Gestisce:
    - Titolo atto
    - Preambolo
    - Articoli
    - Tabelle
    - Allegati
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Estrai struttura...
    # Converti in markdown...
    
    return markdown_text
```

## Prossimi Passi

1. Implementare parser URL ELI
2. Testare download HTML con requests/session
3. Analizzare struttura HTML dettagliata
4. Implementare converter HTML→MD
5. Integrare con gazzetta_api_client.py

## Note

- La sessione è necessaria (cookie tracking)
- Default: tutti articoli selezionati
- Tabelle in formato grafico (potrebbero essere immagini in alcuni casi)
- Possibile flag per includere/escludere note
