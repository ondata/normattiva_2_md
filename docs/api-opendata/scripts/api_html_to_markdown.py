#!/usr/bin/env python3
"""
POC: Conversione HTML da API OpenData → Markdown
Confronto con approccio attuale (XML AKN → Markdown)
"""

import json
import re
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path


class APIHTMLToMarkdown(HTMLParser):
    """Converte HTML strutturato da API Normattiva in Markdown"""

    def __init__(self):
        super().__init__()
        self.md_lines = []
        self.current_text = StringIO()
        self.in_article = False
        self.in_comma = False
        self.in_preamble = False
        self.current_article_num = None
        self.current_comma_num = None
        self.in_ins = False  # Modifiche legislative

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')

        # Numero articolo
        if 'article-num-akn' in class_name:
            self.in_article = True
            self.current_text = StringIO()

        # Rubrica articolo (titolo)
        elif 'article-pre-comma-text-akn' in class_name:
            self.current_text = StringIO()

        # Numero comma
        elif 'comma-num-akn' in class_name:
            self.in_comma = True
            self.current_text = StringIO()

        # Testo comma
        elif 'art_text_in_comma' in class_name:
            self.current_text = StringIO()

        # Modifica legislativa (da wrappare in (( )))
        elif 'ins-akn' in class_name or 'del-akn' in class_name:
            self.in_ins = True
            self.current_text.write("((")

        # Preambolo
        elif 'preamble' in class_name:
            self.in_preamble = True

    def handle_endtag(self, tag):
        # Fine modifica legislativa
        if self.in_ins and tag == 'div':
            self.current_text.write("))")
            self.in_ins = False

    def handle_data(self, data):
        # Ignora whitespace vuoto
        if data.strip():
            self.current_text.write(data.strip() + " ")

    def get_markdown(self, html):
        """Processa HTML e restituisce Markdown"""
        self.feed(html)

        # Post-processing: pulizia testo
        raw_md = "\n".join(self.md_lines)

        # Rimuovi whitespace multipli
        raw_md = re.sub(r'\s+', ' ', raw_md)
        # Rimuovi doppi (( ))
        raw_md = re.sub(r'\(\(\s*\(\(', '((', raw_md)
        raw_md = re.sub(r'\)\)\s*\)\)', '))', raw_md)

        return raw_md


def api_response_to_markdown(api_json):
    """
    Converte risposta JSON da API OpenData in Markdown

    Args:
        api_json: Dict con struttura {"data": {"atto": {...}}}

    Returns:
        str: Markdown formattato
    """
    atto = api_json.get('data', {}).get('atto', {})

    md_lines = []

    # === YAML Front Matter ===
    md_lines.append("---")
    md_lines.append(f"tipo: {atto.get('tipoProvvedimentoDescrizione', '')}")
    md_lines.append(f"numero: {atto.get('numeroProvvedimento', '')}")
    md_lines.append(f"anno: {atto.get('annoProvvedimento', '')}")
    md_lines.append(f"dataGU: {atto.get('annoGU', '')}-{atto.get('meseGU', ''):02d}-{atto.get('giornoGU', ''):02d}")
    md_lines.append(f"codiceRedazionale: (non disponibile in response)")
    md_lines.append("---")
    md_lines.append("")

    # === Titolo ===
    titolo = atto.get('titolo', '')
    md_lines.append(f"# {titolo}")
    md_lines.append("")

    # === Sottotitolo (pulito da HTML) ===
    sottotitolo = atto.get('sottoTitolo', '')
    if sottotitolo:
        # Rimuovi tag HTML semplici
        sottotitolo_clean = re.sub(r'<[^>]+>', '', sottotitolo)
        sottotitolo_clean = re.sub(r'\s+', ' ', sottotitolo_clean).strip()
        md_lines.append(f"**{sottotitolo_clean}**")
        md_lines.append("")

    # === Articolato (HTML → Markdown) ===
    html_content = atto.get('articoloHtml', '')

    if html_content:
        # Parsing HTML con Beautiful Soup sarebbe meglio, ma per POC usiamo regex
        md_lines.append(convert_article_html_simple(html_content))

    return "\n".join(md_lines)


def convert_article_html_simple(html):
    """
    Conversione semplificata HTML → Markdown usando regex
    (Per produzione usare BeautifulSoup o lxml)
    """
    lines = []

    # Estrai articoli
    articles = re.findall(
        r'<h2[^>]*id="art_(\d+)"[^>]*>Art\.\s*(\d+)</h2>(.*?)(?=<h2[^>]*id="art_|$)',
        html,
        re.DOTALL
    )

    for art_id, art_num, art_content in articles:
        lines.append(f"## Art. {art_num}")
        lines.append("")

        # Estrai rubrica (titolo articolo)
        rubrica_match = re.search(
            r'<div class="article-pre-comma-text-akn"[^>]*>(.*?)</div>',
            art_content,
            re.DOTALL
        )
        if rubrica_match:
            rubrica = rubrica_match.group(1)
            rubrica_clean = re.sub(r'<[^>]+>', '', rubrica)
            rubrica_clean = re.sub(r'\s+', ' ', rubrica_clean).strip()
            if rubrica_clean and rubrica_clean != ' ':
                lines.append(f"**({rubrica_clean})**")
                lines.append("")

        # Estrai commi
        commi = re.findall(
            r'<span class="comma-num-akn">(\d+)\.\s*</span><span class="art_text_in_comma">(.*?)</span>',
            art_content,
            re.DOTALL
        )

        for comma_num, comma_text in commi:
            # Pulisci HTML
            comma_clean = re.sub(r'<br\s*/?>', ' ', comma_text)

            # Gestisci modifiche legislative
            comma_clean = re.sub(
                r'<div class="ins-akn"[^>]*>(.*?)</div>',
                r'((\1))',
                comma_clean,
                flags=re.DOTALL
            )

            # Rimuovi tag HTML rimanenti
            comma_clean = re.sub(r'<[^>]+>', '', comma_clean)

            # Decodifica HTML entities
            comma_clean = comma_clean.replace('&Egrave;', 'È')
            comma_clean = comma_clean.replace('&egrave;', 'è')
            comma_clean = comma_clean.replace('&agrave;', 'à')
            comma_clean = comma_clean.replace('&igrave;', 'ì')
            comma_clean = comma_clean.replace('&ograve;', 'ò')
            comma_clean = comma_clean.replace('&ugrave;', 'ù')

            # Pulisci whitespace
            comma_clean = re.sub(r'\s+', ' ', comma_clean).strip()

            lines.append(f"{comma_num}. {comma_clean}")
            lines.append("")

    return "\n".join(lines)


# === TEST ===
if __name__ == "__main__":
    # Determina directory output (relativa allo script)
    SCRIPT_DIR = Path(__file__).parent
    OUTPUT_DIR = SCRIPT_DIR.parent / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Carica risposta API
    input_file = OUTPUT_DIR / "dettaglio_response.json"
    with open(input_file, 'r') as f:
        api_data = json.load(f)

    # Converti in Markdown
    markdown = api_response_to_markdown(api_data)

    # Salva output
    output_path = OUTPUT_DIR / "legge_stanca_from_api.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print("✅ Conversione completata")
    print(f"   Input:  {input_file}")
    print(f"   Output: {output_path}")
    print("\n" + "=" * 80)
    print("PREVIEW (prime 50 righe):")
    print("=" * 80)
    print("\n".join(markdown.split('\n')[:50]))
