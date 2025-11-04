## Why

When analyzing a law document, users often need to understand the referenced laws to get complete context. Currently, users must manually identify and download each cited law individually, which is time-consuming and error-prone. This feature would automate the process of downloading all cited laws and creating a linked collection.

## What Changes

- Add new CLI parameter `--with-references` to enable cross-reference download mode
- Create a folder structure organized by law ID containing the main law and all cited laws
- Automatically extract URIs of cited laws from XML `<ref>` tags
- Download and convert all cited laws to markdown format
- Generate cross-references between the main law and cited laws in markdown files

## Impact

- Affected specs: markdown-conversion (new requirement for batch processing)
- Affected code: convert_akomantoso.py (new CLI parameter, reference extraction, batch download logic)
- New dependencies: None (reuses existing download/conversion infrastructure)
