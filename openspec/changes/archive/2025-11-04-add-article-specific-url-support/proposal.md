## Why
The tool currently supports full law URLs but not URLs that point to specific articles within a law (e.g., https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legge:2018-07-12;87~art3). Users may want to convert only a specific article rather than the entire law document, which would be more efficient for targeted analysis.

## What Changes
- Extend URL parsing to detect and extract article references from URLs containing `~art` suffixes
- Add XML filtering capability to extract only the specified article from the full document
- Modify the conversion process to handle single-article output
- Maintain backward compatibility with full-law URLs

## Impact
- Affected specs: markdown-conversion
- Affected code: convert_akomantoso.py (URL parsing, XML processing, conversion logic)
- No breaking changes - this extends existing functionality