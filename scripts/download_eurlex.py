#!/usr/bin/env python3
"""
Download documents from EUR-Lex in various formats.

This script downloads EU legal documents from EUR-Lex using their CELEX identifier.
Supports multiple formats: Formex XML, XHTML, and PDF.

Usage:
    python scripts/download_eurlex.py <CELEX> [--lang LANG] [--format FORMAT] [--output FILE]

Examples:
    python scripts/download_eurlex.py 32024L1385
    python scripts/download_eurlex.py 32024L1385 --lang IT --format xhtml
    python scripts/download_eurlex.py 32024L1385 --format fmx4 --output directive.xml
    python scripts/download_eurlex.py 32024L1385 --lang IT --format xhtml --to-markdown --output directive.md
"""

import sys
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import io
import os
import subprocess
import tempfile


# Mapping from 2-letter ISO codes to EUR-Lex 3-letter codes
LANG_MAP = {
    'BG': 'BUL',  # Bulgarian
    'ES': 'SPA',  # Spanish
    'CS': 'CES',  # Czech
    'DA': 'DAN',  # Danish
    'DE': 'DEU',  # German
    'ET': 'EST',  # Estonian
    'EL': 'ELL',  # Greek
    'EN': 'ENG',  # English
    'FR': 'FRA',  # French
    'GA': 'GLE',  # Irish
    'HR': 'HRV',  # Croatian
    'IT': 'ITA',  # Italian
    'LV': 'LAV',  # Latvian
    'LT': 'LIT',  # Lithuanian
    'HU': 'HUN',  # Hungarian
    'MT': 'MLT',  # Maltese
    'NL': 'NLD',  # Dutch
    'PL': 'POL',  # Polish
    'PT': 'POR',  # Portuguese
    'RO': 'RON',  # Romanian
    'SK': 'SLK',  # Slovak
    'SL': 'SLV',  # Slovenian
    'FI': 'FIN',  # Finnish
    'SV': 'SWE',  # Swedish
}


def get_lang_code(lang):
    """Convert 2-letter ISO code to EUR-Lex 3-letter code."""
    lang_upper = lang.upper()
    if len(lang_upper) == 3:
        return lang_upper  # Already 3-letter code
    return LANG_MAP.get(lang_upper, lang_upper)


def download_xml_notice(celex, language='EN'):
    """
    Download XML notice (metadata) for a EUR-Lex document.
    
    Args:
        celex: CELEX number (e.g., '32024L1385')
        language: Language code (default: 'EN')
    
    Returns:
        XML string containing document metadata
    """
    url = f"https://eur-lex.europa.eu/legal-content/{language}/TXT/XML/?uri=CELEX:{celex}"
    
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"Error downloading XML notice: {e}", file=sys.stderr)
        sys.exit(1)


def find_download_url(xml_notice, language, format_type):
    """
    Extract download URL from XML notice for specific format and language.
    
    Args:
        xml_notice: XML notice string
        language: Language code (e.g., 'EN', 'IT', 'ENG', 'ITA')
        format_type: Format type ('fmx4', 'xhtml', 'pdfa2a')
    
    Returns:
        Download URL string or None if not found
    """
    try:
        root = ET.fromstring(xml_notice)
    except ET.ParseError as e:
        print(f"Error parsing XML notice: {e}", file=sys.stderr)
        return None
    
    # Convert to 3-letter code if necessary
    lang_code = get_lang_code(language)
    
    # EUR-Lex URLs are in EXPRESSION_MANIFESTED_BY_MANIFESTATION/SAMEAS/URI/VALUE  # Pattern: L_NNNN.{LANG}.{FORMAT}[.filename.zip]
    pattern = f'.{lang_code}.{format_type}'
    
    # Collect all matching URLs
    candidates = []
    
    for url_elem in root.findall('.//EXPRESSION_MANIFESTED_BY_MANIFESTATION//URI/VALUE'):
        url = url_elem.text
        if pattern in url:
            candidates.append(url)
    
    # Fallback: also check in regular MANIFESTATION elements
    for manif in root.findall('.//MANIFESTATION'):
        for url_elem in manif.findall('.//URI/VALUE'):
            url = url_elem.text
            if pattern in url:
                candidates.append(url)
    
    if not candidates:
        return None
    
    # Prefer URLs ending with .zip for fmx4 format (contains actual XML file)
    # For other formats, prefer longer URLs (more specific)
    if format_type == 'fmx4':
        zip_urls = [u for u in candidates if u.endswith('.zip')]
        if zip_urls:
            return zip_urls[0]
    
    # Return longest URL (most specific)
    return max(candidates, key=len)


def download_document(download_url):
    """
    Download document from EUR-Lex following redirects.
    
    Args:
        download_url: URL to download from
    
    Returns:
        Document content as bytes
    """
    try:
        with urllib.request.urlopen(download_url) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        print(f"Error downloading document: {e}", file=sys.stderr)
        sys.exit(1)


def extract_formex_zip(zip_content):
    """
    Extract Formex XML from ZIP archive.
    
    Args:
        zip_content: ZIP file content as bytes
    
    Returns:
        XML content as string
    """
    try:
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
            # Find main document file (not toc or doc metadata)
            files = [f for f in zf.namelist() 
                    if f.endswith('.fmx.xml') and 'toc' not in f.lower() and 'doc' not in f.lower()]
            
            if not files:
                print("Error: No Formex XML file found in ZIP", file=sys.stderr)
                return None
            
            # Return first matching file
            return zf.read(files[0]).decode('utf-8')
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid ZIP archive", file=sys.stderr)
        return None


def convert_xhtml_to_markdown(xhtml_bytes, output_path, lua_filter, extract_media):
    """Convert XHTML bytes to Markdown using pandoc and a Lua filter."""
    if not os.path.isfile(lua_filter):
        print(f"Error: Lua filter not found: {lua_filter}", file=sys.stderr)
        return 1

    temp_in = None
    temp_out = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xhtml") as f:
            f.write(xhtml_bytes)
            temp_in = f.name

        cmd = [
            "pandoc",
            "-f",
            "html",
            "-t",
            "gfm",
            "--wrap=none",
            "--lua-filter",
            lua_filter,
            temp_in,
        ]
        if extract_media:
            cmd.extend(["--extract-media", extract_media])

        if output_path:
            cmd.extend(["-o", output_path])
            result = subprocess.run(cmd, check=False)
            if result.returncode != 0:
                print("Error: pandoc failed", file=sys.stderr)
                return result.returncode
            with open(output_path, "r", encoding="utf-8") as f:
                cleaned = strip_markdown_comments(f.read())
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            return 0

        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as f:
            temp_out = f.name
        cmd.extend(["-o", temp_out])
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            print("Error: pandoc failed", file=sys.stderr)
            return result.returncode
        with open(temp_out, "r", encoding="utf-8") as f:
            sys.stdout.write(strip_markdown_comments(f.read()))
        return 0
    except FileNotFoundError:
        print("Error: pandoc not found. Install pandoc to enable --to-markdown.", file=sys.stderr)
        return 1
    finally:
        if temp_in and os.path.exists(temp_in):
            os.unlink(temp_in)
        if temp_out and os.path.exists(temp_out):
            os.unlink(temp_out)


def strip_markdown_comments(text):
    """Remove placeholder HTML comments inserted by pandoc in lists."""
    lines = []
    for line in text.splitlines():
        if line.strip() == "<!-- -->":
            continue
        lines.append(line)
    return "\n".join(lines) + "\n"


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_filter = os.path.join(script_dir, "eurlex_clean.lua")

    parser = argparse.ArgumentParser(
        description='Download documents from EUR-Lex',
        epilog='Example: %(prog)s 32024L1385 --lang EN --format fmx4'
    )
    parser.add_argument('celex', help='CELEX number (e.g., 32024L1385)')
    parser.add_argument('--lang', default='EN', 
                       help='Language code (default: EN). Examples: EN, IT, FR, DE')
    parser.add_argument('--format', default='fmx4', choices=['fmx4', 'xhtml', 'pdfa2a'],
                       help='Output format (default: fmx4)')
    parser.add_argument('--output', '-o', 
                       help='Output file path (default: stdout for text formats, auto-named for binary)')
    parser.add_argument('--list-formats', action='store_true',
                       help='List available formats and exit')
    parser.add_argument('--to-markdown', action='store_true',
                        help='Convert XHTML to Markdown using pandoc')
    parser.add_argument('--markdown-output',
                        help='Markdown output path (default: stdout)')
    parser.add_argument('--lua-filter', default=default_filter,
                        help='Lua filter for pandoc (default: scripts/eurlex_clean.lua)')
    parser.add_argument('--extract-media',
                        help='Directory for extracted media (passed to pandoc)')
    
    args = parser.parse_args()
    
    if args.list_formats:
        print("Available formats:")
        print("  fmx4     - Formex XML (structured XML, best for processing)")
        print("  xhtml    - XHTML (web format)")
        print("  pdfa2a   - PDF/A (official authentic version)")
        return 0
    
    # Step 1: Download XML notice
    print(f"Downloading XML notice for {args.celex}...", file=sys.stderr)
    xml_notice = download_xml_notice(args.celex, args.lang)
    
    # Step 2: Find download URL
    print(f"Looking for {args.format} format in {args.lang}...", file=sys.stderr)
    download_url = find_download_url(xml_notice, args.lang, args.format)
    
    if not download_url:
        print(f"Error: Format {args.format} not available for language {args.lang}", 
              file=sys.stderr)
        print(f"Try --list-formats to see available formats", file=sys.stderr)
        return 1
    
    print(f"Download URL: {download_url}", file=sys.stderr)
    
    # Step 3: Download document
    print(f"Downloading document...", file=sys.stderr)
    content = download_document(download_url)
    
    # Step 4: Process format-specific content
    if args.format == 'fmx4':
        # Extract from ZIP
        content = extract_formex_zip(content)
        if content is None:
            return 1
        content = content.encode('utf-8')

    if args.to_markdown:
        if args.format != "xhtml":
            print("Error: --to-markdown requires --format xhtml", file=sys.stderr)
            return 1
        md_output = args.markdown_output or args.output
        return convert_xhtml_to_markdown(
            content,
            md_output,
            args.lua_filter,
            args.extract_media,
        )
    
    # Step 5: Write output
    if args.output:
        # Write to file
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(args.output, mode) as f:
            f.write(content)
        print(f"Document saved to {args.output}", file=sys.stderr)
    else:
        # Write to stdout
        if isinstance(content, bytes):
            sys.stdout.buffer.write(content)
        else:
            print(content)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
