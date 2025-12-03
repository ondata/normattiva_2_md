# Design: Schema Validation Monitoring

## Architecture Overview

This change introduces automated monitoring of structural dependencies (HTML parsing, XML schema) through lightweight scheduled validation and issue reporting.

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  schema-validation.yml (weekly schedule)              │  │
│  │                                                        │  │
│  │  1. Checkout code                                     │  │
│  │  2. Setup Python                                      │  │
│  │  3. Run schema tests ──────────────┐                  │  │
│  │  4. Parse results                  │                  │  │
│  │  5. Create issue if failed ────────┼──────┐           │  │
│  └────────────────────────────────────┼──────┼───────────┘  │
└───────────────────────────────────────┼──────┼───────────────┘
                                        │      │
                  ┌─────────────────────┘      │
                  │                            │
                  ▼                            ▼
    ┌──────────────────────────┐   ┌──────────────────────┐
    │ test_schema_             │   │  GitHub Issues API   │
    │ validation.py            │   │                      │
    │                          │   │  Title: Schema       │
    │ 4 tests (~1min):         │   │         validation   │
    │ - HTML params OK?        │   │         failed       │
    │ - XML namespace OK?      │   │  Assignee: aborruso  │
    │ - XML elements OK?       │   │  Labels: bug, auto   │
    │ - Download OK?           │   │                      │
    └──────────┬───────────────┘   └──────────────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  normattiva.it           │
    │  (single sample doc)     │
    │                          │
    │  - Download HTML page    │
    │  - Extract params        │
    │  - Download XML          │
    │  - Verify schema         │
    └──────────────────────────┘
```

## Key Design Decisions

### 1. Test Scope: Schema Only, Not Full Conversion
**Decision**: Validate only HTML parsing and XML schema, skip Markdown conversion

**Rationale**:
- Focused validation: catches the actual breaking points (external dependencies)
- Fast execution: < 1 minute, suitable for weekly schedule
- Fewer false positives: conversion bugs are separate from schema changes
- Clear diagnostics: failure points to specific structural change

**Alternatives Considered**:
- Full conversion testing → rejected (too slow, too many failure modes)
- Only unit tests → rejected (doesn't detect normattiva.it changes)
- Manual monitoring → rejected (requires human attention)

### 2. Single Sample Document
**Decision**: Test against one representative legal document (CAD decree)

**Rationale**:
- Sufficient coverage: one document exercises all structural dependencies
- Fast execution: single download + parse
- Stable baseline: same document enables change detection
- Easy debugging: consistent test case

**Alternatives Considered**:
- Multiple documents → rejected (unnecessary, schema is uniform)
- Random selection → rejected (non-deterministic)
- All test_data/ files → rejected (doesn't test live download)

### 3. Issue Creation Strategy
**Decision**: Create one issue per failed workflow run with all failures grouped

**Rationale**:
- Single notification: maintainer gets one alert, not spam
- Context preservation: all related failures in one place
- Easy tracking: one issue to close when fixed
- Workflow correlation: issue links directly to failed run

**Alternatives Considered**:
- One issue per failed test → rejected (too noisy, 5+ issues per run)
- Update existing open issue → rejected (hard to track historical failures)
- Slack/email notification → rejected (GitHub-native is simpler)

### 4. Validation Criteria
**Decision**: Four focused validation points (HTML params, XML namespace, XML elements, download)

**Rationale**:
- HTML parameter extraction: detects normattiva.it HTML structure changes
- XML namespace: verifies Akoma Ntoso 3.0 compatibility
- Essential XML elements: ensures required structure present
- Download success: catches API/network issues

**What to validate**:
```python
1. HTML parameter extraction:
   - dataGU found in hidden input
   - codiceRedaz found in hidden input
   - dataVigenza found in hidden input (optional)
   - Values are non-empty

2. XML namespace:
   - Akoma Ntoso 3.0 namespace present
   - Namespace URL unchanged

3. Essential XML elements:
   - <akomaNtoso> root element exists
   - <meta> section exists
   - <body> section exists
   - At least one <article> exists

4. Download success:
   - HTTP 200 status
   - Response is parseable XML
   - Not HTML error page
```

### 5. Workflow Schedule
**Decision**: Weekly on Monday 09:00 UTC with manual trigger option

**Rationale**:
- Weekly frequency: balances monitoring vs noise (not too frequent)
- Monday morning: gives full week to address issues
- UTC timezone: clear reference time
- Manual trigger: allows on-demand validation before releases

**Alternatives Considered**:
- Daily → rejected (too frequent, alert fatigue)
- After each commit → rejected (not integration test purpose)
- Monthly → rejected (too infrequent, delays problem detection)

## Error Handling

### Test Failures
- Each test is independent, failures don't stop execution
- All failures collected and reported together
- Stack traces captured for debugging

### Network Failures
- Retry mechanism for transient failures (3 attempts, 5s backoff)
- Distinguish between network errors vs structural changes
- Report network failures separately from conversion errors

### Issue Creation Failures
- Workflow doesn't fail if issue creation fails
- Log error to workflow output
- Maintainer still sees workflow failure in GitHub UI

## Testing Strategy

### Local Testing
```bash
# Run all schema validation tests
pytest tests/test_schema_validation.py -v

# Test HTML parameter extraction only
pytest tests/test_schema_validation.py::TestSchemaValidation::test_html_parameter_extraction -v

# Test XML schema only
pytest tests/test_schema_validation.py::TestSchemaValidation::test_xml_namespace_stable -v
pytest tests/test_schema_validation.py::TestSchemaValidation::test_xml_essential_elements -v
```

### Workflow Testing
1. Manual trigger with success scenario
2. Temporarily break HTML parsing, verify issue created
3. Revert break, verify issue closure (if implemented)
4. Wait for scheduled run (first Monday)

## Performance Considerations

- Target execution time: < 1 minute
- Single document test
- Minimal computation: parse HTML, validate XML structure
- No Markdown conversion (saves time)
- No heavy analysis

## Future Enhancements (Not in Scope)

1. **Multiple Sample Documents**: Test against 3-5 different document types
2. **Historical Tracking**: Store validation results over time, trend analysis
3. **Auto-Recovery**: Retry with different parameters if extraction fails
4. **Full Conversion Testing**: Add optional full MD conversion validation
5. **Performance Benchmarking**: Track download/parse speed over time
