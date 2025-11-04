## 1. CLI Parameter Implementation
- [x] Add `--with-references` parameter to argparse
- [x] Update help text and examples
- [x] Add validation for parameter usage

## 2. Folder Structure Design
- [x] Define folder naming convention (law ID based)
- [x] Create subfolder structure for main law and references
- [x] Implement folder creation logic

## 3. Reference Extraction
- [x] Parse XML to extract all `<ref>` tag href attributes
- [x] Filter and deduplicate valid normattiva.it URIs
- [x] Handle different URI formats (URN, export URLs, etc.)

## 4. Batch Download Logic
- [x] Implement queue system for downloading multiple laws
- [x] Add progress reporting for batch operations
- [x] Handle download failures gracefully (continue with others)

## 5. Cross-Reference Linking
- [x] Modify markdown generation to include relative links to cited laws
- [x] Create index file listing all downloaded laws
- [x] Update front matter with reference information

## 6. Testing and Validation
- [x] Test with sample law containing multiple references
- [x] Verify folder structure and file naming
- [x] Test error handling for failed downloads
