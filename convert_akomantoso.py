import xml.etree.ElementTree as ET
import re
import sys
import argparse
import os
import requests
from datetime import datetime

AKN_NAMESPACE = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}

def parse_chapter_heading(heading_text):
    """
    Separa heading che contengono sia Capo che Sezione.
    Pattern: "Capo [N] [TITOLO] Sezione [N] [Titolo]"
    Gestisce anche il caso in cui Sezione sia dentro modifiche legislative (( ))
    Returns: {'capo': ..., 'sezione': ...} or {'capo': ..., 'sezione': None}
    """
    # Cerca "Sezione" nell'heading, anche se dentro (( ))
    sezione_match = re.search(r'\(?\(?\s*(Sezione\s+[IVX]+)', heading_text, re.IGNORECASE)

    if sezione_match and heading_text.startswith('Capo'):
        # Split in base alla posizione di "Sezione"
        split_pos = sezione_match.start()
        capo_text = heading_text[:split_pos].strip()
        sezione_text = heading_text[split_pos:].strip()

        capo = format_heading_with_separator(capo_text)
        sezione = format_heading_with_separator(sezione_text)
        return {'capo': capo, 'sezione': sezione}

    # Se non c'è match, formatta comunque l'heading
    return {'capo': format_heading_with_separator(heading_text), 'sezione': None}

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
        bool: True se è un URL normattiva.it
    """
    if not isinstance(input_str, str):
        return False
    return bool(re.match(r'https?://(www\.)?normattiva\.it/', input_str, re.IGNORECASE))

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
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8'
    }

    try:
        response = session.get(url, headers=headers, timeout=30)
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

    # Simula un browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
        'Referer': 'https://www.normattiva.it/'
    }

    try:
        response = session.get(url, headers=headers, timeout=30, allow_redirects=True)
        response.raise_for_status()

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

def convert_akomantoso_to_markdown_improved(xml_file_path, markdown_file_path=None):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        markdown_fragments = generate_markdown_fragments(root, AKN_NAMESPACE)
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


def generate_markdown_fragments(root, ns):
    """Build the markdown fragments for a parsed Akoma Ntoso document."""

    fragments = []
    fragments.extend(extract_document_title(root, ns))
    fragments.extend(extract_preamble_fragments(root, ns))
    fragments.extend(extract_body_fragments(root, ns))
    return fragments


def generate_markdown_text(root, ns=AKN_NAMESPACE):
    """Return the Markdown rendering for the provided Akoma Ntoso root."""

    return ''.join(generate_markdown_fragments(root, ns))


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
        process_article(element, article_fragments, ns)
        return article_fragments
    if element.tag.endswith('attachment'):
        return process_attachment(element, ns)
    return []


def process_chapter(chapter_element, ns):
    """Convert a chapter element (and its nested children) to Markdown fragments."""

    chapter_fragments = []
    heading_element = chapter_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        parsed = parse_chapter_heading(clean_heading)
        chapter_fragments.append(f"## {parsed['capo']}\n\n")
        if parsed['sezione']:
            chapter_fragments.append(f"### {parsed['sezione']}\n\n")

    for child in chapter_element:
        if child.tag.endswith('section'):
            chapter_fragments.extend(process_section(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, chapter_fragments, ns)
    return chapter_fragments


def process_section(section_element, ns):
    """Convert a section element and its articles to Markdown fragments."""

    section_fragments = []
    heading_element = section_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        section_fragments.append(f"### {clean_heading}\n\n")

    for article in section_element.findall('./akn:article', ns):
        process_article(article, section_fragments, ns)
    return section_fragments


def process_title(title_element, ns):
    """
    Convert a title element to Markdown H1 heading.
    Titles are top-level structural elements.
    """
    title_fragments = []
    heading_element = title_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        title_fragments.append(f"# {clean_heading}\n\n")

    # Process any nested content (chapters, articles, etc.)
    for child in title_element:
        if child.tag.endswith('chapter'):
            title_fragments.extend(process_chapter(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, title_fragments, ns)

    return title_fragments


def process_part(part_element, ns):
    """
    Convert a part element to Markdown fragments.
    Parts are major structural divisions, rendered as H2.
    """
    part_fragments = []
    heading_element = part_element.find('./akn:heading', ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element)
        part_fragments.append(f"## {clean_heading}\n\n")

    # Process nested content (chapters, articles, etc.)
    for child in part_element:
        if child.tag.endswith('chapter'):
            part_fragments.extend(process_chapter(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, part_fragments, ns)

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
        attachment_fragments.append(f"## Allegato: {clean_heading}\n\n")
    else:
        attachment_fragments.append("## Allegato\n\n")

    # Process attachment content (similar to body processing)
    for child in attachment_element:
        if child.tag.endswith('chapter'):
            attachment_fragments.extend(process_chapter(child, ns))
        elif child.tag.endswith('article'):
            process_article(child, attachment_fragments, ns)

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


def process_article(article_element, markdown_content_list, ns):
    article_num_element = article_element.find('./akn:num', ns)
    article_heading_element = article_element.find('./akn:heading', ns)

    if article_num_element is not None:
        article_num = article_num_element.text.strip()
        if article_heading_element is not None and article_heading_element.text:
            clean_article_heading = clean_text_content(article_heading_element)
            # Improved formatting: "Art. X - Title" format
            markdown_content_list.append(f"# {article_num} - {clean_article_heading}\n\n")
        else:
            markdown_content_list.append(f"# {article_num}\n\n")

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

    # Valida che input sia specificato
    if not input_source:
        parser.error("Input richiesto.\n"
                    "Uso: python convert_akomantoso.py <input> [output.md]\n"
                    "oppure: python convert_akomantoso.py -i <input> [-o output.md]\n"
                    "Se output omesso, markdown va a stdout")

    # Auto-detect: URL o file locale?
    if is_normattiva_url(input_source):
        # Gestione URL
        if not args.quiet:
            print(f"Rilevato URL normattiva.it: {input_source}", file=sys.stderr)

        # Estrai parametri dalla pagina
        params, session = extract_params_from_normattiva_url(input_source, quiet=args.quiet)
        if not params:
            print("❌ Impossibile estrarre parametri dall'URL", file=sys.stderr)
            sys.exit(1)

        if not args.quiet:
            print(f"\nParametri estratti:", file=sys.stderr)
            print(f"  dataGU: {params['dataGU']}", file=sys.stderr)
            print(f"  codiceRedaz: {params['codiceRedaz']}", file=sys.stderr)
            print(f"  dataVigenza: {params['dataVigenza']}\n", file=sys.stderr)

        # Crea file XML temporaneo
        xml_temp_path = f"temp_{params['codiceRedaz']}.xml"

        # Scarica XML
        if not download_akoma_ntoso(params, xml_temp_path, session, quiet=args.quiet):
            print("❌ Errore durante il download del file XML", file=sys.stderr)
            sys.exit(1)

        # Converti a Markdown
        if not args.quiet:
            print(f"\nConversione in Markdown...", file=sys.stderr)
        success = convert_akomantoso_to_markdown_improved(xml_temp_path, output_file)

        if success:
            if not args.quiet:
                if output_file:
                    print(f"✅ Conversione completata: {output_file}", file=sys.stderr)
                else:
                    print(f"✅ Conversione completata (output a stdout)", file=sys.stderr)

            # Rimuovi XML temporaneo se non richiesto diversamente
            if not args.keep_xml:
                try:
                    os.remove(xml_temp_path)
                    if not args.quiet:
                        print(f"File XML temporaneo rimosso", file=sys.stderr)
                except OSError as e:
                    print(f"Attenzione: impossibile rimuovere file temporaneo: {e}", file=sys.stderr)
            else:
                if not args.quiet:
                    print(f"File XML mantenuto: {xml_temp_path}", file=sys.stderr)

            sys.exit(0)
        else:
            print("❌ Errore durante la conversione", file=sys.stderr)
            sys.exit(1)

    else:
        # Gestione file XML locale
        if output_file:
            print(f"Conversione da file XML locale: '{input_source}' a '{output_file}'...", file=sys.stderr)
        else:
            print(f"Conversione da file XML locale: '{input_source}' (output a stdout)...", file=sys.stderr)
        success = convert_akomantoso_to_markdown_improved(input_source, output_file)

        if success:
            print("✅ Conversione completata con successo!", file=sys.stderr)
            sys.exit(0)
        else:
            print("❌ Errore durante la conversione.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
