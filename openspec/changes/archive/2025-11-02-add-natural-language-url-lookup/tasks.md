## 1. CLI Argument Enhancement
- [ ] Add new CLI flag for natural language input (e.g., --search or -s)
- [ ] Update argparse help text and examples
- [ ] Modify argument parsing logic to handle new input type

## 2. URL Lookup Module
- [ ] Create new function to call Gemini CLI with -p flag
- [ ] Implement prompt engineering for normattiva.it URL search
- [ ] Add URL validation and extraction from Gemini response
- [ ] Handle errors when Gemini CLI is not available

## 3. Integration with Main Logic
- [ ] Modify main() to detect natural language input
- [ ] Add preprocessing step to resolve string to URL before conversion
- [ ] Ensure fallback to existing URL/XML processing

## 4. Error Handling and User Feedback
- [ ] Add informative error messages for failed lookups
- [ ] Handle cases where no URL is found
- [ ] Provide user guidance on Gemini CLI installation

## 5. Testing
- [ ] Add unit tests for URL lookup function
- [ ] Add integration tests with mocked Gemini CLI
- [ ] Update CLI tests to cover new flag
- [ ] Test error scenarios (Gemini not installed, no results)

## 6. Documentation
- [ ] Update README with new usage examples
- [ ] Document Gemini CLI dependency and installation
- [ ] Add examples for natural language input