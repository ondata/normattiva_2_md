## 1. Analysis
- [ ] 1.1 Analyze current URL handling in `extract_params_from_normattiva_url`
- [ ] 1.2 Test current behavior with atto intero export URLs
- [ ] 1.3 Identify how to detect export URLs vs law page URLs

## 2. Implementation
- [ ] 2.1 Modify `is_normattiva_url` to detect export URLs
- [ ] 2.2 Add function to extract parameters from export URL query string
- [ ] 2.3 Update `extract_params_from_normattiva_url` to handle both URL types
- [ ] 2.4 Add validation for export URL parameters

## 3. Testing
- [ ] 3.1 Test with atto intero export URLs
- [ ] 3.2 Test with existing law page URLs (regression test)
- [ ] 3.3 Test error handling for invalid export URLs
- [ ] 3.4 Update test data if needed

## 4. Documentation
- [ ] 4.1 Update help text and examples in main() to include atto intero URLs
- [ ] 4.2 Add comments explaining the two URL handling paths