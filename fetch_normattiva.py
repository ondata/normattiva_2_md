import argparse
import os
import sys

# Importa il nostro convertitore Akoma Ntoso a Markdown (il vecchio convert_akomantoso.py)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from convert_akomantoso import convert_akomantoso_to_markdown_improved

# Importa il client Normattiva e il parser Akoma Ntoso da tulit
try:
    from tulit.client.normattiva import NormattivaClient
    import tulit.parsers.xml.akomantoso as tulit_akomantoso_parser_module
except ImportError:
    print("Errore: La libreria 'tulit' non è installata. Esegui 'pip install tulit'.")
    sys.exit(1)

def fetch_and_convert_normattiva(data_gu, codice_redaz, data_vigenza, output_file_path, output_format):
    """
    Recupera un documento Akoma Ntoso da Normattiva usando tulit e lo converte nel formato specificato.
    """
    print(f"Tentativo di recupero del documento da Normattiva con dataGU={data_gu}, codiceRedaz={codice_redaz}, dataVigenza={data_vigenza}...")

    client = NormattivaClient(download_dir='./temp_normattiva_xml', log_dir='./logs')

    try:
        downloaded_paths = client.download(
            dataGU=data_gu,
            codiceRedaz=codice_redaz,
            dataVigenza=data_vigenza
        )

        if not downloaded_paths:
            print(f"Errore: Nessun documento trovato per i parametri forniti.")
            return False

        akoma_ntoso_xml_path = downloaded_paths[0]
        print(f"Documento Akoma Ntoso recuperato: {akoma_ntoso_xml_path}")

        success = False

        if output_format == 'markdown':
            print(f"Conversione di {akoma_ntoso_xml_path} in Markdown a {output_file_path}...")
            success = convert_akomantoso_to_markdown_improved(akoma_ntoso_xml_path, output_file_path)
            if success:
                print(f"✅ Conversione completata. Il file Markdown è stato salvato in '{output_file_path}'")
            else:
                print(f"❌ Errore durante la conversione del file XML in Markdown.")

        elif output_format == 'json':
            print(f"Conversione di {akoma_ntoso_xml_path} in JSON (output grezzo tulit) a {output_file_path}...")
            original_sys_argv = sys.argv
            try:
                sys.argv = ['tulit_akomantoso_parser', '--input', akoma_ntoso_xml_path, '--output', output_file_path]
                tulit_akomantoso_parser_module.main()
                success = True
                print(f"✅ Conversione completata. Il file JSON (output grezzo tulit) è stato salvato in '{output_file_path}'")
            except Exception as e:
                print(f"❌ Errore durante la conversione del file XML in JSON (output grezzo tulit): {e}")
                success = False
            finally:
                sys.argv = original_sys_argv

        # Pulizia dei file temporanei
        try:
            os.remove(akoma_ntoso_xml_path)
            # Rimuovi anche la directory temporanea creata da tulit se vuota
            os.rmdir(os.path.dirname(akoma_ntoso_xml_path))
        except OSError as e:
            print(f"Attenzione: Impossibile rimuovere il file temporaneo o la directory: {e}")

        return success

    except Exception as e:
        print(f"Si è verificato un errore durante il recupero o la conversione: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Recupera un documento Akoma Ntoso da Normattiva e lo converte nel formato specificato.'
    )
    parser.add_argument('--dataGU', required=True,
                        help='Data della Gazzetta Ufficiale (formato YYYYMMDD).')
    parser.add_argument('--codiceRedaz', required=True,
                        help='Codice redazionale del documento.')
    parser.add_argument('--dataVigenza', required=True,
                        help='Data di vigenza del documento (formato YYYYMMDD).')
    parser.add_argument('--output', required=True,
                        help='Il percorso del file di output (Markdown o JSON).')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                        help='Il formato di output desiderato (markdown o json). Default: markdown')

    args = parser.parse_args()

    success = fetch_and_convert_normattiva(
        args.dataGU,
        args.codiceRedaz,
        args.dataVigenza,
        args.output,
        args.format
    )

    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()