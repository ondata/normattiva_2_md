## 1. Extract Metadata from XML
- [ ] 1.1 Add function to extract metadata from XML meta section (dataGU, codiceRedaz, dataVigenza)
- [ ] 1.2 Add function to construct URL and URL_XML from metadata
- [ ] 1.3 Modify main conversion flow to pass metadata to conversion functions

## 2. Add Front Matter Generation
- [ ] 2.1 Create function to generate YAML front matter from metadata
- [ ] 2.2 Add front matter output at the beginning of Markdown generation
- [ ] 2.3 Handle cases where metadata is not available (local XML files)

## 3. Adjust Heading Hierarchy
- [ ] 3.1 Modify all heading generation functions to output one level lower
- [ ] 3.2 Update document title extraction to use H1 for law title
- [ ] 3.3 Ensure proper heading level progression throughout the document

## 4. Update Tests and Validation
- [ ] 4.1 Update existing test cases to expect new heading levels
- [ ] 4.2 Add tests for front matter generation
- [ ] 4.3 Test conversion with both URL and local XML inputs
- [ ] 4.4 Run full test suite to ensure no regressions