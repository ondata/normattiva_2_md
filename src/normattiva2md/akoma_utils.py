import re
import sys
import xml.etree.ElementTree as ET
from .constants import AKN_NAMESPACE
from .normattiva_api import is_normattiva_url


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

    match = re.search(
        r"~art(\d+(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies|vices|tricies|quadragies)?)",
        url,
        re.IGNORECASE,
    )
    if match:
        article_num = match.group(1)
        # Converti in formato eId: art_3, art_16bis, etc.
        return f"art_{article_num}"

    return None


def akoma_uri_to_normattiva_url(akoma_uri):
    """
    Converte un URI Akoma Ntoso in URL normattiva.it.

    Args:
        akoma_uri: URI Akoma Ntoso (es. /akn/it/act/legge/stato/2003-07-29/229/!main#art_1)

    Returns:
        str or None: URL normattiva.it corrispondente o None se conversione fallisce
    """
    try:
        # Gestisci riferimenti ad articoli specifici (#art_X)
        article_ref = None
        if "#art_" in akoma_uri:
            akoma_uri, article_part = akoma_uri.split("#art_", 1)
            # Estrai il numero dell'articolo (può contenere lettere come 1-bis, 16-ter, etc.)
            article_num = article_part.split("-")[
                0
            ]  # Prendi solo la parte prima di eventuali trattini
            article_ref = f"~art{article_num}"

        # Esempio: /akn/it/act/legge/stato/2003-07-29/229/!main
        # Diventa: https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2003-07-29;229
        parts = akoma_uri.strip("/").split("/")
        if (
            len(parts) >= 6
            and parts[0] == "akn"
            and parts[1] == "it"
            and parts[2] == "act"
        ):
            tipo = parts[3]  # legge, decreto-legge, etc.
            giurisdizione = parts[4]  # stato
            data = parts[5]  # 2003-07-29
            numero = parts[6]  # 229

            # Gestisci tipi diversi
            if tipo == "legge":
                urn = f"urn:nir:stato:legge:{data.replace('-', '-')};{numero}"
            elif tipo in ("decreto-legge", "decretoLegge"):
                urn = f"urn:nir:stato:decreto-legge:{data.replace('-', '-')};{numero}"
            elif tipo == "decretoLegislativo":
                urn = f"urn:nir:stato:decreto.legislativo:{data.replace('-', '-')};{numero}"
            elif tipo == "costituzione":
                urn = f"urn:nir:stato:costituzione:{data.replace('-', '-')}"
            elif tipo == "decretoDelPresidenteDellaRepubblica":
                urn = f"urn:nir:stato:decreto.del.presidente.della.repubblica:{data.replace('-', '-')};{numero}"
            elif tipo == "regioDecreto":
                urn = f"urn:nir:stato:regio.decreto:{data.replace('-', '-')};{numero}"
            elif tipo == "codice.civile":
                urn = f"urn:nir:stato:codice.civile:{data.replace('-', '-')}"
            elif tipo == "codice.procedura.civile":
                urn = f"urn:nir:stato:codice.procedura.civile:{data.replace('-', '-')}"
            else:
                return None

            url = f"https://www.normattiva.it/uri-res/N2Ls?{urn}"
            # Only add article reference for document types that support it
            # Costituzioni and codes don't support article-specific links
            if article_ref and tipo not in (
                "costituzione",
                "codice.civile",
                "codice.procedura.civile",
            ):
                url += article_ref
            return url
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
        for element in root.findall(".//*[@href]"):
            href = element.get("href")
            if href and href.startswith("/akn/"):
                akoma_uris.add(href)

    except ET.ParseError:
        pass
    except Exception:
        pass

    return akoma_uris


def extract_cited_laws(xml_file_path):
    """
    Estrae tutti gli URL delle leggi citate da un file XML Akoma Ntoso.
    Raggruppa per legge base, ignorando riferimenti a articoli specifici.

    Args:
        xml_file_path: percorso al file XML

    Returns:
        set: insieme di URL unici delle leggi citate (senza riferimenti ad articoli)
    """
    cited_laws = set()

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Trova tutti i tag <ref> con href
        for ref in root.findall(".//akn:ref[@href]", AKN_NAMESPACE):
            href = ref.get("href")
            if href and href.startswith("/akn/"):
                # Converti URI Akoma Ntoso in URL normattiva.it
                url = akoma_uri_to_normattiva_url(href)
                if url and is_normattiva_url(url):
                    # Rimuovi riferimenti ad articoli specifici (~artX) per raggruppare per legge
                    # Questo evita di scaricare la stessa legge più volte per articoli diversi
                    law_url = url.split("~")[0] if "~" in url else url
                    cited_laws.add(law_url)

    except ET.ParseError as e:
        print(f"Errore parsing XML per riferimenti: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Errore estrazione riferimenti: {e}", file=sys.stderr)

    return cited_laws
