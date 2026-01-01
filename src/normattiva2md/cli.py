import os
import sys
import argparse
import tempfile
import xml.etree.ElementTree as ET

from .constants import VERSION
from .utils import sanitize_output_path, generate_snake_case_filename, load_env_file
from .normattiva_api import (
    is_normattiva_url,
    validate_normattiva_url,
    extract_params_from_normattiva_url,
    download_akoma_ntoso,
)
from .exa_api import lookup_normattiva_url
from .akoma_utils import parse_article_reference
from .xml_parser import construct_article_eid
from .markdown_converter import convert_akomantoso_to_markdown_improved
from .multi_document import convert_with_references
from .provvedimenti_api import (
    extract_law_params_from_url,
    fetch_all_provvedimenti,
    write_provvedimenti_csv,
)
from .validation import MarkdownValidator, StructureComparer


def perform_validation(xml_path, md_path, quiet=False):
    """
    Esegue la validazione strutturale e il confronto tra XML e Markdown.
    """
    if not os.path.exists(md_path):
        return False

    try:
        validator = MarkdownValidator()
        comparer = StructureComparer()

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        tree = ET.parse(xml_path)
        root = tree.getroot()

        v_report = validator.validate(md_text)
        c_report = comparer.compare(root, md_text)

        if not quiet:
            print("\n🔍 Risultati Validazione:", file=sys.stderr)
            print(f"  - Struttura Markdown: {v_report['status']}", file=sys.stderr)
            print(
                f"  - Confronto XML/MD: {c_report['status']} ({c_report['message']})",
                file=sys.stderr,
            )

            if v_report["status"] != "PASS":
                for err in v_report["errors"]:
                    print(f"    ❌ {err['message']}", file=sys.stderr)

        return v_report["status"] == "PASS" and c_report["status"] == "PASS"
    except Exception as e:
        if not quiet:
            print(f"❌ Errore durante la validazione: {e}", file=sys.stderr)
        return False


def main():
    """
    Funzione principale che gestisce gli argomenti della riga di comando
    Supporta sia file XML locali che URL normattiva.it
    """
    cmd = os.path.basename(sys.argv[0]) or "normattiva2md"
    cmd_display = cmd if not cmd.endswith(".py") else "normattiva2md"
    parser = argparse.ArgumentParser(
        description="Converte documenti Akoma Ntoso in formato Markdown da file XML o URL normattiva.it",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=cmd_display,
        epilog=f"""
  Esempi d'uso:

    # Output a file
    {cmd_display} input.xml output.md
    {cmd_display} -i input.xml -o output.md

    # Output a stdout (default se -o omesso)
    {cmd_display} input.xml
    {cmd_display} input.xml > output.md
    {cmd_display} -i input.xml

    # Da URL normattiva.it (auto-detect)
    {cmd_display} "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md
    {cmd_display} "https://www.normattiva.it/esporta/attoCompleto?atto.dataPubblicazioneGazzetta=2018-07-13&atto.codiceRedazionale=18G00112" output.md
    {cmd_display} "URL" > output.md
    {cmd_display} -i "URL" -o output.md

    # Da URL normattiva.it con articolo specifico
    {cmd_display} "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" output.md
    {cmd_display} "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis" output.md

    # Forza conversione completa anche con URL articolo-specifico
    {cmd_display} --completo "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87~art3" -o output.md
    {cmd_display} -c "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53~art16bis" -o output.md

    # Ricerca in linguaggio naturale (richiede Exa API key)
    {cmd_display} -s "legge stanca accessibilità" -o output.md
    {cmd_display} --search "decreto dignità" --exa-api-key "your-key" > output.md

    # Mantenere XML scaricato da URL
    {cmd_display} "URL" --keep-xml -o output.md
    {cmd_display} "URL" --keep-xml > output.md

    # Scaricare anche tutte le leggi citate (output in directory)
    {cmd_display} --with-references "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2005-03-07;82" legge_82_2005/

    # Generare link markdown agli articoli citati su normattiva.it
    {cmd_display} --with-urls "input.xml" -o output.md
    {cmd_display} --with-urls "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" -o output.md

    # Esportare provvedimenti attuativi in CSV
    {cmd_display} --provvedimenti "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024;207" -o output.md

    # Filtrare un singolo articolo
    {cmd_display} --art 4 input.xml output.md
    {cmd_display} --art 16bis "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md
    {cmd_display} --art 3 --with-urls "input.xml" > output.md
            """,
    )

    # Version flag
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {VERSION}"
    )

    # Argomenti posizionali (compatibilità con uso semplice)
    parser.add_argument(
        "input",
        nargs="?",
        help="File XML locale o URL normattiva.it (inclusi URL atto intero)",
    )
    parser.add_argument(
        "output", nargs="?", help="File Markdown di output (default: stdout)"
    )

    # Argomenti opzionali (per maggiore flessibilità)
    parser.add_argument(
        "-i",
        "--input",
        dest="input_named",
        help="File XML locale o URL normattiva.it (inclusi URL atto intero)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_named",
        help="File Markdown di output (default: stdout)",
    )
    parser.add_argument(
        "-s",
        "--search",
        dest="search_query",
        help='Cerca documento legale in linguaggio naturale (es. "legge stanca")',
    )
    parser.add_argument(
        "--exa-api-key", dest="exa_api_key", help="Chiave API per Exa AI"
    )
    parser.add_argument(
        "--debug-search",
        action="store_true",
        help="Mostra JSON completo della ricerca Exa AI e abilita selezione manuale (se --auto-select disabilitato)",
    )
    parser.add_argument(
        "--auto-select",
        action="store_true",
        help="Seleziona automaticamente il miglior risultato dalla ricerca naturale (default: False se --debug-search abilitato)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Esegue la validazione strutturale del Markdown generato",
    )
    parser.add_argument(
        "-c",
        "--completo",
        action="store_true",
        help="Forza la conversione della legge completa anche se l'URL punta a un articolo specifico",
    )
    parser.add_argument(
        "--keep-xml",
        action="store_true",
        help="Mantiene i file XML scaricati temporaneamente",
    )
    parser.add_argument(
        "--with-references",
        action="store_true",
        help="Scarica anche tutte le leggi citate e le converte in una sottocartella 'refs'",
    )
    parser.add_argument(
        "--with-urls",
        action="store_true",
        help="Genera link Markdown agli URL originali di normattiva.it per gli articoli citati",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Disabilita output non essenziali"
    )
    parser.add_argument(
        "--provvedimenti",
        action="store_true",
        help="Cerca e esporta provvedimenti attuativi da programmagoverno.gov.it in formato CSV",
    )
    parser.add_argument(
        "--art",
        dest="article_filter",
        help="Filtra output a singolo articolo (es: 4, 16bis, 3ter). Sovrascrive ~artN nell'URL",
    )
    args = parser.parse_args()

    # Combinazione argomenti posizionali e named
    input_source = args.input_named or args.input
    output_file = args.output_named or args.output

    # Logica di fallback per input/output se non specificati
    if input_source is None and args.search_query is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Esegui load_env_file all'inizio
    # Sebbene load_env_file sia in utils.py, la sua chiamata deve essere qui per inizializzare le variabili d'ambiente prima dell'uso.
    load_env_file()

    # Validate --provvedimenti parameter
    if args.provvedimenti:
        if not input_source or not is_normattiva_url(input_source):
            print(
                "❌ Error: --provvedimenti requires a normattiva.it URL as input",
                file=sys.stderr,
            )
            sys.exit(1)

    # Validate --with-references parameter
    if args.with_references:
        if not is_normattiva_url(input_source):
            print(
                "❌ --with-references può essere usato solo con URL normattiva.it",
                file=sys.stderr,
            )
            sys.exit(1)
        if (
            output_file
            and not os.path.isdir(output_file)
            and os.path.exists(output_file)
        ):
            print(
                "❌ --with-references richiede un nome di directory (non un file esistente)",
                file=sys.stderr,
            )
            print(
                "💡 Esempio: akoma2md --with-references <url> [nome_cartella]",
                file=sys.stderr,
            )
            sys.exit(1)

    # Sanitize output path if provided
    if output_file:
        try:
            output_file = sanitize_output_path(output_file)
        except ValueError as e:
            print(f"❌ Errore nel path di output: {e}", file=sys.stderr)
            sys.exit(1)

    # Determine quiet mode (output to stdout or --quiet flag)
    quiet_mode = args.quiet or output_file is None

    # Convert --art parameter to article eId
    article_filter = args.article_filter
    article_filter_eid = None
    if article_filter:
        article_filter_eid = construct_article_eid(article_filter)
        if not article_filter_eid:
            print(
                f"❌ Formato articolo invalido: '{article_filter}'. Usa formato: numero[estensione] (es: 4, 16bis, 3ter)",
                file=sys.stderr,
            )
            sys.exit(1)
        if not quiet_mode:
            print(
                f"Filtro articolo attivato: {article_filter} (eId: {article_filter_eid})",
                file=sys.stderr,
            )

    # Gestisci ricerca naturale se specificata
    if args.search_query:
        if not args.quiet:
            print(f"🔍 Ricerca documento: {args.search_query}", file=sys.stderr)

        # Determina se usare selezione automatica o manuale
        # auto_select è True di default, a meno che debug_search non sia True
        auto_select_search = args.auto_select
        if args.debug_search:
            auto_select_search = False

        lookup_result = lookup_normattiva_url(
            args.search_query,
            debug_json=args.debug_search,
            auto_select=auto_select_search,
            exa_api_key=args.exa_api_key,
        )
        if not lookup_result:
            print(
                "❌ Impossibile trovare URL per la ricerca specificata", file=sys.stderr
            )
            sys.exit(1)

        # Gestisci risultato (può essere str o dict, se auto_select=False in debug_search)
        if isinstance(lookup_result, dict):
            # Selezione manuale in debug mode - chiedi se scaricare
            selected_url = lookup_result["url"]
            selected_title = lookup_result["title"]

            # Chiedi se vuole scaricare
            try:
                download_choice = (
                    input("\n📥 Vuoi scaricare questo documento? (s/N): ")
                    .strip()
                    .lower()
                )
                if download_choice not in ["s", "si", "sì", "y", "yes"]:
                    print("📄 Mostro il documento su stdout...", file=sys.stderr)
                    input_source = selected_url
                    output_file = None  # Output su stdout
                else:
                    # Genera nome file snake_case
                    suggested_filename = generate_snake_case_filename(selected_title)
                    try:
                        filename_input = input(
                            f"📝 Nome file (INVIO per confermare, o scrivi nome desiderato) [{suggested_filename}]: "
                        ).strip()
                    except KeyboardInterrupt:
                        print("\r❌ Operazione annullata dall'utente", file=sys.stderr)
                        sys.exit(0)

                    # Valida input: ignora risposte di conferma troppo corte
                    if filename_input and filename_input.lower() not in [
                        "s",
                        "si",
                        "sì",
                        "y",
                        "yes",
                        "n",
                        "no",
                    ]:
                        output_file = filename_input
                        if not output_file.endswith(".md"):
                            output_file += ".md"
                    elif filename_input and len(filename_input) <= 2:
                        # Input troppo corto probabilmente è un errore, usa il suggerito
                        print(
                            f"⚠️  Nome troppo corto, uso il nome suggerito: {suggested_filename}",
                            file=sys.stderr,
                        )
                        output_file = suggested_filename
                    else:
                        output_file = suggested_filename

                    # Verifica se il file esiste già
                    if os.path.exists(output_file):
                        try:
                            overwrite = (
                                input(
                                    f"⚠️  Il file '{output_file}' esiste già. Sovrascrivere? (s/N): "
                                )
                                .strip()
                                .lower()
                            )
                        except KeyboardInterrupt:
                            print("\r❌ Operazione annullata dall'utente", file=sys.stderr)
                            sys.exit(0)
                        if overwrite not in ["s", "si", "sì", "y", "yes"]:
                            print("❌ Download annullato dall'utente", file=sys.stderr)
                            sys.exit(0)

                input_source = selected_url
                if output_file:
                    print(f"✅ URL selezionato: {input_source}", file=sys.stderr)

            except (EOFError, KeyboardInterrupt):
                print("\r❌ Operazione annullata dall'utente", file=sys.stderr)
                sys.exit(0)
        else:
            # Selezione automatica - usa il comportamento precedente
            input_source = lookup_result
            if not args.quiet and not args.debug_search:
                print(f"✅ URL trovato: {input_source}", file=sys.stderr)

    # Auto-detect: URL o file locale?
    if is_normattiva_url(input_source):
        # Gestione URL
        if not quiet_mode:
            print(f"Rilevato URL normattiva.it: {input_source}", file=sys.stderr)

        # Validate URL for security
        try:
            validate_normattiva_url(input_source)
        except ValueError as e:
            print(f"❌ Errore validazione URL: {e}", file=sys.stderr)
            sys.exit(1)

        # Handle --with-references mode
        if args.with_references:
            success = convert_with_references(
                input_source, output_file, args.quiet, args.keep_xml, args.completo
            )
            if not success:
                sys.exit(1)
            # Don't exit on success - allow provvedimenti processing if specified
            # Skip normal conversion when using --with-references
        else:
            # Normal conversion (not --with-references mode)

            # Determine article filtering: priority is --art > --completo > URL ~artN
            article_ref = None

            if article_filter_eid:
                # --art flag has highest priority
                article_ref = article_filter_eid
                url_article_ref = parse_article_reference(input_source)
                if url_article_ref and not quiet_mode:
                    print(
                        f"Flag --art sovrascrive riferimento URL (~{url_article_ref})",
                        file=sys.stderr,
                    )
            elif args.completo:
                # --completo flag: ignore URL article reference
                url_article_ref = parse_article_reference(input_source)
                if url_article_ref and not quiet_mode:
                    print(
                        f"Forzando conversione completa della legge (--completo ignora ~{url_article_ref})",
                        file=sys.stderr,
                    )
                article_ref = None
            else:
                # Use URL article reference if present
                article_ref = parse_article_reference(input_source)
                if article_ref and not quiet_mode:
                    print(f"Rilevato riferimento articolo: {article_ref}", file=sys.stderr)

            # Estrai parametri dalla pagina
            params, session = extract_params_from_normattiva_url(
                input_source, quiet=quiet_mode
            )
            if not params:
                print("❌ Impossibile estrarre parametri dall'URL", file=sys.stderr)
                sys.exit(1)

            if not quiet_mode:
                print(f"\nParametri estratti:", file=sys.stderr)
                print(f"  dataGU: {params['dataGU']}", file=sys.stderr)
                print(f"  codiceRedaz: {params['codiceRedaz']}", file=sys.stderr)
                print(f"  dataVigenza: {params['dataVigenza']}\n", file=sys.stderr)

            # Crea file XML temporaneo con tempfile module (più sicuro)
            temp_fd, xml_temp_path = tempfile.mkstemp(
                suffix=f"_{params['codiceRedaz']}.xml", prefix="akoma2md_"
            )
            os.close(temp_fd)  # Close file descriptor, we'll write with requests

            # Scarica XML
            if not download_akoma_ntoso(
                params, xml_temp_path, session, quiet=quiet_mode
            ):
                print("❌ Errore durante il download del file XML", file=sys.stderr)
                sys.exit(1)

            # Converti a Markdown
            if not quiet_mode:
                print(f"\nConversione in Markdown...", file=sys.stderr)

            # Prepare metadata dict for front matter
            metadata = {
                "dataGU": params["dataGU"],
                "codiceRedaz": params["codiceRedaz"],
                "dataVigenza": params["dataVigenza"],
                "url": input_source,  # The original URL
                "url_xml": f"https://www.normattiva.it/do/atto/caricaAKN?dataGU={params['dataGU']}&codiceRedaz={params['codiceRedaz']}&dataVigenza={params['dataVigenza']}",
            }

            # Add article reference to metadata if present (or if overridden by --completo)
            if article_ref:
                metadata["article"] = article_ref
            elif args.completo and parse_article_reference(input_source):
                # Note that complete conversion was forced
                metadata["article"] = parse_article_reference(
                    input_source
                )  # Include original article ref for reference

            success = convert_akomantoso_to_markdown_improved(
                xml_temp_path,
                output_file,
                metadata=metadata,
                article_ref=article_ref,
                with_urls=args.with_urls,
            )

            if success:
                if not quiet_mode:
                    if output_file:
                        print(
                            f"✅ Conversione completata: {output_file}", file=sys.stderr
                        )
                    else:
                        print(
                            f"✅ Conversione completata (output a stdout)",
                            file=sys.stderr,
                        )

                # Validazione strutturale
                if args.validate:
                    if output_file:
                        perform_validation(xml_temp_path, output_file, quiet_mode)
                    elif not quiet_mode:
                        print(
                            "⚠️ Validazione saltata: output a stdout non supportato con --validate",
                            file=sys.stderr,
                        )

                # Rimuovi XML temporaneo se non richiesto diversamente
                if not args.keep_xml:
                    try:
                        os.remove(xml_temp_path)
                        if not quiet_mode:
                            print(f"File XML temporaneo rimosso", file=sys.stderr)
                    except OSError as e:
                        print(
                            f"Attenzione: impossibile rimuovere file temporaneo: {e}",
                            file=sys.stderr,
                        )
                else:
                    if not quiet_mode:
                        print(f"File XML mantenuto: {xml_temp_path}", file=sys.stderr)

                # Don't exit here - allow provvedimenti processing to run if specified
                # sys.exit(0) removed to allow --provvedimenti to execute
            else:
                print("❌ Errore durante la conversione", file=sys.stderr)
                sys.exit(1)

    else:
        # Gestione file XML locale
        if not quiet_mode:
            if output_file:
                print(
                    f"Conversione da file XML locale: '{input_source}' a '{output_file}'...",
                    file=sys.stderr,
                )
            else:
                print(
                    f"Conversione da file XML locale: '{input_source}' (output a stdout)...",
                    file=sys.stderr,
                )
        success = convert_akomantoso_to_markdown_improved(
            input_source,
            output_file,
            metadata=None,
            article_ref=article_filter_eid,
            with_urls=args.with_urls,
        )

        if success:
            if not quiet_mode:
                print("✅ Conversione completata con successo!", file=sys.stderr)

            # Validazione strutturale
            if args.validate:
                if output_file:
                    perform_validation(input_source, output_file, quiet_mode)
                elif not quiet_mode:
                    print(
                        "⚠️ Validazione saltata: output a stdout non supportato con --validate",
                        file=sys.stderr,
                    )
        else:
            print("❌ Errore durante la conversione.", file=sys.stderr)
            sys.exit(1)

    # Handle --provvedimenti if specified
    if args.provvedimenti:
        quiet_mode = args.quiet
        anno, numero = extract_law_params_from_url(input_source)

        if not anno or not numero:
            print(
                f"❌ Error: Unable to extract law year and number from URL: {input_source}",
                file=sys.stderr,
            )
            sys.exit(1)

        if not quiet_mode:
            print(
                f"\n🔍 Ricerca provvedimenti attuativi per la legge {numero}/{anno}...",
                file=sys.stderr,
            )

        provvedimenti_data = fetch_all_provvedimenti(numero, anno, quiet=quiet_mode)

        if provvedimenti_data is None:
            # Network error on first page
            print(
                f"❌ Error: Failed to fetch implementation measures from programmagoverno.gov.it",
                file=sys.stderr,
            )
            sys.exit(1)
        elif not provvedimenti_data:
            # No results found
            print(
                f"Nessun provvedimento attuativo trovato per la legge {numero}/{anno}",
                file=sys.stderr,
            )
            # Continue - this is not an error
        else:
            # Write CSV
            csv_written = write_provvedimenti_csv(
                provvedimenti_data, anno, numero, output_file, quiet=quiet_mode
            )
            if not csv_written:
                sys.exit(1)

if __name__ == "__main__":
    main()
