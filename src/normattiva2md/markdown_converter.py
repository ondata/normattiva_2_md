import re
import sys
import os
import xml.etree.ElementTree as ET
from .constants import AKN_NAMESPACE, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB
from .xml_parser import extract_metadata_from_xml, filter_xml_to_article
from .akoma_utils import akoma_uri_to_normattiva_url
from .normattiva_api import is_normattiva_url

def generate_front_matter(metadata):
    """
    Generate YAML front matter from metadata dictionary.

    Returns front matter string or empty string if no metadata available.
    """
    if not metadata:
        return ""

    # Collect non-None values
    front_matter_data = {}
    for key in [
        "url",
        "url_xml",
        "url_permanente",
        "dataGU",
        "codiceRedaz",
        "dataVigenza",
        "article",
    ]:
        if metadata.get(key):
            front_matter_data[key] = metadata[key]

    if not front_matter_data:
        return ""

    # Generate YAML front matter
    lines = ["---"]
    # Add legal warning at the top
    lines.append("legal_notice: I testi presenti nella banca dati \"Normattiva\" non hanno carattere di ufficialità. L'unico testo ufficiale è quello pubblicato sulla Gazzetta Ufficiale Italiana.")
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
    has_capo = re.search(r"\bCapo\s+[IVX]+", heading_text, re.IGNORECASE)
    has_sezione = re.search(r"\bSezione\s+[IVX]+", heading_text, re.IGNORECASE)

    result = {"type": "", "capo": "", "sezione": ""}
    # Caso 1: Contiene sia Capo che Sezione
    if has_capo and has_sezione:
        result["type"] = "both"
        split_pos = has_sezione.start()
        capo_text = heading_text[:split_pos].strip()
        sezione_text = heading_text[split_pos:].strip()
        result["capo"] = format_heading_with_separator(capo_text)
        result["sezione"] = format_heading_with_separator(sezione_text)
    # Caso 2: Solo Capo
    elif has_capo:
        result["type"] = "capo"
        result["capo"] = format_heading_with_separator(heading_text)
    # Caso 3: Solo Sezione
    elif has_sezione:
        result["type"] = "sezione"
        result["sezione"] = format_heading_with_separator(heading_text)
    # Caso 4: Nessuno dei due (fallback)
    else:
        result["type"] = "unknown"
        result["capo"] = format_heading_with_separator(heading_text)
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
    if text_to_format.startswith("((") and text_to_format.endswith("))"):
        text_to_format = text_to_format[2:-2].strip()
        legislative_prefix = "(("
        legislative_suffix = "))"

    # Pattern per Capo o Sezione
    pattern = r"^((?:Capo|Sezione)\s+[IVX]+)\s+(.+)$"
    match = re.match(pattern, text_to_format, re.IGNORECASE)

    if match:
        prefix = match.group(1)  # "Capo I" o "Sezione I"
        title = match.group(2)  # "PRINCIPI GENERALI"
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
        if child.tag.endswith("strong"):
            text_parts.append(f"**{clean_text_content(child, cross_references)}**")
        elif child.tag.endswith(
            "emphasis" 
        ):  # Akoma Ntoso often uses 'emphasis' for italics
            text_parts.append(f"*{clean_text_content(child, cross_references)}*")
        elif child.tag.endswith("ref"):
            # Extract text content of <ref> tags
            ref_text = clean_text_content(child, cross_references)
            href = child.get("href")

            # If cross_references is provided, try to create a markdown link
            if cross_references and href:
                # Se href è un URI Akoma, convertilo in URL normattiva.it
                if href.startswith("/akn/"):
                    normattiva_url = akoma_uri_to_normattiva_url(href)
                    if normattiva_url:
                        ref_text = f"[{ref_text}]({normattiva_url})"
                # Altrimenti, cerca direttamente nel mapping (per compatibilità)
                elif href in cross_references:
                    ref_text = f"[{ref_text}]({cross_references[href]})"

            text_parts.append(ref_text)
        elif child.tag.endswith(("ins", "del")):
            # For modifications, add double parentheses only if not already present
            inner_text = clean_text_content(child, cross_references)
            # Check if the text already has double parentheses
            if inner_text.strip().startswith("((") and inner_text.strip().endswith("))"):
                text_parts.append(inner_text)
            else:
                text_parts.append(f"(({inner_text}))")
        elif child.tag.endswith("footnote"):
            # Handle footnotes - extract footnote content and create markdown footnote reference
            footnote_content = clean_text_content(child, cross_references)
            if footnote_content:
                # Generate a simple footnote reference (simplified - in practice would need global counter)
                footnote_ref = f"[^{footnote_content[:10].replace(' ', '')}]"  # Simple hash-like ref
                text_parts.append(footnote_ref)

        else:
            text_parts.append(
                clean_text_content(child, cross_references) 
            )  # Recursively get text from other children

        # Process tail text
        if child.tail:
            text_parts.append(child.tail)

    # Join all parts
    full_text = "".join(text_parts)

    # Replace multiple spaces with a single space, and strip leading/trailing whitespace
    cleaned_text = re.sub(r"\s+", " ", full_text).strip()
    
    # Remove dash separators before inline AGGIORNAMENTO
    cleaned_text = re.sub(r"\s*[-–—]{2,}\s*AGGIORNAMENTO", " AGGIORNAMENTO", cleaned_text)

    return cleaned_text


def process_content_with_paragraphs(content_element, ns, cross_references=None):
    """
    Process a <content> element that may contain multiple <p> elements.
    Treats each <p> as a block-level element with appropriate spacing.
    
    Args:
        content_element: The <content> XML element
        ns: XML namespace
        cross_references: Optional cross-reference mapping
    
    Returns:
        str: Processed text with proper line breaks between paragraphs
    """
    if content_element is None:
        return ""
    
    # Check if content has <p> children
    p_elements = content_element.findall("./akn:p", ns)
    
    if not p_elements:
        # No <p> children, process normally
        return clean_text_content(content_element, cross_references)
    
    # Process each <p> separately
    parts = []
    for p_elem in p_elements:
        p_text = clean_text_content(p_elem, cross_references).strip()
        
        # Skip empty, dash-only, or parentheses-only lines
        if not p_text or re.match(r"^[-()]+$", p_text):
            continue
            
        # Check if this is an AGGIORNAMENTO header
        if p_text.startswith("AGGIORNAMENTO"):
            parts.append(f"\n\n{p_text}")
        else:
            # Regular text - add with space if not first
            if parts:
                parts.append(f" {p_text}")
            else:
                parts.append(p_text)
    
    return "".join(parts)

def convert_akomantoso_to_markdown_improved(
    xml_file_path,
    markdown_file_path=None,
    metadata=None,
    article_ref=None,
    cross_references=None,
    with_urls=False,
):
    try:
        # If with_urls is enabled, build cross-reference mapping from <ref> tags
        if with_urls:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            cross_references = cross_references or {}
            # Find all <ref> tags with href
            for ref in root.iter():
                if ref.tag.endswith("ref") and ref.get("href"):
                    href = ref.get("href")
                    # Convert Akoma URI to Normattiva URL if needed
                    if href and href.startswith("/akn/"):
                        normattiva_url = akoma_uri_to_normattiva_url(href)
                    elif href and is_normattiva_url(href):
                        normattiva_url = href
                    else:
                        normattiva_url = None
                    if normattiva_url:
                        cross_references[normattiva_url] = normattiva_url

        # Check file size before parsing (XML bomb protection)
        file_size = os.path.getsize(xml_file_path)
        if file_size > MAX_FILE_SIZE_BYTES:
            print(
                f"Errore: file XML troppo grande ({file_size / 1024 / 1024:.1f}MB). Massimo consentito: {MAX_FILE_SIZE_MB}MB",
                file=sys.stderr,
            )
            return False

        # Parse XML with defusedxml would be better, but using size limit for now
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Filter XML to specific article if requested
        if article_ref:
            filtered_root = filter_xml_to_article(root, article_ref, AKN_NAMESPACE)
            if filtered_root is None:
                # Article not found - continue with empty body but include metadata
                print(
                    f"⚠️  Warning: Article '{article_ref}' not found in document",
                    file=sys.stderr,
                )
                # Create empty root to generate metadata-only output
                filtered_root = ET.Element(root.tag, root.attrib)
                # Copy meta elements for metadata extraction
                for meta_elem in root.findall('.//akn:meta', AKN_NAMESPACE):
                    filtered_root.append(meta_elem)
            root = filtered_root

        # Extract metadata from XML if not provided (for local files)
        if metadata is None:
            metadata = extract_metadata_from_xml(root)

        markdown_fragments = generate_markdown_fragments(
            root, AKN_NAMESPACE, metadata, cross_references
        )
    except ET.ParseError as e:
        print(f"Errore durante il parsing del file XML: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Errore: Il file '{xml_file_path}' non trovato.\n", file=sys.stderr)
        print("Per usare akoma2md, puoi:", file=sys.stderr)
        print("  1. Fornire un URL di normattiva.it:", file=sys.stderr)
        print(
            "     akoma2md 'https://www.normattiva.it/uri-res/N2Ls?urn:...' output.md",
            file=sys.stderr,
        )
        print("  2. Fornire il percorso di un file XML locale:", file=sys.stderr)
        print("     akoma2md percorso/al/file.xml output.md", file=sys.stderr)
        print("  3. Cercare una legge per nome con -s:", file=sys.stderr)
        print("     akoma2md -s 'legge stanca' output.md", file=sys.stderr)
        print(
            "     akoma2md -s 'legge stanca' --exa-api-key 'your-key' output.md",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(f"Si è verificato un errore inatteso: {e}", file=sys.stderr)
        return False

    markdown_text = "".join(markdown_fragments)

    if markdown_file_path is None:
        sys.stdout.write(markdown_text)
        return True

    try:
        with open(markdown_file_path, "w", encoding="utf-8") as f:
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
    attachment_fragments = extract_attachments_fragments(root, ns, cross_references)

    body_fragments = []
    body_fragments.extend(preamble_fragments)
    body_fragments.extend(body_elements_fragments)
    body_fragments.extend(attachment_fragments)

    # Join body content (NO downgrade - proper hierarchy from parsing)
    body_text = "".join(body_fragments)

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

def generate_markdown_text(
    root, ns=AKN_NAMESPACE, metadata=None, cross_references=None
):
    """Return the Markdown rendering for the provided Akoma Ntoso root."""

    return "".join(generate_markdown_fragments(root, ns, metadata, cross_references))

def extract_document_title(root, ns):
    """Convert the `<docTitle>` element to a Markdown H1 if present."""

    doc_title_element = root.find(".//akn:docTitle", ns)
    if doc_title_element is not None and doc_title_element.text:
        return [f"# {doc_title_element.text.strip()}\n\n"]
    return []

def extract_preamble_fragments(root, ns, cross_references=None):
    """Collect Markdown fragments representing the document preamble."""

    fragments = []
    preamble = root.find(".//akn:preamble", ns)
    if preamble is None:
        return fragments

    for element in preamble:
        if element.tag.endswith("formula") or element.tag.endswith("p"):
            text = clean_text_content(element, cross_references)
            if text:
                fragments.append(f"{text}\n\n")
        elif element.tag.endswith("citations"):
            for citation in element.findall("./akn:citation", ns):
                text = clean_text_content(citation, cross_references)
                if text:
                    fragments.append(f"{text}\n\n")
    return fragments

def extract_body_fragments(root, ns, cross_references=None):
    """Traverse body nodes and delegate conversion to specialised handlers."""

    fragments = []
    body = root.find(".//akn:body", ns)
    if body is None:
        return fragments

    for element in body:
        fragments.extend(process_body_element(element, ns, cross_references))
    return fragments


def extract_attachments_fragments(root, ns, cross_references=None):
    """Collect attachment fragments that live outside the main body."""

    fragments = []
    attachments_container = root.find(".//akn:attachments", ns)
    if attachments_container is None:
        return fragments

    attachment_elements = attachments_container.findall("./akn:attachment", ns)
    if not attachment_elements:
        return fragments

    fragments.append("## Allegati\n\n")
    for attachment in attachment_elements:
        fragments.extend(process_attachment(attachment, ns, cross_references))

    return fragments

def process_body_element(element, ns, cross_references=None):
    """Process a direct child of `<body>` producing Markdown fragments."""

    if element.tag.endswith("title"):
        return process_title(element, ns, cross_references)
    if element.tag.endswith("part"):
        return process_part(element, ns, cross_references)
    if element.tag.endswith("chapter"):
        return process_chapter(element, ns, cross_references)
    if element.tag.endswith("article"):
        article_fragments = []
        process_article(
            element, article_fragments, ns, level=2, cross_references=cross_references
        )
        return article_fragments
    if element.tag.endswith("attachment"):
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
    heading_element = chapter_element.find("./akn:heading", ns)

    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        parsed = parse_chapter_heading(clean_heading)

        # Determine heading levels based on parsed structure
        if parsed["type"] == "both":
            # Capo + Sezione: Capo is H2, Sezione is H3
            chapter_fragments.append(f"## {parsed['capo']}\n\n")
            chapter_fragments.append(f"### {parsed['sezione']}\n\n")
            article_level = 4  # Articles under sezione are H4

        elif parsed["type"] == "capo":
            # Only Capo: H2
            chapter_fragments.append(f"## {parsed['capo']}\n\n")
            article_level = 3  # Articles directly under capo are H3

        elif parsed["type"] == "sezione":
            # Only Sezione: H3 (assumes it's under a previous Capo)
            chapter_fragments.append(f"### {parsed['sezione']}\n\n")
            article_level = 4  # Articles under sezione are H4

        else:
            # Unknown/fallback
            chapter_fragments.append(f"## {parsed['capo']}\n\n")
            article_level = 3

    # Process child elements
    for child in chapter_element:
        if child.tag.endswith("section"):
            chapter_fragments.extend(process_section(child, ns, cross_references))
        elif child.tag.endswith("article"):
            process_article(
                child,
                chapter_fragments,
                ns,
                level=article_level,
                cross_references=cross_references,
            )

    return chapter_fragments

def process_section(section_element, ns, cross_references=None):
    """Convert a section element and its articles to Markdown fragments."""

    section_fragments = []
    heading_element = section_element.find("./akn:heading", ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        section_fragments.append(f"#### {clean_heading}\n\n")

    for article in section_element.findall("./akn:article", ns):
        process_article(
            article,
            section_fragments,
            ns,
            level=4,
            cross_references=cross_references,
        )
    return section_fragments

def process_title(title_element, ns, cross_references=None):
    """
    Convert a title element to Markdown H2 heading.
    Titles are top-level structural elements.
    """
    title_fragments = []
    heading_element = title_element.find("./akn:heading", ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        title_fragments.append(f"## {clean_heading}\n\n")

    # Process any nested content (chapters, articles, etc.)
    for child in title_element:
        if child.tag.endswith("chapter"):
            title_fragments.extend(process_chapter(child, ns, cross_references))
        elif child.tag.endswith("article"):
            process_article(
                child,
                title_fragments,
                ns,
                level=3,
                cross_references=cross_references,
            )

    return title_fragments

def process_part(part_element, ns, cross_references=None):
    """
    Convert a part element to Markdown fragments.
    Parts are major structural divisions, rendered as H3.
    """
    part_fragments = []
    heading_element = part_element.find("./akn:heading", ns)
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)
        part_fragments.append(f"### {clean_heading}\n\n")

    # Process nested content (chapters, articles, etc.)
    for child in part_element:
        if child.tag.endswith("chapter"):
            part_fragments.extend(process_chapter(child, ns, cross_references))
        elif child.tag.endswith("article"):
            process_article(
                child,
                part_fragments,
                ns,
                level=3,
                cross_references=cross_references,
            )

    return part_fragments

def process_attachment(attachment_element, ns, cross_references=None):
    """
    Convert an attachment element to Markdown fragments.
    Attachments are rendered as a separate section.
    """
    attachment_fragments = []
    heading_element = attachment_element.find("./akn:heading", ns)
    clean_heading = ""
    heading_from_prefix = False
    heading_from_paragraph = False
    if heading_element is not None and heading_element.text:
        clean_heading = clean_text_content(heading_element, cross_references)

    if not clean_heading:
        # Try to derive a meaningful heading from the first paragraph (common in Normattiva)
        first_p = attachment_element.find(".//akn:p", ns)
        if first_p is not None:
            raw_text = "".join(first_p.itertext())
            raw_text = re.sub(r"\s+", " ", raw_text).strip()
            match = re.match(
                r"(Art\.?\s*\d+(?:-\w+)?\.?\s*(\(\([^)]*\)\)|\([^)]*\))?)", raw_text
            )
            if match:
                clean_heading = match.group(1)
                heading_from_paragraph = True
            else:
                prefix_match = re.match(r"^(.*?)(?:\s+Art\.)", raw_text)
                if prefix_match:
                    clean_heading = prefix_match.group(1).strip()
                    heading_from_prefix = True
                    heading_from_paragraph = True

    if clean_heading:
        heading_level = "###"
        if heading_from_prefix and clean_heading == clean_heading.upper():
            heading_level = "##"
        attachment_fragments.append(f"{heading_level} {clean_heading}\n\n")
    else:
        attachment_fragments.append("### Allegato\n\n")

    # Process attachment content (similar to body processing)
    main_body = attachment_element.find(".//akn:mainBody", ns)
    if main_body is not None:
        paragraphs = main_body.findall("./akn:paragraph", ns)
        if paragraphs:
            for paragraph in paragraphs:
                # Process paragraph content with support for multiple <p> elements
                para_content = paragraph.find("./akn:content", ns)
                text = process_content_with_paragraphs(para_content, ns, cross_references) if para_content is not None else ""
                
                if text and clean_heading:
                    normalized = re.sub(r"\s+", " ", text).strip()
                    if normalized.startswith(clean_heading):
                        trimmed = normalized[len(clean_heading):].lstrip()
                        if heading_from_paragraph:
                            if trimmed.startswith("."):
                                trimmed = trimmed[1:].lstrip()
                            text = trimmed

                # Promote uppercase title lines (e.g. "CODICE CIVILE") to a heading
                if text:
                    normalized = re.sub(r"\s+", " ", text).strip()
                    if not heading_from_paragraph:
                        title_match = re.match(
                            r"^(?P<title>[A-Z][A-Z0-9' .-]{3,})\s+Art\.",
                            normalized,
                        )
                        if title_match:
                            title = title_match.group("title").strip()
                            if title and title == title.upper() and len(title) <= 80:
                                attachment_fragments.append(f"## {title}\n\n")
                                text = normalized[len(title) :].lstrip()
                        if normalized and normalized == normalized.upper() and len(normalized) <= 80:
                            attachment_fragments.append(f"## {normalized}\n\n")
                            continue
                if text:
                    art_match = re.match(
                        r"^Art\.?\s*(?P<num>\d+[A-Za-z-]*)\.?\s*(?P<title>\([^)]*\))?\s*(?P<body>.*)$",
                        text,
                    )
                    if art_match:
                        num = art_match.group("num")
                        title = art_match.group("title") or ""
                        body = art_match.group("body").lstrip()
                        if body.startswith("."):
                            body = body[1:].lstrip()
                        if body.startswith("))"):
                            body = body[2:].lstrip()
                        if title:
                            title = re.sub(r"\s+", " ", title).strip()
                            title = title.replace("(( ", "((").replace("( (", "((")
                            title = title.replace(") )", "))")
                        heading = f"Art. {num}."
                        if title:
                            heading = f"{heading} {title}"
                        attachment_fragments.append(f"### {heading}\n\n")
                        if body:
                            attachment_fragments.append(f"{body}\n\n")
                    else:
                        attachment_fragments.append(f"{text}\n\n")
            return attachment_fragments

        for child in main_body:
            attachment_fragments.extend(
                process_body_element(child, ns, cross_references)
            )
        return attachment_fragments

    for child in attachment_element:
        if child.tag.endswith("chapter"):
            attachment_fragments.extend(process_chapter(child, ns, cross_references))
        elif child.tag.endswith("article"):
            process_article(
                child,
                attachment_fragments,
                ns,
                level=3,
                cross_references=cross_references,
            )

    return attachment_fragments

def process_table(table_element, ns, cross_references=None):
    """
    Convert an Akoma Ntoso table element to basic Markdown table format.
    This is a simplified implementation that extracts text content.
    """
    table_rows = []

    # Find all rows in the table
    rows = table_element.findall(".//akn:tr", ns)
    if not rows:
        return ""

    for row in rows:
        row_cells = []
        # Find all cells in this row (td or th)
        cells = row.findall("./akn:td", ns) + row.findall("./akn:th", ns)
        if not cells:
            continue

        for cell in cells:
            cell_text = clean_text_content(cell, cross_references)
            # Escape pipe characters in cell content
            cell_text = cell_text.replace("|", "\\|")
            row_cells.append(cell_text)

        if row_cells:
            table_rows.append("| " + " | ".join(row_cells) + " |")

    if not table_rows:
        return ""

    # Create markdown table with header separator
    markdown_table = "\n".join(table_rows[:1])  # First row as header
    if len(table_rows) > 1:
        # Add separator row
        num_cols = table_rows[0].count("|") - 1
        separator = "| " + " | ".join(["---"] * num_cols) + " |"
        markdown_table += "\n" + separator
        # Add remaining rows
        markdown_table += "\n" + "\n".join(table_rows[1:])

    return markdown_table

def process_article(
    article_element, markdown_content_list, ns, level=2, cross_references=None
):
    article_num_element = article_element.find("./akn:num", ns)
    article_heading_element = article_element.find("./akn:heading", ns)

    if article_num_element is not None:
        article_num = clean_text_content(article_num_element, cross_references).strip()
        if article_heading_element is not None and article_heading_element.text:
            clean_article_heading = clean_text_content(
                article_heading_element, cross_references
            )
            # Improved formatting: "Art. X - Title" format
            heading_prefix = "#" * level
            markdown_content_list.append(
                f"{heading_prefix} {article_num} - {clean_article_heading}\n\n"
            )
        else:
            heading_prefix = "#" * level
            markdown_content_list.append(f"{heading_prefix} {article_num}\n\n")

    # Process paragraphs and lists within articles
    for child_of_article in article_element:
        if child_of_article.tag.endswith("paragraph"):
            para_num_element = child_of_article.find("./akn:num", ns)
            para_content_element = child_of_article.find("./akn:content", ns)
            para_list_element = child_of_article.find("./akn:list", ns)

            # Check if paragraph contains a list
            if para_list_element is not None:
                # Handle intro element in lists (like in Article 1)
                intro_element = para_list_element.find("./akn:intro", ns)
                if intro_element is not None:
                    intro_text = clean_text_content(intro_element, cross_references)
                    if intro_text:
                        # Remove double dots from paragraph numbering
                        para_num = para_num_element.text.strip().rstrip(".")
                        markdown_content_list.append(f"{para_num}. {intro_text}\n\n")
                    elif intro_text:
                        markdown_content_list.append(f"{intro_text}\n\n")

                for list_item in para_list_element.findall("./akn:point", ns):
                    list_num_element = list_item.find("./akn:num", ns)
                    list_content_element = list_item.find("./akn:content", ns)

                    list_item_text = (
                        clean_text_content(list_content_element, cross_references)
                        if list_content_element is not None
                        else ""
                    )

                    if list_num_element is not None:
                        markdown_content_list.append(
                            f"- {list_num_element.text.strip()} {list_item_text}\n"
                        )
                    elif list_item_text:
                        markdown_content_list.append(f"- {list_item_text}\n")
                markdown_content_list.append("\n")  # Add a newline after a list
            else:
                # Handle regular paragraph content
                paragraph_text = (
                    process_content_with_paragraphs(para_content_element, ns, cross_references)
                    if para_content_element is not None
                    else ""
                )

                # Remove duplicate number if present at the beginning of the paragraph text
                if para_num_element is not None:
                    num_to_remove = para_num_element.text.strip().rstrip(".")
                    # Regex to match the number followed by a period and optional space at the beginning of the string
                    pattern = r"^" + re.escape(num_to_remove) + r"\.?\s*"
                    paragraph_text = re.sub(pattern, "", paragraph_text, 1)

                if para_num_element is not None and paragraph_text:
                    # Remove double dots from paragraph numbering and ensure single dot
                    para_num = para_num_element.text.strip().rstrip(".")
                    markdown_content_list.append(f"{para_num}. {paragraph_text}\n\n")
                elif paragraph_text:
                    # If no number but there's text, just append the text
                    markdown_content_list.append(f"{paragraph_text}\n\n")

        elif child_of_article.tag.endswith("list"):
            # Handle intro element in lists (like in Article 1)
            intro_element = child_of_article.find("./akn:intro", ns)
            if intro_element is not None:
                intro_text = clean_text_content(intro_element, cross_references)
                if intro_text:
                    markdown_content_list.append(f"{intro_text}\n\n")

            for list_item in child_of_article.findall("./akn:point", ns):
                list_num_element = list_item.find("./akn:num", ns)
                list_content_element = list_item.find("./akn:content", ns)

                list_item_text = (
                    clean_text_content(list_content_element, cross_references)
                    if list_content_element is not None
                    else ""
                )

                if list_num_element is not None:
                    markdown_content_list.append(
                        f"- {list_num_element.text.strip()} {list_item_text}\n"
                    )
                elif list_item_text:
                    markdown_content_list.append(f"- {list_item_text}\n")
            markdown_content_list.append("\n")  # Add a newline after a list

        elif child_of_article.tag.endswith("table"):
            # Handle tables - convert to basic markdown table format
            table_markdown = process_table(child_of_article, ns, cross_references)
            if table_markdown:
                markdown_content_list.append(table_markdown)
                markdown_content_list.append("\n")

        elif child_of_article.tag.endswith("quotedStructure"):
            # Handle quoted structures - wrap in markdown blockquote
            quoted_content = clean_text_content(child_of_article, cross_references)
            if quoted_content:
                # Split into lines and add > prefix to each line
                lines = quoted_content.split("\n")
                quoted_lines = [f"> {line}" for line in lines if line.strip()]
                markdown_content_list.append("\n".join(quoted_lines))
                markdown_content_list.append("\n")
