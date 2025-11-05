import xml.etree.ElementTree as ET
import re
import sys
import argparse
import os
import requests
import tempfile
import time
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
VERSION = '2.0.7'

def load_env_file():
    """
    Load environment variables from .env file if it exists.
    This allows storing API keys locally without exporting them each time.
    """
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Split on first '=' to handle values with '='
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Remove quotes if present
                            if (value.startswith('"') and value.endswith('"')) or \
                               (value.startswith("'") and value.endswith("'")):
                                value = value[1:-1]
                            os.environ[key] = value
        except Exception as e:
            # Silently ignore errors loading .env file
            pass

# Load .env file at startup
load_env_file()

def build_permanent_url(dataGU, codiceRedaz, dataVigenza):
    """
    Build permanent URN-style URL with vigenza date.

    Args:
        dataGU: Publication date in YYYYMMDD format
        codiceRedaz: Redaction code
        dataVigenza: Vigenza date in YYYYMMDD format

    Returns:
        str: Permanent URL with URN and vigenza parameter
    """
    try:
        # Convert dates to YYYY-MM-DD format
        dataGU_formatted = f"{dataGU[:4]}-{dataGU[4:6]}-{dataGU[6:]}"
        dataVigenza_formatted = f"{dataVigenza[:4]}-{dataVigenza[4:6]}-{dataVigenza[6:]}"

        base_url = "https://www.normattiva.it/uri-res/N2Ls"
        urn = f"urn:nir:stato:legge:{dataGU_formatted};{codiceRedaz}!vig={dataVigenza_formatted}"

        return f"{base_url}?{urn}"
    except (IndexError, ValueError):
        return None

def extract_metadata_from_xml(root):
    """
    Extract metadata from Akoma Ntoso XML meta section.

    Returns dict with keys: dataGU, codiceRedaz, dataVigenza, url, url_xml, url_permanente
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

    # Extract canonical URN-NIR from FRBRWork
    frbr_work = meta.find('.//akn:FRBRWork', AKN_NAMESPACE)
    if frbr_work is not None:
        urn_alias = frbr_work.find('./akn:FRBRalias[@name="urn:nir"]', AKN_NAMESPACE)
        if urn_alias is not None and urn_alias.get('value'):
            metadata['urn_nir'] = urn_alias.get('value')

    # Construct URLs if we have the required metadata
    if metadata.get('dataGU') and metadata.get('codiceRedaz') and metadata.get('dataVigenza'):
        base_url = "https://www.normattiva.it/uri-res/N2Ls"
        urn = f"urn:nir:stato:legge:{metadata['dataGU'][:4]}-{metadata['dataGU'][4:6]}-{metadata['dataGU'][6:]};{metadata['codiceRedaz']}"
        metadata['url'] = f"{base_url}?{urn}"

        metadata['url_xml'] = f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={metadata['dataGU']}&codiceRedaz={metadata['codiceRedaz']}&dataVigenza={metadata['dataVigenza']}"

        # Build permanent URL using canonical URN-NIR with vigenza date
        if metadata.get('urn_nir'):
            # Convert dataVigenza to YYYY-MM-DD format for the URL
            try:
                vigenza_obj = datetime.strptime(metadata['dataVigenza'], '%Y%m%d')
                vigenza_formatted = vigenza_obj.strftime('%Y-%m-%d')
                metadata['url_permanente'] = f"{base_url}?{metadata['urn_nir']}!vig={vigenza_formatted}"
            except ValueError:
                # Fallback to old method if date conversion fails
                metadata['url_permanente'] = build_permanent_url(metadata['dataGU'], metadata['codiceRedaz'], metadata['dataVigenza'])
        else:
            # Fallback to old method if URN-NIR not found
            metadata['url_permanente'] = build_permanent_url(metadata['dataGU'], metadata['codiceRedaz'], metadata['dataVigenza'])

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
    for key in ['url', 'url_xml', 'url_permanente', 'dataGU', 'codiceRedaz', 'dataVigenza', 'article']:
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
    
    result = {'type': '', 'capo': '', 'sezione': ''}
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

def clean_text_content(element, cross_references=None):
    """
    Extracts text from an element, handling inline formatting and removing specific tags.
    Also cleans up excessive whitespace and indentation.

    Args:
        element: XML element to process
        cross_references: dict mapping Akoma URIs to local markdown file paths (optional)
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
            text_parts.append(f"**{clean_text_content(child, cross_references)}**")
        elif child.tag.endswith('emphasis'): # Akoma Ntoso often uses 'emphasis' for italics
            text_parts.append(f"*{clean_text_content(child, cross_references)}*")
        elif child.tag.endswith('ref'):
            # Extract text content of <ref> tags
            ref_text = clean_text_content(child, cross_references)
            href = child.get('href')

            # If cross_references is provided, try to create a markdown link
            if cross_references and href:
                # Se href è un URI Akoma, convertilo in URL normattiva.it
                if href.startswith('/akn/'):
                    normattiva_url = akoma_uri_to_normattiva_url(href)
                    if normattiva_url and normattiva_url in cross_references:
                        ref_text = f"[{ref_text}]({cross_references[normattiva_url]})"
                # Altrimenti, cerca direttamente nel mapping (per compatibilità)
                elif href in cross_references:
                    ref_text = f"[{ref_text}]({cross_references[href]})"

            text_parts.append(ref_text)
        elif child.tag.endswith(('ins', 'del')):
            # For modifications, add double parentheses only if not already present
            inner_text = clean_text_content(child, cross_references)
            # Check if the text already has double parentheses
            if inner_text.strip().startswith('((') and inner_text.strip().endswith('))'):
                text_parts.append(inner_text)
            else:
                text_parts.append(f"(({inner_text}))")
        elif child.tag.endswith('footnote'):
            # Handle footnotes - extract footnote content and create markdown footnote reference
            footnote_content = clean_text_content(child, cross_references)
            if footnote_content:
                # Generate a simple footnote reference (simplified - in practice would need global counter)
                footnote_ref = f"[^{footnote_content[:10].replace(' ', '')}]"  # Simple hash-like ref
                text_parts.append(footnote_ref)

        else:
            text_parts.append(clean_text_content(child, cross_references)) # Recursively get text from other children

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

def is_normattiva_export_url(url):
    """
    Verifica se l'URL è un URL di esportazione atto intero di normattiva.it

    Questi URL non sono supportati perché richiedono autenticazione per il download XML.
    Si consiglia di usare gli URL permalink (URN) invece.

    Args:
        url: URL da verificare

    Returns:
        bool: True se è un URL di esportazione atto intero
    """
    if not isinstance(url, str):
        return False

    # Check if it's an export URL
    return '/esporta/attoCompleto' in url and is_normattiva_url(url)

def parse_article_reference(url):
    """
    Estrae il riferimento all'articolo dall'URL se presente

    Args:
        url: URL da analizzare

    Returns:
        str or None: identificatore articolo (es. "art_3", "art_16bis") o None se non presente
    """
    if not isinstance(url, str):
        return None

    # Cerca pattern ~artN o ~artNbis etc.
    import re
    match = re.search(r'~art(\d+(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies|vices|tricies|quadragies)?)', url, re.IGNORECASE)
    if match:
        article_num = match.group(1)
        # Converti in formato eId: art_3, art_16bis, etc.
        return f"art_{article_num}"

    return None





def filter_xml_to_article(root, article_eid, ns):
    """
    Filtra il documento XML per estrarre solo l'articolo specificato

    Args:
        root: elemento root del documento XML
        article_eid: eId dell'articolo da estrarre (es. "art_3")
        ns: namespace Akoma Ntoso

    Returns:
        ET.Element or None: nuovo root con solo l'articolo, o None se articolo non trovato
    """
    # Trova l'articolo specifico
    article = root.find(f'.//akn:article[@eId="{article_eid}"]', ns)
    if article is None:
        return None

    # Crea un nuovo documento con solo l'articolo
    # Copia meta e altri elementi di livello superiore
    new_root = ET.Element(root.tag, root.attrib)

    # Copia namespace declarations
    for prefix, uri in ns.items():
        if prefix:
            new_root.set(f'xmlns:{prefix}', uri)
        else:
            new_root.set('xmlns', uri)

    # Copia meta section
    meta = root.find('.//akn:meta', ns)
    if meta is not None:
        new_root.append(meta)

    # Crea un nuovo body con solo l'articolo
    # Copy namespace from the original body
    original_body = root.find('.//akn:body', ns)
    if original_body is not None:
        body = ET.SubElement(new_root, original_body.tag, original_body.attrib)
    else:
        body = ET.SubElement(new_root, 'body')
    body.append(article)

    return new_root

def extract_params_from_normattiva_url(url, session=None, quiet=False):
    """
    Scarica la pagina normattiva e estrae i parametri necessari per il download

    Supporta URL permalink (URN) di normattiva.it visitando la pagina HTML
    e estraendo i parametri dagli input hidden.

    Gli URL di esportazione atto intero (/esporta/attoCompleto) non sono supportati
    perché richiedono autenticazione per il download XML. Usa gli URL permalink invece.

    Args:
        url: URL della norma su normattiva.it
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        tuple: (params dict, session)
    """
    # Reject export URLs as they require authentication
    if is_normattiva_export_url(url):
        print("❌ ERRORE: Gli URL di esportazione atto intero (/esporta/attoCompleto) non sono supportati", file=sys.stderr)
        print("   perché richiedono autenticazione per il download XML.", file=sys.stderr)
        print("   Usa invece gli URL permalink (URN) come:", file=sys.stderr)
        print("   https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:AAAA-MM-GG;N", file=sys.stderr)
        return None, session

    # For permalink URLs, visit the page and extract parameters from HTML
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

def convert_akomantoso_to_markdown_improved(xml_file_path, markdown_file_path=None, metadata=None, article_ref=None, cross_references=None, with_urls=False):
    try:
        # If with_urls is enabled, build cross-reference mapping from <ref> tags
        if with_urls:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            cross_references = cross_references or {}
            # Find all <ref> tags with href
            for ref in root.findall('.//akn:ref[@href]', AKN_NAMESPACE):
                href = ref.get('href')
                ref_text = ref.text.strip() if ref.text else href
                # Convert Akoma URI to Normattiva URL if needed
                if href and href.startswith('/akn/'):
                    normattiva_url = akoma_uri_to_normattiva_url(href)
                elif href and is_normattiva_url(href):
                    normattiva_url = href
                else:
                    normattiva_url = None
                if normattiva_url:
                    cross_references[href] = normattiva_url
        
        # Check file size before parsing (XML bomb protection)
        file_size = os.path.getsize(xml_file_path)
        if file_size > MAX_FILE_SIZE_BYTES:
            print(f"Errore: file XML troppo grande ({file_size / 1024 / 1024:.1f}MB). Massimo consentito: {MAX_FILE_SIZE_MB}MB", file=sys.stderr)
            return False

        # Parse XML with defusedxml would be better, but using size limit for now
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Filter XML to specific article if requested
        if article_ref:
            filtered_root = filter_xml_to_article(root, article_ref, AKN_NAMESPACE)
            if filtered_root is None:
                print(f"❌ Articolo '{article_ref}' non trovato nel documento", file=sys.stderr)
                return False
            root = filtered_root

        # Extract metadata from XML if not provided (for local files)
        if metadata is None:
            metadata = extract_metadata_from_xml(root)

        markdown_fragments = generate_markdown_fragments(root, AKN_NAMESPACE, metadata, cross_references)
    except ET.ParseError as e:
        print(f"Errore durante il parsing del file XML: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Errore: Il file '{xml_file_path}' non trovato.\n", file=sys.stderr)
        print("Per usare akoma2md, puoi:", file=sys.stderr)
        print("  1. Fornire un URL di normattiva.it:", file=sys.stderr)
        print("     akoma2md 'https://www.normattiva.it/uri-res/N2Ls?urn:...' output.md", file=sys.stderr)
        print("  2. Fornire il percorso di un file XML locale:", file=sys.stderr)
        print("     akoma2md percorso/al/file.xml output.md", file=sys.stderr)
        print("  3. Cercare una legge per nome con -s:", file=sys.stderr)
        print("     akoma2md -s 'legge stanca' output.md", file=sys.stderr)
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


def generate_markdown_fragments(root, ns, metadata=None, cross_references=None):
    """Build the markdown fragments for a parsed Akoma Ntoso document."""

    fragments = []

    # Extract document title for later use
    doc_title_fragments = extract_document_title(root, ns)

    # Generate body content
    preamble_fragments = extract_preamble_fragments(root, ns, cross_references)
    body_elements_fragments = extract_body_fragments(root, ns, cross_references)

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


def generate_markdown_text(root, ns=AKN_NAMESPACE, metadata=None, cross_references=None):
    """Return the Markdown rendering for the provided Akoma Ntoso root."""

    return ''.join(generate_markdown_fragments(root, ns, metadata, cross_references))


def extract_document_title(root, ns):
    """Convert the `<docTitle>` element to a Markdown H1 if present."""

    doc_title_element = root.find('.//akn:docTitle', ns)
    if doc_title_element is not None and doc_title_element.text:
        return [f"# {doc_title_element.text.strip()}\n\n"]
    return []


def extract_preamble_fragments(root, ns, cross_references=None):
    """Collect Markdown fragments representing the document preamble."""

    fragments = []
    preamble = root.find('.//akn:preamble', ns)
    if preamble is None:
        return fragments

    for element in preamble:
        if element.tag.endswith('formula') or element.tag.endswith('p'):
            text = clean_text_content(element, cross_references)
            if text:
                fragments.append(f"{text}\n\n")
        elif element.tag.endswith('citations'):
            for citation in element.findall('./akn:citation', ns):
                text = clean_text_content(citation, cross_references)
                if text:
                    fragments.append(f"{text}\n\n")
    return fragments


def extract_body_fragments(root, ns, cross_references=None):
    """Traverse body nodes and delegate conversion to specialised handlers."""

    fragments = []
    body = root.find('.//akn:body', ns)
    if body is None:
        return fragments

    for element in body:
        fragments.extend(process_body_element(element, ns, cross_references))
    return fragments


def process_body_element(element, ns, cross_references=None):
    """Process a direct child of `<body>` producing Markdown fragments."""

    if element.tag.endswith('title'):
        return process_title(element, ns, cross_references)
    if element.tag.endswith('part'):
        return process_part(element, ns, cross_references)
    if element.tag.endswith('chapter'):
        return process_chapter(element, ns, cross_references)
    if element.tag.endswith('article'):
        article_fragments = []
        process_article(element, article_fragments, ns, level=2, cross_references=cross_references)
        return article_fragments
    if element.tag.endswith('attachment'):
        return process_attachment(element, ns, cross_references)
    return []


def process_chapter(chapter_element, ns, cross_references=None):
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
        clean_heading = clean_text_content(heading_element, cross_references)
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
            chapter_fragments.extend(process_section(child, ns, cross_references))
        elif child.tag.endswith('article'):
            process_article(child, chapter_fragments, ns, level=article_level, cross_references=cross_references)

    return chapter_fragments


def process_section(section_element, ns, cross_references=None):
    """Convert a section element and its articles to Markdown fragments."""

    section_fragments = []
    heading_element = section_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        section_fragments.append(f"#### {clean_heading}\n\n")

    for article in section_element.findall('./akn:article', ns):
        process_article(article, section_fragments, ns, level=4, cross_references=cross_references)
    return section_fragments


def process_title(title_element, ns, cross_references=None):
    """
    Convert a title element to Markdown H2 heading.
    Titles are top-level structural elements.
    """
    title_fragments = []
    heading_element = title_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        title_fragments.append(f"## {clean_heading}\n\n")

    # Process any nested content (chapters, articles, etc.)
    for child in title_element:
        if child.tag.endswith('chapter'):
            title_fragments.extend(process_chapter(child, ns, cross_references))
        elif child.tag.endswith('article'):
            process_article(child, title_fragments, ns, level=3, cross_references=cross_references)

    return title_fragments


def process_part(part_element, ns, cross_references=None):
    """
    Convert a part element to Markdown fragments.
    Parts are major structural divisions, rendered as H3.
    """
    part_fragments = []
    heading_element = part_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        part_fragments.append(f"### {clean_heading}\n\n")

    # Process nested content (chapters, articles, etc.)
    for child in part_element:
        if child.tag.endswith('chapter'):
            part_fragments.extend(process_chapter(child, ns, cross_references))
        elif child.tag.endswith('article'):
            process_article(child, part_fragments, ns, level=3, cross_references=cross_references)

    return part_fragments


def process_attachment(attachment_element, ns, cross_references=None):
    """
    Convert an attachment element to Markdown fragments.
    Attachments are rendered as a separate section.
    """
    attachment_fragments = []
    heading_element = attachment_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        attachment_fragments.append(f"### Allegato: {clean_heading}\n\n")
    else:
        attachment_fragments.append("### Allegato\n\n")

    # Process attachment content (similar to body processing)
    for child in attachment_element:
        if child.tag.endswith('chapter'):
            attachment_fragments.extend(process_chapter(child, ns, cross_references))
        elif child.tag.endswith('article'):
            process_article(child, attachment_fragments, ns, level=3, cross_references=cross_references)

    return attachment_fragments


def process_table(table_element, ns, cross_references=None):
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
            cell_text = clean_text_content(cell, cross_references)
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


def process_article(article_element, markdown_content_list, ns, level=2, cross_references=None):
    article_num_element = article_element.find('./akn:num', ns)
    article_heading_element = article_element.find('./akn:heading', ns)

    if article_num_element is not None:
        article_num = article_num_element.text.strip()
        if article_heading_element is not None and article_heading_element.text:
            clean_article_heading = clean_text_content(article_heading_element, cross_references)
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
                    intro_text = clean_text_content(intro_element, cross_references)
                    if intro_text:
                        # Remove double dots from paragraph numbering
                        para_num = para_num_element.text.strip().rstrip('.')
                        markdown_content_list.append(f"{para_num}. {intro_text}\n\n")
                    elif intro_text:
                        markdown_content_list.append(f"{intro_text}\n\n")

                for list_item in para_list_element.findall('./akn:point', ns):
                    list_num_element = list_item.find('./akn:num', ns)
                    list_content_element = list_item.find('./akn:content', ns)

                    list_item_text = clean_text_content(list_content_element, cross_references) if list_content_element is not None else ""

                    if list_num_element is not None:
                        markdown_content_list.append(f"- {list_num_element.text.strip()} {list_item_text}\n")
                    elif list_item_text:
                        markdown_content_list.append(f"- {list_item_text}\n")
                markdown_content_list.append("\n") # Add a newline after a list
            else:
                # Handle regular paragraph content
                paragraph_text = clean_text_content(para_content_element, cross_references) if para_content_element is not None else ""

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
                intro_text = clean_text_content(intro_element, cross_references)
                if intro_text:
                    markdown_content_list.append(f"{intro_text}\n\n")

            for list_item in child_of_article.findall('./akn:point', ns):
                list_num_element = list_item.find('./akn:num', ns)
                list_content_element = list_item.find('./akn:content', ns)

                list_item_text = clean_text_content(list_content_element, cross_references) if list_content_element is not None else ""

                if list_num_element is not None:
                    markdown_content_list.append(f"- {list_num_element.text.strip()} {list_item_text}\n")
                elif list_item_text:
                    markdown_content_list.append(f"- {list_item_text}\n")
            markdown_content_list.append("\n") # Add a newline after a list

        elif child_of_article.tag.endswith('table'):
            # Handle tables - convert to basic markdown table format
            table_markdown = process_table(child_of_article, ns, cross_references)
            if table_markdown:
                markdown_content_list.append(table_markdown)
                markdown_content_list.append("\n")

        elif child_of_article.tag.endswith('quotedStructure'):
            # Handle quoted structures - wrap in markdown blockquote
            quoted_content = clean_text_content(child_of_article, cross_references)
            if quoted_content:
                # Split into lines and add > prefix to each line
                lines = quoted_content.split('\n')
                quoted_lines = [f"> {line}" for line in lines if line.strip()]
                markdown_content_list.append('\n'.join(quoted_lines))
                markdown_content_list.append("\n")

def lookup_normattiva_url(search_query, debug_json=False, auto_select=True):
    """
    Usa Exa AI API per cercare l'URL normattiva.it corrispondente alla query di ricerca.

    Args:
        search_query (str): La stringa di ricerca naturale (es. "legge stanca")
        debug_json (bool): Se True, mostra il JSON completo della risposta
        auto_select (bool): Se True, seleziona automaticamente il miglior risultato

    Returns:
        str or None: L'URL trovato, oppure None se non trovato o errore
    """
    import os
    import json

    try:
        # Verifica che l'API key di Exa sia configurata
        exa_api_key = os.getenv('EXA_API_KEY')
        if not exa_api_key:
            print("❌ EXA_API_KEY non trovata nelle variabili d'ambiente", file=sys.stderr)
            print("   Configura la variabile: export EXA_API_KEY='your-api-key'", file=sys.stderr)
            print("   Registrati su: https://exa.ai", file=sys.stderr)
            return None

        # Prepara la richiesta per Exa API
        url = "https://api.exa.ai/search"
        headers = {
            "x-api-key": exa_api_key,
            "Content-Type": "application/json"
        }

        # Payload per Exa API - filtro dominio tramite includeDomains
        payload = {
            "query": search_query,
            "includeDomains": ["normattiva.it"],
            "numResults": 5,
            "type": "auto"
        }

        # Effettua la chiamata API
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            print(f"❌ Errore Exa API (HTTP {response.status_code}): {response.text}", file=sys.stderr)
            return None

        # Parse JSON response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"❌ Errore nel parsing JSON da Exa API: {e}", file=sys.stderr)
            return None

        # Debug: mostra JSON completo se richiesto
        if debug_json:
            print(f"🔍 JSON completo da Exa API:", file=sys.stderr)
            print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
            print(file=sys.stderr)

        # Estrai risultati
        results = data.get('results', [])
        if not results:
            print(f"❌ Nessun risultato trovato per: {search_query}", file=sys.stderr)
            return None

        # Debug: mostra tutti i risultati ricevuti solo in debug mode
        if debug_json:
            print(f"🔍 Risultati ricevuti da Exa ({len(results)}):", file=sys.stderr)
            for i, result in enumerate(results, 1):
                url = result.get('url', 'N/A')
                title = result.get('title', 'N/A')[:100]  # Tronca titolo lungo
                score = result.get('score', 'N/A')
                print(f"  [{i}] URL: {url}", file=sys.stderr)
                print(f"      Titolo: {title}...", file=sys.stderr)
                print(f"      Score: {score}", file=sys.stderr)
                print(file=sys.stderr)

        # Logica di selezione migliorata: preferisci URL senza riferimenti ad articoli specifici
        valid_results = []
        query_lower = search_query.lower()

        # Controlla se l'utente vuole un articolo specifico
        import re
        # Riconosce: "articolo 7", "art 7", "art. 7", "articolo 16bis", etc.
        article_match = re.search(r'\b(?:articolo|art\.?|art)\s+(\d+(?:\s*(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies|vices|tricies|quadragies))?)\b', query_lower, re.IGNORECASE)
        requested_article = article_match.group(1).replace(' ', '') if article_match else None

        for i, result in enumerate(results):
            url = result.get('url')
            if url and is_normattiva_url(url):
                # Calcola un punteggio di preferenza
                preference_score = 0
                title = result.get('title', '').lower()

                # Bonus per il primo risultato (probabilmente il più rilevante)
                if i == 0:
                    preference_score += 3
                    # Bonus extra se non è richiesto un articolo specifico
                    if not requested_article:
                        preference_score += 10

                # Logica specifica per articoli richiesti
                if requested_article:
                    # Se l'utente vuole un articolo specifico, dai bonus agli URL che lo contengono
                    if f'~art{requested_article}' in url.lower():
                        preference_score += 20  # Bonus enorme per l'articolo esatto
                    elif '~art' in url:
                        preference_score -= 5  # Penalizza altri articoli
                else:
                    # Se l'utente NON vuole un articolo specifico, penalizza URL con articoli
                    if '~art' in url:
                        preference_score -= 10
                    else:
                        # Bonus extra per URL di leggi complete
                        preference_score += 2

                # Bonus per titoli che sembrano leggi complete
                if any(word in title for word in ['legge', 'decreto-legge', 'decreto legislativo']):
                    preference_score += 5

                # Bonus se il titolo contiene parole chiave della query
                query_words = set(query_lower.split())
                title_words = set(title.split())
                common_words = query_words.intersection(title_words)
                if common_words:
                    preference_score += len(common_words) * 2

                # Bonus extra se il titolo contiene la query quasi completa
                if query_lower in title or title in query_lower:
                    preference_score += 10

                # Penalizza titoli che sembrano articoli specifici (solo se non richiesti)
                if not requested_article and any(word in title for word in ['articolo', 'art.', 'comma']):
                    preference_score -= 5

                valid_results.append({
                    'url': url,
                    'title': result.get('title', ''),
                    'score': result.get('score', 0),
                    'preference_score': preference_score,
                    'rank': i + 1
                })

        if not valid_results:
            print(f"❌ Nessun URL normattiva.it valido trovato nei risultati", file=sys.stderr)
            return None

        # La logica di conversione automatica è ora integrata nel sistema di punteggio sopra

        # Se auto_select è False, mostra i risultati e chiedi all'utente di scegliere
        if not auto_select:
            print(f"🔍 Risultati trovati per: {search_query}", file=sys.stderr)
            print(f"Seleziona il numero del risultato desiderato (1-{len(valid_results)}), o 0 per annullare:", file=sys.stderr)
            for i, result in enumerate(valid_results, 1):
                print(f"  [{i}] {result['title'][:80]}...", file=sys.stderr)
                print(f"      URL: {result['url']}", file=sys.stderr)
                print(f"      Preferenza: {result['preference_score']}", file=sys.stderr)
                print(file=sys.stderr)

            try:
                choice = int(input("Scelta: ").strip())
                if choice == 0:
                    print("❌ Ricerca annullata dall'utente", file=sys.stderr)
                    return None
                elif 1 <= choice <= len(valid_results):
                    selected = valid_results[choice - 1]
                    print(f"✅ URL selezionato manualmente: {selected['url']}", file=sys.stderr)
                    return selected['url']
                else:
                    print(f"❌ Scelta non valida: {choice}", file=sys.stderr)
                    return None
            except (ValueError, EOFError):
                print("❌ Input non valido, ricerca annullata", file=sys.stderr)
                return None

        # Selezione automatica
        # Ordina per punteggio di preferenza decrescente, poi per score Exa
        valid_results.sort(key=lambda x: (x['preference_score'], x['score']), reverse=True)

        selected = valid_results[0]

        # Se l'utente non ha specificato un articolo ma il risultato selezionato è un articolo specifico,
        # convertilo automaticamente nella legge completa
        if not requested_article and '~art' in selected['url']:
            complete_url = selected['url'].split('~art')[0]
            if not debug_json:  # Solo in modalità non-debug mostra il messaggio di conversione
                print(f"🔄 Convertito URL articolo specifico in URL legge completa: {complete_url}", file=sys.stderr)
            selected['url'] = complete_url

        if debug_json:
            print(f"✅ URL selezionato automaticamente (preferenza: {selected['preference_score']}, score: {selected['score']}): {selected['url']}", file=sys.stderr)
            print(f"   Titolo: {selected['title']}", file=sys.stderr)

        return selected['url']

    except requests.exceptions.Timeout:
        print("❌ Timeout nella chiamata a Exa API", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione a Exa API: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Errore nella ricerca URL: {e}", file=sys.stderr)
        return None

def convert_with_references(url, output_dir=None, quiet=False, keep_xml=False, force_complete=False):
    """
    Scarica e converte una legge con tutte le sue riferimenti, creando una struttura di cartelle.

    Args:
        url: URL normattiva.it della legge principale
        quiet: se True, modalità silenziosa
        keep_xml: se True, mantiene i file XML temporanei
        force_complete: se True, forza download legge completa anche con URL articolo-specifico

    Returns:
        bool: True se il processo è completato con successo
    """
    try:
        # Estrai parametri dalla pagina principale
        if not quiet:
            print(f"🔍 Analisi legge principale: {url}", file=sys.stderr)

        params, session = extract_params_from_normattiva_url(url, quiet=quiet)
        if not params:
            print("❌ Impossibile estrarre parametri dalla legge principale", file=sys.stderr)
            return False

        # Crea nome cartella basato sui parametri della legge o usa directory specificata
        if output_dir:
            folder_path = os.path.abspath(output_dir)
        else:
            folder_name = f"{params['codiceRedaz']}_{params['dataGU']}"
            folder_path = os.path.join(os.getcwd(), folder_name)

        if not quiet:
            print(f"📁 Creazione struttura in: {folder_path}", file=sys.stderr)

        # Crea struttura cartelle
        os.makedirs(folder_path, exist_ok=True)
        refs_path = os.path.join(folder_path, "refs")
        os.makedirs(refs_path, exist_ok=True)

        # Scarica legge principale
        xml_temp_path = os.path.join(folder_path, f"{params['codiceRedaz']}.xml")
        if not download_akoma_ntoso(params, xml_temp_path, session, quiet=quiet):
            print("❌ Errore durante il download della legge principale", file=sys.stderr)
            return False

        # Estrai riferimenti dalla legge principale
        if not quiet:
            print(f"🔗 Estrazione riferimenti dalla legge principale...", file=sys.stderr)

        cited_urls = extract_cited_laws(xml_temp_path)
        if not quiet:
            print(f"📋 Trovati {len(cited_urls)} riferimenti unici", file=sys.stderr)

        # Scarica e converte legge principale
        main_md_path = os.path.join(folder_path, "main.md")
        metadata = {
            'dataGU': params['dataGU'],
            'codiceRedaz': params['codiceRedaz'],
            'dataVigenza': params['dataVigenza'],
            'url': url,
            'url_xml': f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={params['dataGU']}&codiceRedaz={params['codiceRedaz']}&dataVigenza={params['dataVigenza']}"
        }

        # Per ora, convertiamo la legge principale senza cross-references
        # Li aggiungeremo dopo aver scaricato tutte le leggi
        if not convert_akomantoso_to_markdown_improved(xml_temp_path, main_md_path, metadata):
            print("❌ Errore durante la conversione della legge principale", file=sys.stderr)
            return False

        # Scarica e converte leggi citate
        successful_downloads = 0
        failed_downloads = 0
        url_to_file_mapping = {}  # Mappa URL originali ai percorsi dei file

        for i, cited_url in enumerate(cited_urls, 1):
            if not quiet:
                print(f"📥 [{i}/{len(cited_urls)}] Download legge citata: {cited_url}", file=sys.stderr)

            try:
                # Estrai parametri dalla URL citata
                cited_params, cited_session = extract_params_from_normattiva_url(cited_url, quiet=True)
                if not cited_params:
                    if not quiet:
                        print(f"⚠️  Impossibile estrarre parametri da: {cited_url}", file=sys.stderr)
                    failed_downloads += 1
                    continue

                # Crea nome file per la legge citata
                cited_filename = f"{cited_params['codiceRedaz']}_{cited_params['dataGU']}.md"
                cited_md_path = os.path.join(refs_path, cited_filename)

                # Mappa l'URL originale al percorso del file
                url_to_file_mapping[cited_url] = f"refs/{cited_filename}"

                # Scarica XML temporaneo per la legge citata
                cited_xml_temp = os.path.join(folder_path, f"temp_{cited_params['codiceRedaz']}.xml")
                if download_akoma_ntoso(cited_params, cited_xml_temp, cited_session, quiet=True):
                    # Converti a markdown
                    cited_metadata = {
                        'dataGU': cited_params['dataGU'],
                        'codiceRedaz': cited_params['codiceRedaz'],
                        'dataVigenza': cited_params['dataVigenza'],
                        'url': cited_url,
                        'url_xml': f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={cited_params['dataGU']}&codiceRedaz={cited_params['codiceRedaz']}&dataVigenza={cited_params['dataVigenza']}"
                    }

                    if convert_akomantoso_to_markdown_improved(cited_xml_temp, cited_md_path, cited_metadata):
                        successful_downloads += 1
                        if not quiet:
                            print(f"✅ Convertita: {cited_filename}", file=sys.stderr)
                    else:
                        failed_downloads += 1
                        if not quiet:
                            print(f"❌ Errore conversione: {cited_filename}", file=sys.stderr)

                    # Rimuovi XML temporaneo
                    if not keep_xml:
                        try:
                            os.remove(cited_xml_temp)
                        except OSError:
                            pass
                else:
                    failed_downloads += 1
                    if not quiet:
                        print(f"❌ Errore download: {cited_url}", file=sys.stderr)

            except Exception as e:
                failed_downloads += 1
                if not quiet:
                    print(f"❌ Errore elaborazione {cited_url}: {e}", file=sys.stderr)

            # Rate limiting: wait 1 second between requests to be respectful to normattiva.it
            if not quiet:
                print(f"⏳ Attesa 1 secondo prima del prossimo download...", file=sys.stderr)
            time.sleep(1)

        # Costruisci mapping cross-references basato sugli URL originali
        cross_references = build_cross_references_mapping_from_urls(url_to_file_mapping)

        # Se abbiamo cross-references, riconverti la legge principale con i link
        if cross_references:
            if not quiet:
                print(f"🔗 Aggiunta collegamenti incrociati alla legge principale...", file=sys.stderr)
            if not convert_akomantoso_to_markdown_improved(xml_temp_path, main_md_path, metadata, cross_references=cross_references):
                print("⚠️  Avviso: riconversione con collegamenti fallita, mantengo versione senza link", file=sys.stderr)

        # Crea file indice
        create_index_file(folder_path, params, cited_urls, successful_downloads, failed_downloads)

        # Rimuovi XML principale se non richiesto
        if not keep_xml:
            try:
                os.remove(xml_temp_path)
            except OSError:
                pass

        if not quiet:
            print(f"\n✅ Completato! {successful_downloads} leggi citate scaricate, {failed_downloads} fallite", file=sys.stderr)
            if cross_references:
                print(f"🔗 Collegamenti incrociati aggiunti: {len(cross_references)} riferimenti", file=sys.stderr)
            print(f"📂 Struttura creata in: {folder_path}", file=sys.stderr)

        return True

    except Exception as e:
        print(f"❌ Errore durante il processo con riferimenti: {e}", file=sys.stderr)
        return False


def extract_cited_laws(xml_file_path):
    """
    Estrae tutti gli URL delle leggi citate da un file XML Akoma Ntoso.

    Args:
        xml_file_path: percorso al file XML

    Returns:
        set: insieme di URL unici delle leggi citate
    """
    cited_urls = set()

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Trova tutti i tag <ref> con href
        for ref in root.findall('.//akn:ref[@href]', AKN_NAMESPACE):
            href = ref.get('href')
            if href and href.startswith('/akn/'):
                # Converti URI Akoma Ntoso in URL normattiva.it
                url = akoma_uri_to_normattiva_url(href)
                if url and is_normattiva_url(url):
                    cited_urls.add(url)

    except ET.ParseError as e:
        print(f"Errore parsing XML per riferimenti: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Errore estrazione riferimenti: {e}", file=sys.stderr)

    return cited_urls


def akoma_uri_to_normattiva_url(akoma_uri):
    """
    Converte un URI Akoma Ntoso in URL normattiva.it.

    Args:
        akoma_uri: URI Akoma Ntoso (es. /akn/it/act/legge/stato/2003-07-29/229/!main)

    Returns:
        str or None: URL normattiva.it corrispondente o None se conversione fallisce
    """
    try:
        # Esempio: /akn/it/act/legge/stato/2003-07-29/229/!main
        # Diventa: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2003-07-29;229
        parts = akoma_uri.strip('/').split('/')
        if len(parts) >= 6 and parts[0] == 'akn' and parts[1] == 'it' and parts[2] == 'act':
            tipo = parts[3]  # legge, decreto-legge, etc.
            giurisdizione = parts[4]  # stato
            data = parts[5]  # 2003-07-29
            numero = parts[6]  # 229

            # Gestisci tipi diversi
            if tipo == 'legge':
                urn = f"urn:nir:stato:legge:{data.replace('-', '-')};{numero}"
            elif tipo == 'decreto-legge':
                urn = f"urn:nir:stato:decreto-legge:{data.replace('-', '-')};{numero}"
            elif tipo == 'decretoLegislativo':
                urn = f"urn:nir:stato:decreto.legislativo:{data.replace('-', '-')};{numero}"
            elif tipo == 'costituzione':
                urn = f"urn:nir:stato:costituzione:{data.replace('-', '-')}"
            else:
                return None

            return f"https://www.normattiva.it/uri-res/N2Ls?{urn}"
    except:
        pass

    return None


def extract_akoma_uris_from_xml(xml_file_path):
    """
    Estrae tutti gli URI Akoma Ntoso da un file XML.

    Args:
        xml_file_path: percorso al file XML

    Returns:
        set: insieme di URI Akoma Ntoso trovati nel documento
    """
    akoma_uris = set()

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Cerca tutti gli elementi con attributo href che inizia con /akn/
        for element in root.findall('.//*[@href]'):
            href = element.get('href')
            if href and href.startswith('/akn/'):
                akoma_uris.add(href)

    except ET.ParseError:
        pass
    except Exception:
        pass

    return akoma_uris

def build_cross_references_mapping_from_urls(url_to_file_mapping):
    """
    Costruisce un mapping da URL normattiva.it a percorsi relativi dei file markdown.

    Args:
        url_to_file_mapping: dict che mappa URL normattiva.it ai percorsi dei file

    Returns:
        dict: mapping da URL normattiva.it a percorso relativo del file markdown
    """
    return url_to_file_mapping

def create_index_file(folder_path, main_params, cited_urls, successful, failed):
    """
    Crea un file indice che elenca tutte le leggi scaricate.
    """
    index_path = os.path.join(folder_path, "index.md")

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"# Raccolta Legislativa\n\n")
        f.write(f"**Legge principale:** {main_params['codiceRedaz']} del {main_params['dataGU']}\n\n")
        f.write(f"**Le leggi citate scaricate:** {successful}\n\n")
        f.write(f"**Le leggi citate non scaricate:** {failed}\n\n")

        if successful > 0:
            f.write("## Leggi Citare Scaricate\n\n")
            refs_path = os.path.join(folder_path, "refs")
            for filename in sorted(os.listdir(refs_path)):
                if filename.endswith('.md'):
                    f.write(f"- [{filename}](./refs/{filename})\n")
            f.write("\n")

        f.write(f"[Legge principale](./main.md)\n")


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
    python convert_akomantoso.py "https://www.normattiva.it/esporta/attoCompleto?atto.dataPubblicazioneGazzetta=2018-07-13&atto.codiceRedazionale=18G00112" output.md
    python convert_akomantoso.py "URL" > output.md
    python convert_akomantoso.py -i "URL" -o output.md

    # Da URL normattiva.it con articolo specifico
    python convert_akomantoso.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" output.md
    python convert_akomantoso.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis" output.md

    # Forza conversione completa anche con URL articolo-specifico
    python convert_akomantoso.py "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" --completo output.md
    python convert_akomantoso.py -c "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis" output.md

    # Ricerca per nome naturale (richiede Exa API key)
    python convert_akomantoso.py -s "legge stanca" output.md
    python convert_akomantoso.py --search "decreto dignità" > output.md

    # Mantenere XML scaricato da URL
    python convert_akomantoso.py "URL" output.md --keep-xml
    python convert_akomantoso.py "URL" --keep-xml > output.md

     # Scaricare anche tutte le leggi citate
     python convert_akomantoso.py --with-references "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-03-07;82" output.md

     # Generare link markdown agli articoli citati su normattiva.it
     python convert_akomantoso.py --with-urls "input.xml" output.md
     python convert_akomantoso.py --with-urls "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md
            """
    )

    # Version flag
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')

    # Argomenti posizionali (compatibilità con uso semplice)
    parser.add_argument('input', nargs='?',
                       help='File XML locale o URL normattiva.it (inclusi URL atto intero)')
    parser.add_argument('output', nargs='?',
                       help='File Markdown di output (default: stdout)')

    # Argomenti opzionali (per maggiore flessibilità)
    parser.add_argument('-i', '--input', dest='input_named',
                         help='File XML locale o URL normattiva.it (inclusi URL atto intero)')
    parser.add_argument('-o', '--output', dest='output_named',
                        help='File Markdown di output (default: stdout)')
    parser.add_argument('-s', '--search', dest='search_query',
                         help='Cerca documento legale per nome naturale (es. "legge stanca")')
    parser.add_argument('--keep-xml', action='store_true',
                         help='Mantieni file XML temporaneo dopo conversione da URL')
    parser.add_argument('-q', '--quiet', action='store_true',
                         help='Modalità silenziosa: mostra solo errori')
    parser.add_argument('-c', '--completo', action='store_true',
                          help='Scarica e converti la legge completa anche se l\'URL specifica un singolo articolo')
    parser.add_argument('--with-references', action='store_true',
                           help='Scarica e converti anche tutte le leggi citate, creando una struttura di cartelle con collegamenti incrociati')
    parser.add_argument('--with-urls', action='store_true',
                           help='Genera link markdown agli articoli citati su normattiva.it (solo conversione, nessun download)')
    parser.add_argument('--debug-search', action='store_true',
                         help='Mostra JSON completo da Exa API e permetti selezione manuale dei risultati di ricerca')
    parser.add_argument('--auto-select', action='store_true', default=True,
                         help='Seleziona automaticamente il miglior risultato di ricerca (default: True)')

    args = parser.parse_args()

    # Determina input e output
    input_source = args.input or args.input_named
    search_query = args.search_query
    output_file = args.output or args.output_named
    with_references = args.with_references

    # Valida che almeno input o search sia specificato
    if not input_source and not search_query:
        parser.error("Input richiesto.\n"
                    "Uso: python convert_akomantoso.py <input> [output.md]\n"
                    "oppure: python convert_akomantoso.py -i <input> [-o output.md]\n"
                    "oppure: python convert_akomantoso.py -s <query> [-o output.md]\n"
                    "Se output omesso, markdown va a stdout")

    # Validate --with-references parameter
    if with_references:
        if not is_normattiva_url(input_source):
            print("❌ --with-references può essere usato solo con URL normattiva.it", file=sys.stderr)
            sys.exit(1)
        if output_file and not os.path.isdir(output_file) and os.path.exists(output_file):
            print("❌ --with-references richiede un nome di directory (non un file esistente)", file=sys.stderr)
            print("💡 Esempio: akoma2md --with-references <url> [nome_cartella]", file=sys.stderr)
            sys.exit(1)

    # Sanitize output path if provided
    if output_file:
        try:
            output_file = sanitize_output_path(output_file)
        except ValueError as e:
            print(f"❌ Errore nel path di output: {e}", file=sys.stderr)
            sys.exit(1)

    # Gestisci ricerca naturale se specificata
    if search_query:
        if not args.quiet:
            print(f"🔍 Ricerca documento: {search_query}", file=sys.stderr)

        # Determina se usare selezione automatica o manuale
        auto_select = args.auto_select and not args.debug_search

        input_source = lookup_normattiva_url(search_query, debug_json=args.debug_search, auto_select=auto_select)
        if not input_source:
            print("❌ Impossibile trovare URL per la ricerca specificata", file=sys.stderr)
            sys.exit(1)

        if not args.quiet and not args.debug_search:
            print(f"✅ URL trovato: {input_source}", file=sys.stderr)

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

        # Handle --with-references mode
        if with_references:
            success = convert_with_references(input_source, output_file, args.quiet, args.keep_xml, args.completo)
            if success:
                sys.exit(0)
            else:
                sys.exit(1)

        # Check for article reference in URL
        article_ref = parse_article_reference(input_source)
        if article_ref and not quiet_mode:
            print(f"Rilevato riferimento articolo: {article_ref}", file=sys.stderr)

        # Determine if we should filter to article or convert complete document
        force_complete = args.completo
        if force_complete and article_ref and not quiet_mode:
            print(f"Forzando conversione completa della legge (--completo)", file=sys.stderr)
            article_ref = None  # Override article filtering

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

        # Add article reference to metadata if present (or if overridden by --completo)
        if article_ref:
            metadata['article'] = article_ref
        elif force_complete and parse_article_reference(input_source):
            # Note that complete conversion was forced
            metadata['article'] = parse_article_reference(input_source)  # Include original article ref for reference

        success = convert_akomantoso_to_markdown_improved(xml_temp_path, output_file, metadata, article_ref)

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
    try:
        main()
    except BrokenPipeError:
        # Gestisce il caso in cui stdout viene chiuso (es. piping a less e quit)
        # Chiude stdout e stderr per evitare errori successivi
        import os
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(0)
    except KeyboardInterrupt:
        # Gestisce CTRL+C in modo graceful
        sys.exit(130)
