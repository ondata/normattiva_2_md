## 1. Analyze Current Reference Processing
- [x] Review how <ref> tags are currently processed in clean_text_content()
- [x] Understand the current markdown generation flow
- [x] Identify where to inject cross-reference logic

## 2. Modify Reference Processing Logic
- [x] Add parameter to track --with-references mode in markdown generation functions
- [x] Modify clean_text_content() to accept cross-reference mapping
- [x] Create function to map Akoma URIs to local markdown file paths

## 3. Implement Link Generation
- [x] Parse href attributes from <ref> tags to extract Akoma URIs
- [x] Convert Akoma URIs to relative markdown file paths (e.g., refs/costituzione_1947.md)
- [x] Replace plain text references with markdown links [text](path)

## 4. Update Main Markdown Generation
- [x] Pass cross-reference mapping to markdown generation functions
- [x] Ensure links are generated only for successfully downloaded references
- [x] Handle cases where referenced laws failed to download

## 5. Testing and Validation
- [x] Test with sample law containing multiple references
- [x] Verify links point to correct files in refs/ folder
- [x] Test edge cases (missing references, failed downloads)
- [x] Ensure backward compatibility when not using --with-references
