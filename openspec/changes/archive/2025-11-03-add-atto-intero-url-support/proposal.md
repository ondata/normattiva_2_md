## Why
The tool currently supports normattiva.it URLs that are law pages (e.g., https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto-legge:2018-07-12;87) by scraping them to extract parameters for XML download. However, users may also want to provide "atto intero" (full act) export URLs directly (e.g., https://www.normattiva.it/esporta/attoCompleto?atto.dataPubblicazioneGazzetta=2018-07-13&atto.codiceRedazionale=18G00112), which contain the necessary parameters in the URL query string and should be handled seamlessly.

## What Changes
- Extend URL detection and parameter extraction to support both law page URLs and atto intero export URLs
- Modify `extract_params_from_normattiva_url` to handle export URLs by parsing query parameters directly
- Ensure all normattiva.it URLs ultimately result in XML download and conversion

## Impact
- Affected specs: markdown-conversion
- Affected code: convert_akomantoso.py (URL handling functions)
- No breaking changes - this extends existing functionality