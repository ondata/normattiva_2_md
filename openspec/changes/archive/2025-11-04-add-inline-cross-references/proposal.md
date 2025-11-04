## Why

When using --with-references, users expect to be able to click on law references directly in the main markdown file to navigate to the downloaded referenced laws, rather than having to use a separate index file. Currently, references in main.md remain as plain text, requiring users to manually find the corresponding files in the refs/ folder.

## What Changes

- Modify the markdown generation for --with-references mode to convert law references into clickable markdown links
- Replace plain text references with relative links pointing to downloaded markdown files in refs/
- Maintain backward compatibility - links only added when using --with-references mode

## Impact

- Affected specs: markdown-conversion (modify existing Cross-Reference Linking requirement)
- Affected code: convert_akomantoso.py (markdown generation logic when processing <ref> tags)
- New dependencies: None
