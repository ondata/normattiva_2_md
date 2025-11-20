# EUR-Lex API Documentation

## Overview

EUR-Lex provides access to European Union legal documents in multiple formats through various APIs and endpoints.

## Document Identification Systems

EUR-Lex uses three main identification systems:

1. **CELEX** (Communitatis Europeae LEX): Alphanumeric code (e.g., `32024L1385`)
   - Format: `[sector][year][type][number]`
   - Example: `32024L1385` = Directive 1385 of 2024

2. **ELI** (European Legislation Identifier): URI-based identifier
   - Format: `http://data.europa.eu/eli/{type}/{year}/{number}/{version}`
   - Example: `http://data.europa.eu/eli/dir/2024/1385/oj`

3. **Cellar ID**: Internal UUID in the Publications Office repository
   - Format: UUID (e.g., `51d63356-1968-11ef-a251-01aa75ed71a1`)

## Available APIs

### 1. XML Notice API (Metadata)

**Endpoint:**
```
https://eur-lex.europa.eu/legal-content/{LANGUAGE}/TXT/XML/?uri=CELEX:{CELEX_NUMBER}
```

**Example:**
```bash
curl "https://eur-lex.europa.eu/legal-content/EN/TXT/XML/?uri=CELEX:32024L1385"
```

**Returns:** XML notice with document metadata including:
- All available manifestations (formats)
- Languages available
- Citations and references
- Subject matter classifications
- Download URLs for all formats

### 2. Document Download API

#### Available Formats

1. **Formex XML** (`fmx4`): Structured XML format
   - Best for programmatic processing
   - Contains full document structure
   - URL pattern: `http://publications.europa.eu/resource/oj/{OJ_CODE}.{LANG}.fmx4.{FILENAME}.zip`

2. **XHTML** (`xhtml`): HTML format with semantic markup
   - Good for display and conversion
   - URL pattern: `http://publications.europa.eu/resource/oj/{OJ_CODE}.{LANG}.xhtml.{FILENAME}.html`

3. **PDF** (`pdfa2a`): Official authentic version
   - Legally binding format
   - URL pattern: `http://publications.europa.eu/resource/oj/{OJ_CODE}.{LANG}.pdfa2a.{FILENAME}.pdf`

#### Download Pattern

**Step 1: Get XML Notice**
```python
import urllib.request
celex = "32024L1385"
url = f"https://eur-lex.europa.eu/legal-content/EN/TXT/XML/?uri=CELEX:{celex}"
response = urllib.request.urlopen(url)
xml_notice = response.read().decode('utf-8')
```

**Step 2: Extract Download URLs from XML**
```python
import xml.etree.ElementTree as ET

root = ET.fromstring(xml_notice)

# Find Formex XML URL
for manif in root.findall('.//MANIFESTATION'):
    format_elem = manif.find('.//MANIFESTATION_TYPE/VALUE')
    if format_elem is not None and format_elem.text == 'fmx4':
        url_elem = manif.find('.//ITEM/URI/VALUE')
        if url_elem is not None:
            formex_url = url_elem.text
            print(f"Formex XML: {formex_url}")
```

**Step 3: Download and Extract**
```bash
# Download Formex ZIP
curl -sL "http://publications.europa.eu/resource/oj/L_202401385.ENG.fmx4.OJABA_L_202401385_ENG.fmx4.zip" \
  -o document.zip

# Extract
unzip document.zip
```

### 3. SPARQL Endpoint

**Endpoint:**
```
http://publications.europa.eu/webapi/rdf/sparql
```

**Example Query:**
```sparql
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX eli: <http://data.europa.eu/eli/ontology#>

SELECT ?work ?title ?date ?format
WHERE {
  ?work cdm:resource_legal_id_celex "32024L1385" .
  ?work cdm:work_date_document ?date .
  OPTIONAL { ?work cdm:work_title_expression ?title }
}
```

## Document Formats Comparison

| Format | Extension | Use Case | Structure | Processing |
|--------|-----------|----------|-----------|------------|
| Formex XML | `.fmx.xml` | Programmatic | High | Complex but precise |
| XHTML | `.xhtml` | Web display | Medium | Moderate |
| PDF | `.pdf` | Legal reference | None | OCR needed |

## Formex XML Structure

Formex (FORMats for European law EXchange) is the XML format used by EU Publications Office.

### Key Elements

```xml
<ACT>
  <TITLE>        <-- Campione delle particelle TARES con superficie Document title -->
  <PREAMBLE>     <-- Campione delle particelle TARES con superficie Preamble -->
  <ENACTING.TERMS>
    <DIVISION>   <-- Campione delle particelle TARES con superficie Chapters -->
      <ARTICLE>  <-- Campione delle particelle TARES con superficie Articles -->
        <PARAG>  <-- Campione delle particelle TARES con superficie Paragraphs -->
          <ALINEA> <-- Campione delle particelle TARES con superficie Text blocks -->
```

### Common Tags

- `<ARTICLE>`: Legislative article
- `<PARAG>`: Numbered paragraph
- `<ALINEA>`: Text paragraph
- `<LIST>`: Lists (ordered/unordered)
- `<TI.ART>`: Article title
- `<NO.PARAG>`: Paragraph number
- `<CONSID>`: Recital/Consideration

## Complete Example Workflow

```python
#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import io

def download_eurlex_document(celex, language='EN', format_type='fmx4'):
    """
    Download a EUR-Lex document in the specified format.
    
    Args:
        celex: CELEX number (e.g., '32024L1385')
        language: Language code (e.g., 'EN', 'IT', 'FR')
        format_type: 'fmx4', 'xhtml', or 'pdfa2a'
    
    Returns:
        Document content (bytes or str depending on format)
    """
    # Step 1: Get XML notice
    notice_url = f"https://eur-lex.europa.eu/legal-content/{language}/TXT/XML/?uri=CELEX:{celex}"
    
    with urllib.request.urlopen(notice_url) as response:
        xml_notice = response.read().decode('utf-8')
    
    # Step 2: Parse XML to find download URL
    root = ET.fromstring(xml_notice)
    
    download_url = None
    for expr in root.findall('.//EXPRESSION'):
        # Check if this is the right language
        lang_elem = expr.find(f'.//VALUE[@type="language"]')
        if lang_elem is None:
            continue
            
        if language.upper() not in lang_elem.text:
            continue
        
        # Find the right format
        for manif in expr.findall('.//MANIFESTATION'):
            fmt = manif.find('.//MANIFESTATION_TYPE/VALUE')
            if fmt is not None and fmt.text == format_type:
                url_elem = manif.find('.//ITEM/URI/VALUE')
                if url_elem is not None:
                    download_url = url_elem.text
                    break
        
        if download_url:
            break
    
    if not download_url:
        raise ValueError(f"Format {format_type} not found for language {language}")
    
    # Step 3: Download document (following redirects)
    with urllib.request.urlopen(download_url) as response:
        content = response.read()
    
    # Step 4: If ZIP, extract
    if format_type == 'fmx4':
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            # Return main document file
            files = [f for f in zf.namelist() if f.endswith('.fmx.xml') and 'toc' not in f and 'doc' not in f]
            if files:
                return zf.read(files[0]).decode('utf-8')
    
    return content

# Usage
doc = download_eurlex_document('32024L1385', 'EN', 'fmx4')
print(doc[:1000])
```

## Language Codes

- `BG` - Bulgarian
- `ES` - Spanish
- `CS` - Czech
- `DA` - Danish
- `DE` - German
- `ET` - Estonian
- `EL` - Greek
- `EN` - English
- `FR` - French
- `GA` - Irish
- `HR` - Croatian
- `IT` - Italian
- `LV` - Latvian
- `LT` - Lithuanian
- `HU` - Hungarian
- `MT` - Maltese
- `NL` - Dutch
- `PL` - Polish
- `PT` - Portuguese
- `RO` - Romanian
- `SK` - Slovak
- `SL` - Slovenian
- `FI` - Finnish
- `SV` - Swedish

## API Rate Limits

EUR-Lex does not publish official rate limits, but recommended practices:
- Implement reasonable delays between requests (1-2 seconds)
- Cache downloaded documents locally
- Use bulk download features when available
- Respect robots.txt

## References

- EUR-Lex Homepage: https://eur-lex.europa.eu
- ELI Specification: https://eur-lex.europa.eu/eli-register/about.html
- Formex Documentation: https://op.europa.eu/en/web/eu-vocabularies/formex
- SPARQL Endpoint: http://publications.europa.eu/webapi/rdf/sparql
