"""
Module for searching and extracting legislative implementation measures (provvedimenti attuativi)
from programmagoverno.gov.it
"""

import re
import sys
import csv
import os
import requests
from .constants import VERSION

BASE_URL = "https://www.programmagoverno.gov.it/it/ricerca-provvedimenti/"
DEFAULT_TIMEOUT = 15


def extract_law_params_from_url(url):
    """
    Extract law year and number from normattiva.it URL

    Args:
        url: normattiva.it URL containing URN

    Returns:
        tuple: (year, number) or (None, None) if not found
    """
    # Match URN patterns like: urn:nir:stato:legge:2024;207 or urn:nir:stato:legge:2024-03-01;207
    urn_match = re.search(r'urn:nir:stato:[^:]+:(\d{4})(?:-\d{2}-\d{2})?[;-](\d+)', url)
    if urn_match:
        return urn_match.group(1), urn_match.group(2)
    return None, None


def build_search_url(numero, anno, page=None):
    """
    Build search URL for programmagoverno.gov.it

    Args:
        numero: Law number
        anno: Law year
        page: Page number (0-indexed), None for first page

    Returns:
        str: Full search URL
    """
    params = f"numero={numero}&anno={anno}&oggetto="
    if page is not None and page > 0:
        params = f"page={page}&" + params
    return f"{BASE_URL}?{params}"


def fetch_provvedimenti_page(numero, anno, page=0, quiet=False):
    """
    Fetch a single search results page from programmagoverno.gov.it

    Args:
        numero: Law number
        anno: Law year
        page: Page number (0-indexed)
        quiet: If True, suppress progress messages

    Returns:
        str: HTML content or None on error
    """
    url = build_search_url(numero, anno, page)

    if not quiet:
        if page == 0:
            print(f"Fetching implementation measures for law {numero}/{anno}...", file=sys.stderr)
        else:
            print(f"Fetching page {page}...", file=sys.stderr)

    headers = {
        "User-Agent": f"normattiva2md/{VERSION} (https://github.com/ondata/normattiva_2_md)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    }

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}", file=sys.stderr)
        return None


def parse_provvedimenti_html(html_content):
    """
    Parse HTML content and extract implementation measures data

    Args:
        html_content: HTML string from programmagoverno.gov.it

    Returns:
        list: List of dicts with keys: dettagli, governo, fonte_provvedimento,
              oggetto, provvedimento_previsto, adozione, link_al_provvedimento
    """
    results = []

    # Check for "Nessun risultato" message
    if "Nessun risultato." in html_content or "Nessun provvedimento trovato" in html_content:
        return results

    # Find table rows - pattern matches <tr> tags with content
    # Skip header row by looking for <td> tags (data rows)
    row_pattern = r'<tr>(.*?)</tr>'
    all_rows = re.findall(row_pattern, html_content, re.DOTALL | re.IGNORECASE)

    # Filter to only rows with <td> (data rows, not headers)
    data_rows = [row for row in all_rows if '<td' in row.lower()]

    for row_content in data_rows:
        # Extract all <td> cells from this row
        cell_pattern = r'<td[^>]*>(.*?)</td>'
        cells = re.findall(cell_pattern, row_content, re.DOTALL | re.IGNORECASE)

        if len(cells) >= 7:  # Should have 7 columns
            # Extract text from cells, removing HTML tags
            def clean_cell(text):
                # Remove HTML tags
                text = re.sub(r'<[^>]+>', '', text)
                # Decode HTML entities
                text = text.replace('&#xB0;', '°')
                text = text.replace('&#x27;', "'")
                text = text.replace('&#xE0;', 'à')
                text = text.replace('&#xE8;', 'è')
                text = text.replace('&#xE9;', 'é')
                text = text.replace('&#xEC;', 'ì')
                text = text.replace('&#xF2;', 'ò')
                text = text.replace('&#xF9;', 'ù')
                text = text.replace('&#x22EF;', '⋯')
                text = text.replace('&amp;', '&')
                text = text.replace('&quot;', '"')
                text = text.replace('&lt;', '<')
                text = text.replace('&gt;', '>')
                # Strip whitespace
                return text.strip()

            # Extract link from first cell (dettagli column) - keep the icon/link text
            dettagli_text = clean_cell(cells[0])
            link_match = re.search(r'href="([^"]+)"', cells[0])
            if link_match:
                # Store the full URL to detail page
                dettagli = "https://www.programmagoverno.gov.it" + link_match.group(1)
            else:
                dettagli = dettagli_text

            # Extract link from last cell (link al provvedimento) if present
            link_al_provvedimento = ""
            if len(cells) > 6:
                link_match_prov = re.search(r'href="([^"]+)"', cells[6])
                if link_match_prov:
                    link_al_provvedimento = cells[6]  # Keep raw HTML for now or extract properly
                    # Try to extract URL
                    url_match = re.search(r'href="([^"]+)"', cells[6])
                    if url_match:
                        link_url = url_match.group(1)
                        if link_url.startswith('http'):
                            link_al_provvedimento = link_url
                        else:
                            link_al_provvedimento = "https://www.programmagoverno.gov.it" + link_url

            result = {
                "dettagli": dettagli,  # Column 0 - details link icon
                "governo": clean_cell(cells[1]),  # Column 1 - Government
                "fonte_provvedimento": clean_cell(cells[2]),  # Column 2 - Source law
                "oggetto": clean_cell(cells[3]),  # Column 3 - Subject/description
                "provvedimento_previsto": clean_cell(cells[4]),  # Column 4 - Expected measure type
                "adozione": clean_cell(cells[5]),  # Column 5 - Adoption status
                "link_al_provvedimento": link_al_provvedimento,  # Column 6 - Link to measure
            }
            results.append(result)

    return results


def has_next_page(html_content):
    """
    Detect if there are more pages of results

    Args:
        html_content: HTML string

    Returns:
        bool: True if there's a next page link
    """
    # Look for pagination links with higher page numbers
    # or "next page" style links
    next_patterns = [
        r'href="[^"]*page=\d+',  # Any page link with page parameter
        r'pagination-next',  # Common pagination class
        r'aria-label="[Pp]agina successiva"',  # Italian "next page"
        r'>Avanti<',  # Italian "forward"
        r'>Next<',
    ]

    for pattern in next_patterns:
        if re.search(pattern, html_content, re.IGNORECASE):
            # Additional check: make sure we're not on the last page
            # by looking for disabled next button
            if not re.search(r'pagination-next[^>]*disabled', html_content, re.IGNORECASE):
                return True

    return False


def fetch_all_provvedimenti(numero, anno, quiet=False):
    """
    Fetch all pages of implementation measures for a given law

    Args:
        numero: Law number
        anno: Law year
        quiet: If True, suppress progress messages

    Returns:
        list: All implementation measures across all pages,
              or None on error
    """
    all_results = []
    page = 0
    max_pages = 100  # Safety limit to prevent infinite loops

    while page < max_pages:
        html_content = fetch_provvedimenti_page(numero, anno, page, quiet)

        if html_content is None:
            # Network error
            if page == 0:
                return None  # Fatal error on first page
            else:
                # Partial results fetched, return what we have
                print(f"Warning: Failed to fetch page {page}, returning {len(all_results)} results", file=sys.stderr)
                break

        page_results = parse_provvedimenti_html(html_content)

        if not page_results and page == 0:
            # No results found at all
            return []

        if not page_results and page > 0:
            # End of results
            break

        all_results.extend(page_results)

        # Check for next page
        if not has_next_page(html_content):
            break

        page += 1

    return all_results


def determine_csv_path(output_file, anno, numero):
    """
    Determine where to save the CSV file

    Args:
        output_file: Markdown output file path (or None for stdout)
        anno: Law year
        numero: Law number

    Returns:
        str: Path where CSV should be saved
    """
    csv_filename = f"{anno}_{numero}_provvedimenti.csv"

    if output_file:
        # Save in same directory as output file
        output_dir = os.path.dirname(output_file)
        if output_dir:
            return os.path.join(output_dir, csv_filename)
        else:
            # output_file is just a filename in current dir
            return csv_filename
    else:
        # stdout mode - use current working directory
        return csv_filename


def prompt_overwrite(filepath):
    """
    Prompt user to confirm overwrite of existing file

    Args:
        filepath: Path to file that would be overwritten

    Returns:
        bool: True if user confirms, False otherwise
    """
    while True:
        response = input(f"File {filepath} already exists. Overwrite? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            print("Aborted.", file=sys.stderr)
            return False
        else:
            print("Please answer 'y' or 'n'", file=sys.stderr)


def export_provvedimenti_csv(data, filepath):
    """
    Export implementation measures data to CSV file

    Args:
        data: List of dicts with implementation measures
        filepath: Path to output CSV file

    Returns:
        bool: True on success, False on error
    """
    if not data:
        return False

    fieldnames = [
        "dettagli",
        "governo",
        "fonte_provvedimento",
        "oggetto",
        "provvedimento_previsto",
        "adozione",
        "link_al_provvedimento",
    ]

    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(filepath)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(data)

        return True
    except IOError as e:
        print(f"Error writing CSV file {filepath}: {e}", file=sys.stderr)
        return False


def write_provvedimenti_csv(data, anno, numero, output_file, quiet=False):
    """
    Main orchestrator for CSV export with all logic

    Args:
        data: List of implementation measures
        anno: Law year
        numero: Law number
        output_file: Markdown output file (or None)
        quiet: If True, suppress non-essential output

    Returns:
        bool: True on success, False on error or user abort
    """
    if not data:
        return False

    csv_path = determine_csv_path(output_file, anno, numero)

    # Check if file exists and prompt for overwrite
    if os.path.exists(csv_path):
        if not prompt_overwrite(csv_path):
            return False

    # Write CSV
    success = export_provvedimenti_csv(data, csv_path)

    if success and not quiet:
        print(f"Exported {len(data)} implementation measures to {csv_path}", file=sys.stderr)

    return success
