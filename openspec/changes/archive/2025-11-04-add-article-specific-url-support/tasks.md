## 1. Analysis
- [x] 1.1 Analyze current URL parsing and XML processing logic
- [x] 1.2 Understand how article-specific URLs work (~art suffix)
- [x] 1.3 Identify where to add article filtering in the conversion pipeline

## 2. Implementation
- [x] 2.1 Add function to detect and parse article references from URLs
- [x] 2.2 Add function to filter XML document to specific article
- [x] 2.3 Modify conversion pipeline to handle single-article documents
- [x] 2.4 Update metadata generation for article-specific URLs
- [x] 2.5 Add validation for article existence in document

## 3. Testing
- [x] 3.1 Test with article-specific URLs (~art3, ~art16bis, etc.)
- [x] 3.2 Test with non-existent articles (error handling)
- [x] 3.3 Test regression with full-law URLs
- [x] 3.4 Test edge cases (articles with extensions: bis, ter, etc.)
- [ ] 3.5 Update test data if needed

## 4. Documentation
- [x] 4.1 Update help text and examples to include article-specific URLs
- [x] 4.2 Add comments explaining article filtering logic
- [ ] 4.3 Update README with article-specific URL examples