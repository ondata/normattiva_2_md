import os
import sys
import time
import tempfile
from .normattiva_api import extract_params_from_normattiva_url, download_akoma_ntoso
from .akoma_utils import extract_cited_laws
from .markdown_converter import convert_akomantoso_to_markdown_improved


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

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# Raccolta Legislativa\n\n")
        f.write(
            f"**Legge principale:** {main_params['codiceRedaz']} del {main_params['dataGU']}\n\n"
        )
        f.write(f"**Le leggi citate scaricate:** {successful}\n\n")
        f.write(f"**Le leggi citate non scaricate:** {failed}\n\n")

        if successful > 0:
            f.write("## Leggi Citare Scaricate\n\n")
            refs_path = os.path.join(folder_path, "refs")
            for filename in sorted(os.listdir(refs_path)):
                if filename.endswith(".md"):
                    f.write(f"- [{filename}](./refs/{filename})\n")
            f.write("\n")

        f.write(f"[Legge principale](./main.md)\n")


def convert_with_references(
    url, output_dir=None, quiet=False, keep_xml=False, force_complete=False
):
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
            print(
                "❌ Impossibile estrarre parametri dalla legge principale",
                file=sys.stderr,
            )
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
            print(
                "❌ Errore durante il download della legge principale", file=sys.stderr
            )
            return False

        # Estrai riferimenti dalla legge principale
        if not quiet:
            print(
                f"🔗 Estrazione riferimenti dalla legge principale...", file=sys.stderr
            )

        cited_urls = extract_cited_laws(xml_temp_path)
        if not quiet:
            print(f"📋 Trovate {len(cited_urls)} leggi uniche citate", file=sys.stderr)

        # Scarica e converte legge principale
        main_md_path = os.path.join(folder_path, "main.md")
        metadata = {
            "dataGU": params["dataGU"],
            "codiceRedaz": params["codiceRedaz"],
            "dataVigenza": params["dataVigenza"],
            "url": url,
            "url_xml": f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={params['dataGU']}&codiceRedaz={params['codiceRedaz']}&dataVigenza={params['dataVigenza']}",
        }

        # Per ora, convertiamo la legge principale senza cross-references
        # Li aggiungeremo dopo aver scaricato tutte le leggi
        if not convert_akomantoso_to_markdown_improved(
            xml_temp_path,
            main_md_path,
            metadata=metadata,
        ):
            print(
                "❌ Errore durante la conversione della legge principale",
                file=sys.stderr,
            )
            return False

        # Scarica e converte leggi citate
        successful_downloads = 0
        failed_downloads = 0
        url_to_file_mapping = {}  # Mappa URL originali ai percorsi dei file

        for i, cited_url in enumerate(cited_urls, 1):
            if not quiet:
                print(
                    f"📥 [{i}/{len(cited_urls)}] Download legge citata: {cited_url}",
                    file=sys.stderr,
                )

            try:
                # Estrai parametri dalla URL citata
                cited_params, cited_session = extract_params_from_normattiva_url(
                    cited_url, quiet=True
                )
                if not cited_params:
                    if not quiet:
                        print(
                            f"⚠️  Impossibile estrarre parametri da: {cited_url}",
                            file=sys.stderr,
                        )
                    failed_downloads += 1
                    continue

                # Crea nome file per la legge citata
                cited_filename = (
                    f"{cited_params['codiceRedaz']}_{cited_params['dataGU']}.md"
                )
                cited_md_path = os.path.join(refs_path, cited_filename)

                # Mappa l'URL originale al percorso del file
                url_to_file_mapping[cited_url] = f"refs/{cited_filename}"

                # Scarica XML temporaneo per la legge citata
                cited_xml_temp = os.path.join(
                    folder_path, f"temp_{cited_params['codiceRedaz']}.xml"
                )
                if download_akoma_ntoso(
                    cited_params, cited_xml_temp, cited_session, quiet=True
                ):
                    # Converti a markdown
                    cited_metadata = {
                        "dataGU": cited_params["dataGU"],
                        "codiceRedaz": cited_params["codiceRedaz"],
                        "dataVigenza": cited_params["dataVigenza"],
                        "url": cited_url,
                        "url_xml": f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={cited_params['dataGU']}&codiceRedaz={cited_params['codiceRedaz']}&dataVigenza={cited_params['dataVigenza']}",
                    }

                    if convert_akomantoso_to_markdown_improved(
                        cited_xml_temp, cited_md_path, cited_metadata
                    ):
                        successful_downloads += 1
                        if not quiet:
                            print(f"✅ Convertita: {cited_filename}", file=sys.stderr)
                    else:
                        failed_downloads += 1
                        if not quiet:
                            print(
                                f"❌ Errore conversione: {cited_filename}",
                                file=sys.stderr,
                            )

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
                print(
                    f"⏳ Attesa 1 secondo prima del prossimo download...",
                    file=sys.stderr,
                )
            time.sleep(1)

        # Costruisci mapping cross-references basato sugli URL originali
        cross_references = build_cross_references_mapping_from_urls(url_to_file_mapping)

        # Se abbiamo cross-references, riconverti la legge principale con i link
        if cross_references:
            if not quiet:
                print(
                    f"🔗 Aggiunta collegamenti incrociati alla legge principale...",
                    file=sys.stderr,
                )
            if not convert_akomantoso_to_markdown_improved(
                xml_temp_path,
                main_md_path,
                metadata=metadata,
                cross_references=cross_references,
            ):
                print(
                    "⚠️  Avviso: riconversione con collegamenti fallita, mantengo versione senza link",
                    file=sys.stderr,
                )

        # Crea file indice
        create_index_file(
            folder_path, params, cited_urls, successful_downloads, failed_downloads
        )

        # Rimuovi XML principale se non richiesto
        if not keep_xml:
            try:
                os.remove(xml_temp_path)
            except OSError:
                pass

        if not quiet:
            print(
                f"\n✅ Completato! {successful_downloads} leggi citate scaricate, {failed_downloads} fallite",
                file=sys.stderr,
            )
            if cross_references:
                print(
                    f"🔗 Collegamenti incrociati aggiunti: {len(cross_references)} riferimenti",
                    file=sys.stderr,
                )
            print(f"📂 Struttura creata in: {folder_path}", file=sys.stderr)

        return True

    except Exception as e:
        print(f"❌ Errore durante il processo con riferimenti: {e}", file=sys.stderr)
        return False
