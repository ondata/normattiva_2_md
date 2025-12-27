import xml.etree.ElementTree as ET
from datetime import datetime
from .constants import AKN_NAMESPACE, GU_NAMESPACE, ELI_NAMESPACE

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
        dataVigenza_formatted = (
            f"{dataVigenza[:4]}-{dataVigenza[4:6]}-{dataVigenza[6:]}"
        )

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
    meta = root.find(".//akn:meta", AKN_NAMESPACE)
    if meta is None:
        return metadata

    # Extract codiceRedaz (eli:id_local) - try both eli and gu namespaces
    id_local = meta.find(".//eli:id_local", ELI_NAMESPACE)
    if id_local is None:
        id_local = meta.find(".//gu:id_local", GU_NAMESPACE)
    if id_local is not None and id_local.text:
        metadata["codiceRedaz"] = id_local.text.strip()

    # Extract dataGU (eli:date_document) - try both eli and gu namespaces
    date_doc = meta.find(".//eli:date_document", ELI_NAMESPACE)
    if date_doc is None:
        date_doc = meta.find(".//gu:date_document", GU_NAMESPACE)
    if date_doc is not None and date_doc.text:
        # Convert from YYYY-MM-DD to YYYYMMDD format
        try:
            date_obj = datetime.strptime(date_doc.text.strip(), "%Y-%m-%d")
            metadata["dataGU"] = date_obj.strftime("%Y%m%d")
        except ValueError:
            metadata["dataGU"] = date_doc.text.strip()

    # Extract dataVigenza from FRBRExpression date
    frbr_expr = meta.find(".//akn:FRBRExpression", AKN_NAMESPACE)
    if frbr_expr is not None:
        date_expr = frbr_expr.find("./akn:FRBRdate", AKN_NAMESPACE)
        if date_expr is not None and date_expr.get("date"):
            # Convert from YYYY-MM-DD to YYYYMMDD format
            try:
                date_obj = datetime.strptime(date_expr.get("date"), "%Y-%m-%d")
                metadata["dataVigenza"] = date_obj.strftime("%Y%m%d")
            except ValueError:
                metadata["dataVigenza"] = date_expr.get("date")

    # Extract canonical URN-NIR from FRBRWork
    frbr_work = meta.find(".//akn:FRBRWork", AKN_NAMESPACE)
    if frbr_work is not None:
        urn_alias = frbr_work.find('./akn:FRBRalias[@name="urn:nir"]', AKN_NAMESPACE)
        if urn_alias is not None and urn_alias.get("value"):
            metadata["urn_nir"] = urn_alias.get("value")

    # Construct URLs if we have the required metadata
    if (
        metadata.get("dataGU")
        and metadata.get("codiceRedaz")
        and metadata.get("dataVigenza")
    ):
        base_url = "https://www.normattiva.it/uri-res/N2Ls"
        urn = f"urn:nir:stato:legge:{metadata['dataGU'][:4]}-{metadata['dataGU'][4:6]}-{metadata['dataGU'][6:]};{metadata['codiceRedaz']}"
        metadata["url"] = f"{base_url}?{urn}"

        metadata["url_xml"] = (
            f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={metadata['dataGU']}&codiceRedaz={metadata['codiceRedaz']}&dataVigenza={metadata['dataVigenza']}"
        )

        # Build permanent URL using canonical URN-NIR with vigenza date
        if metadata.get("urn_nir"):
            # Convert dataVigenza to YYYY-MM-DD format for the URL
            try:
                vigenza_obj = datetime.strptime(metadata["dataVigenza"], "%Y%m%d")
                vigenza_formatted = vigenza_obj.strftime("%Y-%m-%d")
                metadata["url_permanente"] = (
                    f"{base_url}?{metadata['urn_nir']}!vig={vigenza_formatted}"
                )
            except ValueError:
                # Fallback to old method if date conversion fails
                metadata["url_permanente"] = build_permanent_url(
                    metadata["dataGU"], metadata["codiceRedaz"], metadata["dataVigenza"]
                )
        else:
            # Fallback to old method if URN-NIR not found
            metadata["url_permanente"] = build_permanent_url(
                metadata["dataGU"], metadata["codiceRedaz"], metadata["dataVigenza"]
            )

    return metadata


def construct_article_eid(user_input):
    """
    Costruisce l'eId di un articolo dal formato user-friendly.

    Args:
        user_input: stringa con numero articolo ed eventuale estensione (es: "4", "16bis", "3ter")

    Returns:
        str: eId formato Akoma Ntoso (es: "art_4", "art_16bis") o None se formato invalido
    """
    import re

    if not user_input:
        return None

    # Normalizza input: trim e lowercase
    user_input = user_input.strip().lower()

    # Valida formato: numero seguito da lettere opzionali
    pattern = r'^(\d+)([a-z]*)$'
    match = re.match(pattern, user_input)

    if not match:
        return None

    numero = match.group(1)
    estensione = match.group(2)

    # Costruisci eId (con trattino per estensioni, formato Akoma Ntoso)
    if estensione:
        return f"art_{numero}-{estensione}"
    else:
        return f"art_{numero}"


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
            new_root.set(f"xmlns:{prefix}", uri)
        else:
            new_root.set("xmlns", uri)

    # Copia meta section
    meta = root.find(".//akn:meta", ns)
    if meta is not None:
        new_root.append(meta)

    # Crea un nuovo body con solo l'articolo
    # Copy namespace from the original body
    original_body = root.find(".//akn:body", ns)
    if original_body is not None:
        body = ET.SubElement(new_root, original_body.tag, original_body.attrib)
    else:
        body = ET.SubElement(new_root, "body")
    body.append(article)

    return new_root
