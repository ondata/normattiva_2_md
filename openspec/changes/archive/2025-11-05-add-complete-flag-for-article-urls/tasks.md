## 1. Analysis
- [x] 1.1 Review current article-specific URL implementation
- [x] 1.2 Understand where article filtering occurs in the pipeline
- [x] 1.3 Identify where to add the --completo flag logic

## 2. Implementation
- [x] 2.1 Add --completo/-c argument to argparse configuration
- [x] 2.2 Modify main() function to detect and pass complete flag
- [x] 2.3 Update convert_akomantoso_to_markdown_improved() to accept complete flag
- [x] 2.4 Modify article filtering logic to skip when complete flag is set
- [x] 2.5 Update metadata generation to reflect complete conversion

## 3. Testing
- [x] 3.1 Test --completo flag with article-specific URLs
- [x] 3.2 Test --completo flag with full-law URLs (no change in behavior)
- [x] 3.3 Test without --completo flag maintains existing behavior
- [x] 3.4 Test error handling for invalid article references with --completo
- [x] 3.5 Update help text and examples

## 4. Documentation
- [x] 4.1 Update README with --completo flag examples
- [x] 4.2 Update CLI help text to include --completo option