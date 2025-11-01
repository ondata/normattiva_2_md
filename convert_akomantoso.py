import xml.etree.ElementTree as ET
import re
import sys
import argparse
import os
import requests
import tempfile
from datetime import datetime
from urllib.parse import urlparse

AKN_NAMESPACE = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}
GU_NAMESPACE = {'gu': 'http://www.gazzettaufficiale.it/eli/'}
ELI_NAMESPACE = {'eli': 'http://data.europa.eu/eli/ontology#'}

# Security constants
ALLOWED_DOMAINS = ['www.normattiva.it', 'normattiva.it']
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
DEFAULT_TIMEOUT = 30
VERSION = '1.4.2'

def extract_metadata_from_xml(root):
    """
    Extract metadata from Akoma Ntoso XML meta section.

    Returns dict with keys: dataGU, codiceRedaz, dataVigenza, url, url_xml
    Returns None for missing fields.
    """
    metadata = {}

    # Extract from meta section
    meta = root.find('.//akn:meta', AKN_NAMESPACE)
    if meta is None:
        return metadata

    # Extract codiceRedaz (eli:id_local) - try both eli and gu namespaces
    id_local = meta.find('.//eli:id_local', ELI_NAMESPACE)
    if id_local is None:
        id_local = meta.find('.//gu:id_local', GU_NAMESPACE)
    if id_local is not None and id_local.text:
        metadata['codiceRedaz'] = id_local.text.strip()

    # Extract dataGU (eli:date_document) - try both eli and gu namespaces
    date_doc = meta.find('.//eli:date_document', ELI_NAMESPACE)
    if date_doc is None:
        date_doc = meta.find('.//gu:date_document', GU_NAMESPACE)
    if date_doc is not None and date_doc.text:
        # Convert from YYYY-MM-DD to YYYYMMDD format
        try:
            date_obj = datetime.strptime(date_doc.text.strip(), '%Y-%m-%d')
            metadata['dataGU'] = date_obj.strftime('%Y%m%d')
        except ValueError:
            metadata['dataGU'] = date_doc.text.strip()

    # Extract dataVigenza from FRBRExpression date
    frbr_expr = meta.find('.//akn:FRBRExpression', AKN_NAMESPACE)
    if frbr_expr is not None:
        date_expr = frbr_expr.find('./akn:FRBRdate', AKN_NAMESPACE)
        if date_expr is not None and date_expr.get('date'):
            # Convert from YYYY-MM-DD to YYYYMMDD format
            try:
                date_obj = datetime.strptime(date_expr.get('date'), '%Y-%m-%d')
                metadata['dataVigenza'] = date_obj.strftime('%Y%m%d')
            except ValueError:
                metadata['dataVigenza'] = date_expr.get('date')

    # Construct URLs if we have the required metadata
    if metadata.get('dataGU') and metadata.get('codiceRedaz') and metadata.get('dataVigenza'):
        base_url = "https://www.normattiva.it/uri-res/N2Ls"
        urn = f"urn:nir:stato:legge:{metadata['dataGU'][:4]}-{metadata['dataGU'][4:6]}-{metadata['dataGU'][6:]};{metadata['codiceRedaz']}"
        metadata['url'] = f"{base_url}?{urn}"

        metadata['url_xml'] = f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={metadata['dataGU']}&codiceRedaz={metadata['codiceRedaz']}&dataVigenza={metadata['dataVigenza']}"

    return metadata

def validate_normattiva_url(url):
    """
    Validates that a URL is from the allowed normattiva.it domain and uses HTTPS.

    Args:
        url: URL string to validate

    Returns:
        bool: True if URL is valid and safe to fetch

    Raises:
        ValueError: If URL is invalid or not from allowed domain
    """
    try:
        parsed = urlparse(url)

        # Check scheme is HTTPS
        if parsed.scheme != 'https':
            raise ValueError(f"Solo HTTPS è consentito. URL fornito usa: {parsed.scheme}")

        # Check domain is in whitelist
        if parsed.netloc.lower() not in ALLOWED_DOMAINS:
            raise ValueError(f"Dominio non consentito: {parsed.netloc}. Domini permessi: {', '.join(ALLOWED_DOMAINS)}")

        return True

    except Exception as e:
        raise ValueError(f"URL non valido: {e}")

def sanitize_output_path(path, allow_absolute=True):
    """
    Sanitizes an output file path to prevent path traversal attacks.

    Args:
        path: File path to sanitize
        allow_absolute: Whether to allow absolute paths

    Returns:
        str: Sanitized absolute path

    Raises:
        ValueError: If path attempts traversal outside working directory
    """
    if not path:
        raise ValueError("Path non può essere vuoto")

    # Convert to absolute path
    abs_path = os.path.abspath(path)

    # Get working directory
    cwd = os.path.abspath(os.getcwd())

    # If not allowing absolute paths or path is outside cwd, reject
    if not allow_absolute and not abs_path.startswith(cwd):
        raise ValueError(f"Path fuori dalla directory di lavoro: {path}")

    # Check for common path traversal patterns
    if '..' in path or path.startswith('/etc') or path.startswith('/sys'):
        raise ValueError(f"Path non sicuro rilevato: {path}")

    return abs_path

def generate_front_matter(metadata):
    """
    Generate YAML front matter from metadata dictionary.

    Returns front matter string or empty string if no metadata available.
    """
    if not metadata:
        return ""

    # Collect non-None values
    front_matter_data = {}
    for key in ['url', 'url_xml', 'dataGU', 'codiceRedaz', 'dataVigenza']:
        if metadata.get(key):
            front_matter_data[key] = metadata[key]

    if not front_matter_data:
        return ""

    # Generate YAML front matter
    lines = ["---"]
    for key, value in front_matter_data.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")  # Empty line after front matter
    lines.append("")  # Additional empty line before content

    return "\n".join(lines)

def parse_chapter_heading(heading_text):
    """
    Separa heading che contengono sia Capo che Sezione.
    Pattern: "Capo [N] [TITOLO] Sezione [N] [Titolo]"
    Gestisce anche il caso in cui Sezione sia dentro modifiche legislative (( ))
    Returns: {'type': 'capo'|'sezione'|'both', 'capo': ..., 'sezione': ...}
    """
    # Cerca pattern "Capo" e "Sezione"
    has_capo = re.search(r'\bCapo\s+[IVX]+', heading_text, re.IGNORECASE)
    has_sezione = re.search(r'\bSezione\s+[IVX]+', heading_text, re.IGNORECASE)
    
    result = {'type': None, 'capo': None, 'sezione': None}
    
    # Caso 1: Contiene sia Capo che Sezione
    if has_capo and has_sezione:
        result['type'] = 'both'
        split_pos = has_sezione.start()
        capo_text = heading_text[:split_pos].strip()
        sezione_text = heading_text[split_pos:].strip()
        
        result['capo'] = format_heading_with_separator(capo_text)
        result['sezione'] = format_heading_with_separator(sezione_text)
    
    # Caso 2: Solo Capo
    elif has_capo:
        result['type'] = 'capo'
        result['capo'] = format_heading_with_separator(heading_text)
    
    # Caso 3: Solo Sezione
    elif has_sezione:
        result['type'] = 'sezione'
        result['sezione'] = format_heading_with_separator(heading_text)
    
    # Caso 4: Nessuno dei due (fallback)
    else:
        result['type'] = 'unknown'
        result['capo'] = format_heading_with_separator(heading_text)
    
    return result

def format_heading_with_separator(heading_text):
    """
    Formatta heading aggiungendo " - " dopo il numero romano.
    Es: "Capo I PRINCIPI GENERALI" -> "Capo I - PRINCIPI GENERALI"
    Gestisce anche modifiche legislative (( ))
    """
    # Estrai modifiche legislative se presenti
    legislative_prefix = ""
    legislative_suffix = ""
    text_to_format = heading_text

    # Se inizia con ((, estrai e processa il contenuto
    if text_to_format.startswith('((') and text_to_format.endswith('))'):
        text_to_format = text_to_format[2:-2].strip()
        legislative_prefix = "(("
        legislative_suffix = "))"

    # Pattern per Capo o Sezione
    pattern = r'^((?:Capo|Sezione)\s+[IVX]+)\s+(.+)$'
    match = re.match(pattern, text_to_format, re.IGNORECASE)

    if match:
        prefix = match.group(1)  # "Capo I" o "Sezione I"
        title = match.group(2)   # "PRINCIPI GENERALI"
        formatted = f"{prefix} - {title}"
        return f"{legislative_prefix}{formatted}{legislative_suffix}"

    return heading_text

def clean_text_content(element):
    """
    Extracts text from an element, handling inline formatting and removing specific tags.
    Also cleans up excessive whitespace and indentation.
    """
    text_parts = []
    if element is None:
        return ""

    # Process element's own text
    if element.text:
        text_parts.append(element.text)

    for child in element:
        # Handle inline formatting
        if child.tag.endswith('strong'):
            text_parts.append(f"**{clean_text_content(child)}**")
        elif child.tag.endswith('emphasis'): # Akoma Ntoso often uses 'emphasis' for italics
            text_parts.append(f"*{clean_text_content(child)}*")
        elif child.tag.endswith('ref'):
            # Extract text content of <ref> tags instead of ignoring them
            text_parts.append(clean_text_content(child))
        elif child.tag.endswith(('ins', 'del')):
            # For modifications, add double parentheses only if not already present
            inner_text = clean_text_content(child)
            # Check if the text already has double parentheses
            if inner_text.strip().startswith('((') and inner_text.strip().endswith('))'):
                text_parts.append(inner_text)
            else:
                text_parts.append(f"(({inner_text}))")
        elif child.tag.endswith('footnote'):
            # Handle footnotes - extract footnote content and create markdown footnote reference
            footnote_content = clean_text_content(child)
            if footnote_content:
                # Generate a simple footnote reference (simplified - in practice would need global counter)
                footnote_ref = f"[^{footnote_content[:10].replace(' ', '')}]"  # Simple hash-like ref
                text_parts.append(footnote_ref)

        else:
            text_parts.append(clean_text_content(child)) # Recursively get text from other children

        # Process tail text
        if child.tail:
            text_parts.append(child.tail)

    # Join all parts
    full_text = ''.join(text_parts)

    # Replace multiple spaces with a single space, and strip leading/trailing whitespace
    cleaned_text = re.sub(r'\s+', ' ', full_text).strip()

    return cleaned_text

def is_normattiva_url(input_str):
    """
    Verifica se l'input è un URL di normattiva.it

    Args:
        input_str: stringa da verificare

    Returns:
        bool: True se è un URL normattiva.it valido e sicuro
    """
    if not isinstance(input_str, str):
        return False

    # Check if it looks like a URL
    if not re.match(r'https?://(www\.)?normattiva\.it/', input_str, re.IGNORECASE):
        return False

    # Validate URL for security
    try:
        validate_normattiva_url(input_str)
        return True
    except ValueError:
        return False

def extract_params_from_normattiva_url(url, session=None, quiet=False):
    """
    Scarica la pagina normattiva e estrae i parametri necessari per il download

    Args:
        url: URL della norma su normattiva.it
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        tuple: (params dict, session)
    """
    if not quiet:
        print(f"Caricamento pagina {url}...", file=sys.stderr)

    if session is None:
        session = requests.Session()

    headers = {
        'User-Agent': f'Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8'
    }

    try:
        response = session.get(url, headers=headers, timeout=DEFAULT_TIMEOUT, verify=True)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel caricamento della pagina: {e}", file=sys.stderr)
        return None, session

    html = response.text

    # Estrai parametri dagli input hidden usando regex
    params = {}

    # Cerca atto.dataPubblicazioneGazzetta
    match_gu = re.search(r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html)
    if match_gu:
        # Converti da formato YYYY-MM-DD a YYYYMMDD
        date_str = match_gu.group(1).replace('-', '')
        params['dataGU'] = date_str

    # Cerca atto.codiceRedazionale
    match_codice = re.search(r'name="atto\.codiceRedazionale"[^>]*value="([^"]+)"', html)
    if match_codice:
        params['codiceRedaz'] = match_codice.group(1)

    # Cerca la data di vigenza dall'input visibile
    match_vigenza = re.search(r'<input[^>]*value="(\d{2}/\d{2}/\d{4})"[^>]*>', html)
    if match_vigenza:
        # Converti da formato DD/MM/YYYY a YYYYMMDD
        date_parts = match_vigenza.group(1).split('/')
        params['dataVigenza'] = f"{date_parts[2]}{date_parts[1]}{date_parts[0]}"
    else:
        # Usa data odierna se non trovata
        params['dataVigenza'] = datetime.now().strftime('%Y%m%d')

    if not all(k in params for k in ['dataGU', 'codiceRedaz', 'dataVigenza']):
        print("Errore: impossibile estrarre tutti i parametri necessari", file=sys.stderr)
        print(f"Parametri trovati: {params}", file=sys.stderr)
        return None, session

    return params, session

def download_akoma_ntoso(params, output_path, session=None, quiet=False):
    """
    Scarica il documento Akoma Ntoso usando i parametri estratti

    Args:
        params: dizionario con dataGU, codiceRedaz, dataVigenza
        output_path: percorso dove salvare il file XML
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        bool: True se il download è riuscito
    """
    url = f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={params['dataGU']}&codiceRedaz={params['codiceRedaz']}&dataVigenza={params['dataVigenza']}"

    if not quiet:
        print(f"Download Akoma Ntoso da: {url}", file=sys.stderr)

    if session is None:
        session = requests.Session()

    headers = {
        'User-Agent': f'Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
        'Referer': 'https://www.normattiva.it/'
    }

    try:
        response = session.get(url, headers=headers, timeout=DEFAULT_TIMEOUT, allow_redirects=True, verify=True)
        response.raise_for_status()

        # Check file size before processing
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > MAX_FILE_SIZE_BYTES:
            print(f"❌ Errore: file troppo grande ({int(content_length) / 1024 / 1024:.1f}MB). Massimo consentito: {MAX_FILE_SIZE_MB}MB", file=sys.stderr)
            return False

        # Verifica che sia XML
        if response.content[:5] == b'<?xml' or b'<akomaNtoso' in response.content[:500]:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            if not quiet:
                print(f"✅ File XML salvato in: {output_path}", file=sys.stderr)
            return True
        else:
            print(f"❌ Errore: la risposta non è un file XML valido", file=sys.stderr)
            # Salva comunque per debug
            debug_path = output_path + '.debug.html'
            with open(debug_path, 'wb') as f:
                f.write(response.content)
            print(f"   Risposta salvata in: {debug_path}", file=sys.stderr)
            return False

    except requests.RequestException as e:
        print(f"❌ Errore durante il download: {e}", file=sys.stderr)
        return False

def convert_akomantoso_to_markdown_improved(xml_file_path, markdown_file_path=None, metadata=None):
    try:
        # Check file size before parsing (XML bomb protection)
        file_size = os.path.getsize(xml_file_path)
        if file_size > MAX_FILE_SIZE_BYTES:
            print(f"Errore: file XML troppo grande ({file_size / 1024 / 1024:.1f}MB). Massimo consentito: {MAX_FILE_SIZE_MB}MB", file=sys.stderr)
            return False

        # Parse XML with defusedxml would be better, but using size limit for now
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Extract metadata from XML if not provided (for local files)
        if metadata is None:
            metadata = extract_metadata_from_xml(root)

        markdown_fragments = generate_markdown_fragments(root, AKN_NAMESPACE, metadata)
    except ET.ParseError as e:
        print(f"Errore durante il parsing del file XML: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"Errore: Il file XML '{xml_file_path}' non trovato.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Si è verificato un errore inatteso: {e}", file=sys.stderr)
        return False

    markdown_text = ''.join(markdown_fragments)

    if markdown_file_path is None:
        sys.stdout.write(markdown_text)
        return True

    try:
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        print(
            f"Conversione completata. Il file Markdown è stato salvato in '{markdown_file_path}'",
            file=sys.stderr,
        )
        return True
    except IOError as e:
        print(f"Errore durante la scrittura del file Markdown: {e}", file=sys.stderr)
        return False


def generate_markdown_fragments(root, ns, metadata=None):
    """Build the markdown fragments for a parsed Akoma Ntoso document."""

    fragments = []

    # Extract document title for later use
    doc_title_fragments = extract_document_title(root, ns)

    # Generate body content
    preamble_fragments = extract_preamble_fragments(root, ns)
    body_elements_fragments = extract_body_fragments(root, ns)

    body_fragments = []
    body_fragments.extend(preamble_fragments)
    body_fragments.extend(body_elements_fragments)

    # Join body content (NO downgrade - proper hierarchy from parsing)
    body_text = ''.join(body_fragments)

    # Add front matter if metadata is available
    if metadata:
        front_matter = generate_front_matter(metadata)
        if front_matter:
            fragments.append(front_matter)

    # Add document title as H1
    fragments.extend(doc_title_fragments)

    # Add downgraded body content
    fragments.append(body_text)

    return fragments


def generate_markdown_text(root, ns=AKN_NAMESPACE, metadata=None):
    """Return the Markdown rendering for the provided Akoma Ntoso root."""

    return ''.join(generate_markdown_fragments(root, ns, metadata))


def extract_document_title(root, ns):
    """Convert the `<docTitle>` element to a Markdown H1 if present."""

    doc_title_element = root.find('.//akn:docTitle', ns)
    if doc_title_element is not None and doc_title_element.text:
        return [f"# {doc_title_element.text.strip()}\n\n"]
    return []


def extract_preamble_fragments(root, ns):
    """Collect Markdown fragments representing the document preamble."""

    fragments = []
    preamble = root.find('.//akn:preamble', ns)
    if preamble is None:
        return fragments

    for element in preamble:
        if element.tag.endswith('formula') or element.tag.endswith('p'):
            text = clean_text_content(element)
            if text:
                fragments.append(f"{text}\n\n")
        elif element.tag.endswith('citations'):
            for citation in element.findall('./akn:citation', ns):
                text = clean_text_content(citation)
                if text:
                    fragments.append(f"{text}\n\n")
    return fragments


def extract_body_fragments(root, ns):
    """Traverse body nodes and delegate conversion to specialised handlers."""

    fragments = []
    body = root.find('.//akn:body', ns)
    if body is None:
        return fragments

    for element in body:
        fragments.extend(process_body_element(element, ns))
    return fragments


def process_body_element(element, ns):
    """Process a direct child of `<body>` producing Markdown fragments."""

    if element.tag.endswith('title'):
        return process_title(element, ns)
    if element.tag.endswith('part'):
        return process_part(element, ns)
    if element.tag.endswith('chapter'):
        return process_chapter(element, ns)
    if element.tag.endswith('article'):
        article_fragments = []
        process_article(element, article_fragments, ns, level=2)
        return article_fragments
    if element.tag.endswith('attachment'):
        return process_attachment(element, ns)
    return []


def process_chapter(chapter_element, ns):
    """
    Convert a chapter element to Markdown fragments with proper hierarchy.
    
    Handles XML structure where both Capo and Sezione are marked as <chapter>,
    with hierarchy information encoded in the heading text.
    
    Hierarchy:
    - Capo only: H2
    - Capo + Sezione: H2 (Capo), H3 (Sezione), H4 (Articles)
    - Sezione only: H3, H4 (Articles)
    """
    chapter_fragments = []
    article_level = 3  # Default level
    heading_element = chapter_element.find('./akn:heading', ns)
    
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        parsed = parse_chapter_heading(clean_heading)
        
        # Determine heading levels based on parsed structure
        if parsed['type'] == 'both':
            # Capo + Sezione: Capo is H2, Sezione is H3
            chapter_fragments.append(f"## {parsed['capo']}\n\n")
            chapter_fragments.append(f"### {parsed['sezione']}\n\n")
            article_level = 4  # Articles under sezione are H4
        
        elif parsed['type'] == 'capo':
            # Only Capo: H2
            chapter_fragments.append(f"## {parsed['capo']}\n\n")
            article_level = 3  # Articles directly under capo are H3
        
        elif parsed['type'] == 'sezione':
            # Only Sezione: H3 (assumes it's under a previous Capo)
            chapter_fragments.append(f"### {parsed['sezione']}\n\n")
            article_level = 4  # Articles under sezione are H4
        
        else:
            # Unknown/fallback
            chapter_fragments.append(f"## {parsed['capo']}\n\n")
            article_level = 3

    # Process child elements
    for child in chapter_element:
        if child.tag.endswith('section'):
            chapter_fragments.extend(process_section(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, chapter_fragments, ns, level=article_level)
    
    return chapter_fragments


def process_section(section_element, ns):
    """Convert a section element and its articles to Markdown fragments."""

    section_fragments = []
    heading_element = section_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        section_fragments.append(f"#### {clean_heading}\n\n")

    for article in section_element.findall('./akn:article', ns):
        process_article(article, section_fragments, ns, level=4)
    return section_fragments


def process_title(title_element, ns):
    """
    Convert a title element to Markdown H2 heading.
    Titles are top-level structural elements.
    """
    title_fragments = []
    heading_element = title_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        title_fragments.append(f"## {clean_heading}\n\n")

    # Process any nested content (chapters, articles, etc.)
    for child in title_element:
        if child.tag.endswith('chapter'):
            title_fragments.extend(process_chapter(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, title_fragments, ns, level=3)

    return title_fragments


def process_part(part_element, ns):
    """
    Convert a part element to Markdown fragments.
    Parts are major structural divisions, rendered as H3.
    """
    part_fragments = []
    heading_element = part_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        part_fragments.append(f"### {clean_heading}\n\n")

    # Process nested content (chapters, articles, etc.)
    for child in part_element:
        if child.tag.endswith('chapter'):
            part_fragments.extend(process_chapter(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, part_fragments, ns, level=3)

    return part_fragments


def process_attachment(attachment_element, ns):
    """
    Convert an attachment element to Markdown fragments.
    Attachments are rendered as a separate section.
    """
    attachment_fragments = []
    heading_element = attachment_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        attachment_fragments.append(f"### Allegato: {clean_heading}\n\n")
    else:
        attachment_fragments.append("### Allegato\n\n")

    # Process attachment content (similar to body processing)
    for child in attachment_element:
        if child.tag.endswith('chapter'):
            attachment_fragments.extend(process_chapter(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, attachment_fragments, ns, level=3)

    return attachment_fragments


def process_table(table_element, ns):
    """
    Convert an Akoma Ntoso table element to basic Markdown table format.
    This is a simplified implementation that extracts text content.
    """
    table_rows = []

    # Find all rows in the table
    rows = table_element.findall('.//akn:tr', ns)
    if not rows:
        return ""

    for row in rows:
        row_cells = []
        # Find all cells in this row (td or th)
        cells = row.findall('./akn:td', ns) + row.findall('./akn:th', ns)
        if not cells:
            continue

        for cell in cells:
            cell_text = clean_text_content(cell)
            # Escape pipe characters in cell content
            cell_text = cell_text.replace('|', '\\|')
            row_cells.append(cell_text)

        if row_cells:
            table_rows.append('| ' + ' | '.join(row_cells) + ' |')

    if not table_rows:
        return ""

    # Create markdown table with header separator
    markdown_table = '\n'.join(table_rows[:1])  # First row as header
    if len(table_rows) > 1:
        # Add separator row
        num_cols = table_rows[0].count('|') - 1
        separator = '| ' + ' | '.join(['---'] * num_cols) + ' |'
        markdown_table += '\n' + separator
        # Add remaining rows
        markdown_table += '\n' + '\n'.join(table_rows[1:])

    return markdown_table


def process_article(article_element, markdown_content_list, ns, level=2):
    article_num_element = article_element.find('./akn:num', ns)
    article_heading_element = article_element.find('./akn:heading', ns)

    if article_num_element is not None:
        article_num = article_num_element.text.strip()
        if article_heading_element is not None and article_heading_element.text:
            clean_article_heading = clean_text_content(article_heading_element)
            # Improved formatting: "Art. X - Title" format
            heading_prefix = "#" * level
            markdown_content_list.append(f"{heading_prefix} {article_num} - {clean_article_heading}\n\n")
        else:
            heading_prefix = "#" * level
            markdown_content_list.append(f"{heading_prefix} {article_num}\n\n")

    # Process paragraphs and lists within articles
    for child_of_article in article_element:
        if child_of_article.tag.endswith('paragraph'):
            para_num_element = child_of_article.find('./akn:num', ns)
            para_content_element = child_of_article.find('./akn:content', ns)
            para_list_element = child_of_article.find('./akn:list', ns)

            # Check if paragraph contains a list
            if para_list_element is not None:
                # Handle intro element in lists (like in Article 1)
                intro_element = para_list_element.find('./akn:intro', ns)
                if intro_element is not None:
                    intro_text = clean_text_content(intro_element)
                    if intro_text:
                        # Remove double dots from paragraph numbering
                        para_num = para_num_element.text.strip().rstrip('.')
                        markdown_content_list.append(f"{para_num}. {intro_text}\n\n")
                    elif intro_text:
                        markdown_content_list.append(f"{intro_text}\n\n")

                for list_item in para_list_element.findall('./akn:point', ns):
                    list_num_element = list_item.find('./akn:num', ns)
                    list_content_element = list_item.find('./akn:content', ns)

                    list_item_text = clean_text_content(list_content_element) if list_content_element is not None else ""

                    if list_num_element is not None:
                        markdown_content_list.append(f"- {list_num_element.text.strip()} {list_item_text}\n")
                    elif list_item_text:
                        markdown_content_list.append(f"- {list_item_text}\n")
                markdown_content_list.append("\n") # Add a newline after a list
            else:
                # Handle regular paragraph content
                paragraph_text = clean_text_content(para_content_element) if para_content_element is not None else ""

                # Remove the "------------" lines from the paragraph content
                lines = paragraph_text.split('\n')
                filtered_lines = [line for line in lines if not re.match(r'^-+$', line.strip())]
                paragraph_text = '\n'.join(filtered_lines).strip()

                # Remove duplicate number if present at the beginning of the paragraph text
                if para_num_element is not None:
                    num_to_remove = para_num_element.text.strip().rstrip('.')
                    # Regex to match the number followed by a period and optional space at the beginning of the string
                    pattern = r"^" + re.escape(num_to_remove) + r"\.?\s*"
                    paragraph_text = re.sub(pattern, "", paragraph_text, 1).strip()

                if para_num_element is not None and paragraph_text:
                    # Remove double dots from paragraph numbering and ensure single dot
                    para_num = para_num_element.text.strip().rstrip('.')
                    markdown_content_list.append(f"{para_num}. {paragraph_text}\n\n")
                elif paragraph_text:
                    # If no number but there's text, just append the text
                    markdown_content_list.append(f"{paragraph_text}\n\n")

        elif child_of_article.tag.endswith('list'):
            # Handle intro element in lists (like in Article 1)
            intro_element = child_of_article.find('./akn:intro', ns)
            if intro_element is not None:
                intro_text = clean_text_content(intro_element)
                if intro_text:
                    markdown_content_list.append(f"{intro_text}\n\n")

            for list_item in child_of_article.findall('./akn:point', ns):
                list_num_element = list_item.find('./akn:num', ns)
                list_content_element = list_item.find('./akn:content', ns)

                list_item_text = clean_text_content(list_content_element) if list_content_element is not None else ""

                if list_num_element is not None:
                    markdown_content_list.append(f"- {list_num_element.text.strip()} {list_item_text}\n")
                elif list_item_text:
                    markdown_content_list.append(f"- {list_item_text}\n")
            markdown_content_list.append("\n") # Add a newline after a list

        elif child_of_article.tag.endswith('table'):
            # Handle tables - convert to basic markdown table format
            table_markdown = process_table(child_of_article, ns)
            if table_markdown:
                markdown_content_list.append(table_markdown)
                markdown_content_list.append("\n")

        elif child_of_article.tag.endswith('quotedStructure'):
            # Handle quoted structures - wrap in markdown blockquote
            quoted_content = clean_text_content(child_of_article)
            if quoted_content:
                # Split into lines and add > prefix to each line
                lines = quoted_content.split('\n')
                quoted_lines = [f"> {line}" for line in lines if line.strip()]
                markdown_content_list.append('\n'.join(quoted_lines))
                markdown_content_list.append("\n")

def main():
    """
    Funzione principale che gestisce gli argomenti della riga di comando
    Supporta sia file XML locali che URL normattiva.it
    """
    parser = argparse.ArgumentParser(
        description='Converte documenti Akoma Ntoso in formato Markdown da file XML o URL normattiva.it',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Output a file
  python convert_akomantoso.py input.xml output.md
  python convert_akomantoso.py -i input.xml -o output.md

  # Output a stdout (default se -o omesso)
  python convert_akomantoso.py input.xml
  python convert_akomantoso.py input.xml > output.md
  python convert_akomantoso.py -i input.xml

  # Da URL normattiva.it (auto-detect)
  python convert_akomantoso.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md
  python convert_akomantoso.py "URL" > output.md
  python convert_akomantoso.py -i "URL" -o output.md

  # Mantenere XML scaricato da URL
  python convert_akomantoso.py "URL" output.md --keep-xml
  python convert_akomantoso.py "URL" --keep-xml > output.md
        """
    )

    # Version flag
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')

    # Argomenti posizionali (compatibilità con uso semplice)
    parser.add_argument('input', nargs='?',
                       help='File XML locale o URL normattiva.it')
    parser.add_argument('output', nargs='?',
                       help='File Markdown di output (default: stdout)')

    # Argomenti opzionali (per maggiore flessibilità)
    parser.add_argument('-i', '--input', dest='input_named',
                       help='File XML locale o URL normattiva.it')
    parser.add_argument('-o', '--output', dest='output_named',
                       help='File Markdown di output (default: stdout)')
    parser.add_argument('--keep-xml', action='store_true',
                       help='Mantieni file XML temporaneo dopo conversione da URL')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Modalità silenziosa: mostra solo errori')

    args = parser.parse_args()

    # Determina input e output
    input_source = args.input or args.input_named
    output_file = args.output or args.output_named

    # Sanitize output path if provided
    if output_file:
        try:
            output_file = sanitize_output_path(output_file)
        except ValueError as e:
            print(f"❌ Errore nel path di output: {e}", file=sys.stderr)
            sys.exit(1)

    # Valida che input sia specificato
    if not input_source:
        parser.error("Input richiesto.\n"
                    "Uso: python convert_akomantoso.py <input> [output.md]\n"
                    "oppure: python convert_akomantoso.py -i <input> [-o output.md]\n"
                    "Se output omesso, markdown va a stdout")

    # Auto-detect: URL o file locale?
    if is_normattiva_url(input_source):
        # Gestione URL
        quiet_mode = args.quiet or output_file is None  # Quiet when output to stdout
        if not quiet_mode:
            print(f"Rilevato URL normattiva.it: {input_source}", file=sys.stderr)

        # Validate URL for security
        try:
            validate_normattiva_url(input_source)
        except ValueError as e:
            print(f"❌ Errore validazione URL: {e}", file=sys.stderr)
            sys.exit(1)

        # Estrai parametri dalla pagina
        params, session = extract_params_from_normattiva_url(input_source, quiet=quiet_mode)
        if not params:
            print("❌ Impossibile estrarre parametri dall'URL", file=sys.stderr)
            sys.exit(1)

        if not quiet_mode:
            print(f"\nParametri estratti:", file=sys.stderr)
            print(f"  dataGU: {params['dataGU']}", file=sys.stderr)
            print(f"  codiceRedaz: {params['codiceRedaz']}", file=sys.stderr)
            print(f"  dataVigenza: {params['dataVigenza']}\n", file=sys.stderr)

        # Crea file XML temporaneo con tempfile module (più sicuro)
        temp_fd, xml_temp_path = tempfile.mkstemp(suffix=f"_{params['codiceRedaz']}.xml", prefix="akoma2md_")
        os.close(temp_fd)  # Close file descriptor, we'll write with requests

        # Scarica XML
        if not download_akoma_ntoso(params, xml_temp_path, session, quiet=quiet_mode):
            print("❌ Errore durante il download del file XML", file=sys.stderr)
            sys.exit(1)

        # Converti a Markdown
        if not quiet_mode:
            print(f"\nConversione in Markdown...", file=sys.stderr)

        # Prepare metadata dict for front matter
        metadata = {
            'dataGU': params['dataGU'],
            'codiceRedaz': params['codiceRedaz'],
            'dataVigenza': params['dataVigenza'],
            'url': input_source,  # The original URL
            'url_xml': f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={params['dataGU']}&codiceRedaz={params['codiceRedaz']}&dataVigenza={params['dataVigenza']}"
        }

        success = convert_akomantoso_to_markdown_improved(xml_temp_path, output_file, metadata)

        if success:
            if not quiet_mode:
                if output_file:
                    print(f"✅ Conversione completata: {output_file}", file=sys.stderr)
                else:
                    print(f"✅ Conversione completata (output a stdout)", file=sys.stderr)

            # Rimuovi XML temporaneo se non richiesto diversamente
            if not args.keep_xml:
                try:
                    os.remove(xml_temp_path)
                    if not quiet_mode:
                        print(f"File XML temporaneo rimosso", file=sys.stderr)
                except OSError as e:
                    print(f"Attenzione: impossibile rimuovere file temporaneo: {e}", file=sys.stderr)
            else:
                if not quiet_mode:
                    print(f"File XML mantenuto: {xml_temp_path}", file=sys.stderr)

            sys.exit(0)
        else:
            print("❌ Errore durante la conversione", file=sys.stderr)
            sys.exit(1)

    else:
        # Gestione file XML locale
        quiet_mode = args.quiet or output_file is None  # Quiet when output to stdout
        if not quiet_mode:
            if output_file:
                print(f"Conversione da file XML locale: '{input_source}' a '{output_file}'...", file=sys.stderr)
            else:
                print(f"Conversione da file XML locale: '{input_source}' (output a stdout)...", file=sys.stderr)
        success = convert_akomantoso_to_markdown_improved(input_source, output_file)

        if success and not quiet_mode:
            print("✅ Conversione completata con successo!", file=sys.stderr)
        elif not success:
            print("❌ Errore durante la conversione.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
