import json
import os
import re
import sys
import time
import zipfile
from datetime import datetime
from io import BytesIO
from urllib.parse import parse_qs, urlparse

import requests

from .provvedimenti_api import extract_law_params_from_url
from .constants import (
    ALLOWED_DOMAINS,
    DEFAULT_TIMEOUT,
    VERSION,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
)


def normalize_normattiva_url(url):
    """
    Normalizza URL normattiva.it rimuovendo escape backslash.

    Args:
        url: URL string

    Returns:
        str: URL normalizzato
    """
    if not isinstance(url, str):
        return url

    return url.replace("\\", "")


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
        url = normalize_normattiva_url(url)
        parsed = urlparse(url)

        # Check scheme is HTTPS
        if parsed.scheme != "https":
            raise ValueError(
                f"Solo HTTPS è consentito. URL fornito usa: {parsed.scheme}"
            )

        # Check domain is in whitelist
        if parsed.netloc.lower() not in ALLOWED_DOMAINS:
            raise ValueError(
                f"Dominio non consentito: {parsed.netloc}. Domini permessi: {', '.join(ALLOWED_DOMAINS)}"
            )

        return True

    except Exception as e:
        raise ValueError(f"URL non valido: {e}")


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

    normalized = normalize_normattiva_url(input_str)

    # Check if it looks like a URL
    if not re.match(r"https?://(www\.)?normattiva\.it/", normalized, re.IGNORECASE):
        return False

    # Validate URL for security
    try:
        validate_normattiva_url(normalized)
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
    return "/esporta/attoCompleto" in url and is_normattiva_url(url)


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
    url = normalize_normattiva_url(url)

    # Reject export URLs as they require authentication
    if is_normattiva_export_url(url):
        print(
            "❌ ERRORE: Gli URL di esportazione atto intero (/esporta/attoCompleto) non sono supportati",
            file=sys.stderr,
        )
        print(
            "   perché richiedono autenticazione per il download XML.", file=sys.stderr
        )
        print("   Usa invece gli URL permalink (URN) come:", file=sys.stderr)
        print(
            "   https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:AAAA-MM-GG;N",
            file=sys.stderr,
        )
        return None, session

    # For permalink URLs, visit the page and extract parameters from HTML
    if not quiet:
        print(f"Caricamento pagina {url}...", file=sys.stderr)

    if session is None:
        session = requests.Session()

    headers = {
        "User-Agent": f"Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    }

    try:
        response = session.get(
            url, headers=headers, timeout=DEFAULT_TIMEOUT, verify=True
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel caricamento della pagina: {e}", file=sys.stderr)
        return None, session

    html = response.text

    # Prova a leggere direttamente il link caricaAKN (più affidabile)
    params = {}
    link_match = re.search(r'href="([^"]*caricaAKN[^"]*)"', html, re.I)
    if link_match:
        link = link_match.group(1).replace("&amp;", "&")
        parsed_link = urlparse(link)
        query = parse_qs(parsed_link.query)
        if "dataGU" in query:
            params["dataGU"] = query["dataGU"][0]
        if "codiceRedaz" in query:
            params["codiceRedaz"] = query["codiceRedaz"][0]
        if "dataVigenza" in query:
            params["dataVigenza"] = query["dataVigenza"][0]

        if all(k in params for k in ["dataGU", "codiceRedaz", "dataVigenza"]):
            return params, session

    # Se il link caricaAKN non è presente, ritorna None per tentare il fallback
    if not link_match:
        if not quiet:
            print(
                "⚠️  Link caricaAKN non trovato, tentativo con fallback...",
                file=sys.stderr,
            )
        return None, session

    # Estrai parametri dagli input hidden usando regex (fallback)

    # Cerca atto.dataPubblicazioneGazzetta
    match_gu = re.search(
        r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html
    )
    if match_gu:
        # Converti da formato YYYY-MM-DD a YYYYMMDD
        date_str = match_gu.group(1).replace("-", "")
        params["dataGU"] = date_str

    # Cerca atto.codiceRedazionale
    match_codice = re.search(
        r'name="atto\.codiceRedazionale"[^>]*value="([^"]+)"', html
    )
    if match_codice:
        params["codiceRedaz"] = match_codice.group(1)

    # Cerca la data di vigenza dall'input visibile
    match_vigenza = re.search(r'<input[^>]*value="(\d{2}/\d{2}/\d{4})"[^>]*>', html)
    if match_vigenza:
        # Converti da formato DD/MM/YYYY a YYYYMMDD
        date_parts = match_vigenza.group(1).split("/")
        params["dataVigenza"] = f"{date_parts[2]}{date_parts[1]}{date_parts[0]}"
    else:
        # Usa data odierna se non trovata
        params["dataVigenza"] = datetime.now().strftime("%Y%m%d")

    if not all(k in params for k in ["dataGU", "codiceRedaz", "dataVigenza"]):
        print(
            "Errore: impossibile estrarre tutti i parametri necessari", file=sys.stderr
        )
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
        "User-Agent": f"Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
        "Referer": "https://www.normattiva.it/",
    }

    try:
        response = session.get(
            url,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
            allow_redirects=True,
            verify=True,
        )
        response.raise_for_status()

        # Check file size before processing
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > MAX_FILE_SIZE_BYTES:
            print(
                f"❌ Errore: file troppo grande ({int(content_length) / 1024 / 1024:.1f}MB). Massimo consentito: {MAX_FILE_SIZE_MB}MB",
                file=sys.stderr,
            )
            return False

        # Verifica che sia XML
        if response.content[:5] == b"<?xml" or b"<akomaNtoso" in response.content[:500]:
            with open(output_path, "wb") as f:
                f.write(response.content)
            if not quiet:
                print(f"✅ File XML salvato in: {output_path}", file=sys.stderr)
            return True
        else:
            print(f"❌ Errore: la risposta non è un file XML valido", file=sys.stderr)
            # Salva comunque per debug
            debug_path = output_path + ".debug.html"
            with open(debug_path, "wb") as f:
                f.write(response.content)
            print(f"   Risposta salvata in: {debug_path}", file=sys.stderr)
            return False

    except requests.RequestException as e:
        print(f"❌ Errore durante il download: {e}", file=sys.stderr)
        return False


def download_akoma_ntoso_via_export(url, output_path, session=None, quiet=False):
    """
    Tenta il download Akoma Ntoso passando dal form di export HTML.

    Questo fallback è utile quando il link caricaAKN non è esposto pubblicamente.

    Args:
        url: URL normattiva.it dell'atto
        output_path: percorso dove salvare il file XML
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        tuple: (success, metadata, session)
    """
    if session is None:
        session = requests.Session()

    headers = {
        "User-Agent": f"Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
        "Referer": "https://www.normattiva.it/",
    }

    try:
        response = session.get(url, headers=headers, timeout=DEFAULT_TIMEOUT, verify=True)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel caricamento della pagina: {e}", file=sys.stderr)
        return False, None, session

    html = response.text
    export_meta = _extract_export_metadata(html)
    if not export_meta:
        print(
            "❌ ERRORE: impossibile estrarre i parametri per l'export HTML.",
            file=sys.stderr,
        )
        return False, None, session

    export_url = (
        "https://www.normattiva.it/atto/vediMenuExport?"
        f"atto.dataPubblicazioneGazzetta={export_meta['dataGU_human']}"
        f"&atto.codiceRedazionale={export_meta['codiceRedaz']}"
        "&currentSearch="
    )

    try:
        export_page = session.get(
            export_url,
            headers={**headers, "Referer": url},
            timeout=DEFAULT_TIMEOUT,
            verify=True,
        )
        export_page.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Errore nel caricamento del menu export: {e}", file=sys.stderr)
        return False, None, session

    payload = _build_export_payload(export_page.text)
    if not payload:
        print("❌ ERRORE: impossibile costruire payload export.", file=sys.stderr)
        return False, None, session

    # Forza export XML
    payload.append(("generaXml", "Esporta XML"))

    try:
        export_response = session.post(
            "https://www.normattiva.it/do/atto/export",
            data=payload,
            headers={**headers, "Referer": export_url},
            timeout=DEFAULT_TIMEOUT,
            verify=True,
        )
        export_response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Errore durante il download via export: {e}", file=sys.stderr)
        return False, None, session

    if (
        export_response.content[:5] == b"<?xml"
        or b"<akomaNtoso" in export_response.content[:500]
    ):
        with open(output_path, "wb") as f:
            f.write(export_response.content)
        if not quiet:
            print(f"✅ File XML (export) salvato in: {output_path}", file=sys.stderr)
        metadata = {
            "dataGU": export_meta["dataGU"],
            "codiceRedaz": export_meta["codiceRedaz"],
            "dataVigenza": export_meta["dataVigenza"],
            "url": url,
        }
        return True, metadata, session

    # Salva HTML di errore per debug
    debug_path = output_path + ".export.debug.html"
    with open(debug_path, "wb") as f:
        f.write(export_response.content)
    print("❌ Errore: export non ha restituito XML valido", file=sys.stderr)
    print(f"   Risposta salvata in: {debug_path}", file=sys.stderr)
    return False, None, session


def download_akoma_ntoso_via_opendata(url, output_path, session=None, quiet=False):
    """
    Tenta il download Akoma Ntoso via API OpenData (collezioni ZIP).

    Questo fallback è utile quando il link caricaAKN non è esposto pubblicamente.

    Args:
        url: URL normattiva.it dell'atto
        output_path: percorso dove salvare il file XML
        session: sessione requests da usare (opzionale)
        quiet: se True, stampa solo errori

    Returns:
        tuple: (success, metadata, session)
    """
    if session is None:
        session = requests.Session()

    headers = {
        "User-Agent": f"Akoma2MD/{VERSION} (https://github.com/ondata/akoma2md)",
        "Accept": "application/json",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    }

    if not quiet:
        print("🔄 Tentativo download via API OpenData...", file=sys.stderr)

    try:
        response = session.get(
            url, headers={**headers, "Accept": "text/html"}, timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel caricamento della pagina: {e}", file=sys.stderr)
        return False, None, session

    export_meta = _extract_export_metadata(response.text)
    if not export_meta:
        print(
            "❌ ERRORE: impossibile estrarre i parametri dalla pagina per l'API OpenData.",
            file=sys.stderr,
        )
        return False, None, session

    anno, numero = extract_law_params_from_url(url)
    if not anno or not numero:
        print(
            "❌ ERRORE: impossibile estrarre anno/numero provvedimento dall'URL.",
            file=sys.stderr,
        )
        return False, None, session

    base_url = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1"
    nuova_ricerca_url = f"{base_url}/api/v1/ricerca-asincrona/nuova-ricerca"

    payload = {
        "formato": "AKN",
        "richiestaExport": "M",
        "modalita": "C",
        "tipoRicerca": "A",
        "parametriRicerca": {
            "dataInizioPubblicazione": f"{export_meta['dataGU_human']}T00:00:00.000Z",
            "dataFinePubblicazione": f"{export_meta['dataGU_human']}T23:59:59.999Z",
            "numeroProvvedimento": int(numero),
            "annoProvvedimento": int(anno),
        },
    }

    relaxed_payload = {
        "formato": "AKN",
        "richiestaExport": "M",
        "modalita": "C",
        "tipoRicerca": "A",
        "parametriRicerca": {
            "numeroProvvedimento": int(numero),
            "annoProvvedimento": int(anno),
        },
    }

    def _run_async_search(search_payload):
        try:
            ricerca_response = session.post(
                nuova_ricerca_url,
                headers={**headers, "Content-Type": "application/json"},
                data=json.dumps(search_payload),
                timeout=DEFAULT_TIMEOUT,
            )
            ricerca_response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Errore avvio ricerca OpenData: {e}", file=sys.stderr)
            return None, None, None

        token = ricerca_response.text.strip().strip('"')
        if not token:
            print("❌ ERRORE: token ricerca OpenData non valido.", file=sys.stderr)
            return None, None, None

        # Conferma ricerca (opzionale)
        conferma_url = f"{base_url}/api/v1/ricerca-asincrona/conferma-ricerca"
        try:
            session.put(
                conferma_url,
                headers={**headers, "Content-Type": "application/json"},
                data=json.dumps({"token": token}),
                timeout=DEFAULT_TIMEOUT,
            )
        except requests.RequestException:
            pass

        status_url = f"{base_url}/api/v1/ricerca-asincrona/check-status/{token}"
        stato = None
        status_data = None

        if not quiet:
            print(
                "⏳ Preparazione collezione OpenData",
                end="",
                file=sys.stderr,
                flush=True,
            )

        for _ in range(60):
            try:
                status_response = session.get(
                    status_url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
                if status_response.status_code == 303:
                    stato = 3
                    break
                status_response.raise_for_status()
                status_data = status_response.json()
                stato = status_data.get("stato")
                if stato == 3:
                    break
            except requests.RequestException:
                pass

            if not quiet:
                print(".", end="", file=sys.stderr, flush=True)
            time.sleep(2)

        if not quiet:
            print()  # New line after progress dots

        return stato, status_data, token

    payloads = [payload, relaxed_payload]
    download_url = None
    selected = None

    for idx, current_payload in enumerate(payloads):
        stato, status_data, token = _run_async_search(current_payload)
        if stato != 3:
            if idx == 0:
                continue
            print(
                "❌ ERRORE: ricerca OpenData non completata in tempo utile.",
                file=sys.stderr,
            )
            return False, None, session

        if status_data and status_data.get("totAtti") == 0:
            if idx == 0:
                if not quiet:
                    print(
                        "⚠️  Ricerca OpenData senza risultati, ritento senza filtro data...",
                        file=sys.stderr,
                    )
                continue
            print(
                "❌ ERRORE: ricerca OpenData non ha restituito risultati.",
                file=sys.stderr,
            )
            return False, None, session

        download_url = (
            f"{base_url}/api/v1/collections/download/collection-asincrona/{token}"
        )

        try:
            download_response = session.get(
                download_url, headers=headers, timeout=DEFAULT_TIMEOUT
            )
            download_response.raise_for_status()
        except requests.RequestException as e:
            if idx == 0:
                if not quiet:
                    print(
                        "⚠️  Errore download collezione OpenData, ritento senza filtro data...",
                        file=sys.stderr,
                    )
                continue
            print(f"❌ Errore download collezione OpenData: {e}", file=sys.stderr)
            return False, None, session

        try:
            with zipfile.ZipFile(BytesIO(download_response.content)) as zf:
                target_date = _parse_yyyymmdd(export_meta.get("dataVigenza"))
                selected = _select_akoma_file_from_zip(zf, target_date)
                if not selected:
                    if idx == 0:
                        if not quiet:
                            print(
                                "⚠️  ZIP OpenData senza XML AKN, ritento senza filtro data...",
                                file=sys.stderr,
                            )
                        continue
                    print(
                        "❌ ERRORE: nessun XML Akoma Ntoso trovato nel pacchetto OpenData.",
                        file=sys.stderr,
                    )
                    return False, None, session
                with zf.open(selected) as src, open(output_path, "wb") as dst:
                    dst.write(src.read())
            break
        except zipfile.BadZipFile:
            if idx == 0:
                if not quiet:
                    print(
                        "⚠️  ZIP OpenData non valido, ritento senza filtro data...",
                        file=sys.stderr,
                    )
                continue
            print("❌ ERRORE: file ZIP OpenData non valido.", file=sys.stderr)
            return False, None, session

    if not selected:
        return False, None, session

    if not quiet:
        print(f"✅ File XML (OpenData) salvato in: {output_path}", file=sys.stderr)

    metadata = {
        "dataGU": export_meta["dataGU"],
        "codiceRedaz": export_meta["codiceRedaz"],
        "dataVigenza": export_meta["dataVigenza"],
        "url": url,
        "url_xml": download_url,
    }
    return True, metadata, session


def _extract_export_metadata(html):
    match_gu = re.search(
        r'name="atto\.dataPubblicazioneGazzetta"[^>]*value="([^"]+)"', html
    )
    match_codice = re.search(
        r'name="atto\.codiceRedazionale"[^>]*value="([^"]+)"', html
    )
    match_vigenza = re.search(
        r'<input[^>]*name="dataVigenza"[^>]*value="(\d{2}/\d{2}/\d{4})"',
        html,
    )

    if not match_gu or not match_codice:
        return None

    data_gu_human = match_gu.group(1)
    data_gu = data_gu_human.replace("-", "")
    codice = match_codice.group(1)

    if match_vigenza:
        date_parts = match_vigenza.group(1).split("/")
        data_vigenza = f"{date_parts[2]}{date_parts[1]}{date_parts[0]}"
    else:
        data_vigenza = datetime.now().strftime("%Y%m%d")

    return {
        "dataGU_human": data_gu_human,
        "dataGU": data_gu,
        "codiceRedaz": codice,
        "dataVigenza": data_vigenza,
    }


def _build_export_payload(html):
    form_match = re.search(
        r'<form[^>]*id="anteprima"[^>]*>(.*?)</form>',
        html,
        re.S | re.I,
    )
    if not form_match:
        return None

    form_html = form_match.group(1)
    inputs = re.findall(r"<input[^>]*>", form_html, re.I)
    payload = []

    for inp in inputs:
        name_match = re.search(r'name="([^"]+)"', inp, re.I)
        if not name_match:
            continue
        name = name_match.group(1)

        type_match = re.search(r'type="([^"]+)"', inp, re.I)
        input_type = type_match.group(1).lower() if type_match else ""

        value_match = re.search(r'value="([^"]*)"', inp, re.I)
        value = value_match.group(1) if value_match else ""

        # Skip submit controls; we'll add our own
        if input_type == "submit":
            continue

        # Include checked checkboxes only
        if input_type == "checkbox":
            if not re.search(r'checked', inp, re.I):
                continue

        payload.append((name, value))

    return payload


def _select_akoma_file_from_zip(zf, target_date):
    candidates = []
    originals = []
    for name in zf.namelist():
        lower = name.lower()
        if not lower.endswith(".xml"):
            continue
        if "vigenza_" in lower:
            match = re.search(r"VIGENZA_(\d{4}-\d{2}-\d{2})_V", name)
            if match:
                date_str = match.group(1)
                date_obj = _parse_iso_date(date_str)
                candidates.append((date_obj, name))
        elif "origin" in lower or "originale" in lower:
            originals.append(name)

    if candidates:
        candidates.sort(key=lambda x: x[0])
        if target_date:
            valid = [c for c in candidates if c[0] and c[0] <= target_date]
            if valid:
                return valid[-1][1]
        return candidates[-1][1]

    if originals:
        return originals[0]
    return None


def _parse_iso_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _parse_yyyymmdd(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except (ValueError, TypeError):
        return None
