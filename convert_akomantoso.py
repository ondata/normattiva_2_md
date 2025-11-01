import xml.etree.ElementTree as ET
import re
import sys
import argparse

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

def convert_akomantoso_to_markdown_improved(xml_file_path, markdown_file_path):
    markdown_content = []
    ns = {'akn': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0'}

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Extract document title (if available)
        doc_title_element = root.find('.//akn:docTitle', ns)
        if doc_title_element is not None and doc_title_element.text:
            markdown_content.append(f"# {doc_title_element.text.strip()}\n\n")

        # Extract preamble content
        preamble = root.find('.//akn:preamble', ns)
        if preamble is not None:
            for element in preamble:
                if element.tag.endswith('formula') or element.tag.endswith('p'):
                    text = clean_text_content(element)
                    if text:
                        markdown_content.append(f"{text}\n\n")
                elif element.tag.endswith('citations'):
                    for citation in element.findall('./akn:citation', ns):
                        text = clean_text_content(citation)
                        if text:
                            markdown_content.append(f"{text}\n\n")

        # Iterate through the body of the document
        body = root.find('.//akn:body', ns)
        if body is not None:
            for chapter_or_article in body:
                # Handle chapters and sections
                if chapter_or_article.tag.endswith('chapter'):
                    heading_element = chapter_or_article.find('./akn:heading', ns)
                    if heading_element is not None and heading_element.text:
                        # Clean heading text, including removing (( )) if present
                        clean_heading = clean_text_content(heading_element)
                        # Parse to separate Capo and Sezione if both present
                        parsed = parse_chapter_heading(clean_heading)
                        if parsed['sezione']:
                            # Separa in due heading distinti
                            markdown_content.append(f"## {parsed['capo']}\n\n")
                            markdown_content.append(f"### {parsed['sezione']}\n\n")
                        else:
                            # Heading singolo
                            markdown_content.append(f"## {parsed['capo']}\n\n")

                    # Process articles directly under chapter or within sections
                    for element in chapter_or_article:
                        if element.tag.endswith('section'):
                            section_heading_element = element.find('./akn:heading', ns)
                            if section_heading_element is not None and section_heading_element.text:
                                clean_section_heading = clean_text_content(section_heading_element)
                                markdown_content.append(f"### {clean_section_heading}\n\n")

                            for article in element.findall('./akn:article', ns):
                                process_article(article, markdown_content, ns)
                        elif element.tag.endswith('article'):
                            process_article(element, markdown_content, ns)
                elif chapter_or_article.tag.endswith('article'): # Articles directly under body
                    process_article(chapter_or_article, markdown_content, ns)

    except ET.ParseError as e:
        print(f"Errore durante il parsing del file XML: {e}")
        return False
    except FileNotFoundError:
        print(f"Errore: Il file XML '{xml_file_path}' non trovato.")
        return False
    except Exception as e:
        print(f"Si è verificato un errore inatteso: {e}")
        return False

    try:
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(''.join(markdown_content))
        print(f"Conversione completata. Il file Markdown è stato salvato in '{markdown_file_path}'")
        return True
    except IOError as e:
        print(f"Errore durante la scrittura del file Markdown: {e}")
        return False

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

def main():
    """
    Funzione principale che gestisce gli argomenti della riga di comando
    """
    parser = argparse.ArgumentParser(
        description='Converte un file XML Akoma Ntoso in formato Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  python convert_akomantoso.py input.xml output.md
  python convert_akomantoso.py -i input.xml -o output.md
  python convert_akomantoso.py --input input.xml --output output.md
        """
    )

    # Argomenti posizionali (compatibilità con uso semplice)
    parser.add_argument('input_file', nargs='?',
                       help='File XML di input in formato Akoma Ntoso')
    parser.add_argument('output_file', nargs='?',
                       help='File Markdown di output')

    # Argomenti opzionali (per maggiore flessibilità)
    parser.add_argument('-i', '--input', dest='input_named',
                       help='File XML di input in formato Akoma Ntoso')
    parser.add_argument('-o', '--output', dest='output_named',
                       help='File Markdown di output')

    args = parser.parse_args()

    # Determina i file di input e output
    input_file = args.input_file or args.input_named
    output_file = args.output_file or args.output_named

    # Valida che entrambi i file siano specificati
    if not input_file or not output_file:
        parser.error("Sono richiesti sia il file di input che quello di output.\n"
                    "Uso: python convert_akomantoso.py <input.xml> <output.md>\n"
                    "oppure: python convert_akomantoso.py -i <input.xml> -o <output.md>")

    # Esegui la conversione
    print(f"Conversione da '{input_file}' a '{output_file}'...")
    success = convert_akomantoso_to_markdown_improved(input_file, output_file)

    if success:
        print("✅ Conversione completata con successo!")
        sys.exit(0)
    else:
        print("❌ Errore durante la conversione.")
        sys.exit(1)

if __name__ == "__main__":
    main()
