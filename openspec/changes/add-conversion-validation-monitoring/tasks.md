# Tasks: add-conversion-validation-monitoring

## Implementation Tasks

### 1. Create Schema Validation Test Suite
- [ ] Create `tests/test_schema_validation.py` with:
  - `TestSchemaValidation` class
  - Test fixture: single representative legal document URL (e.g., CAD)
  - `test_html_parameter_extraction()` - verify HTML parsing extracts dataGU, codiceRedaz, dataVigenza
  - `test_xml_namespace_stable()` - verify Akoma Ntoso 3.0 namespace present
  - `test_xml_essential_elements()` - verify akomaNtoso, meta, body, article elements exist
  - `test_xml_download_succeeds()` - verify HTTP 200 and valid XML response
- [ ] Add test configuration constants:
  - `SAMPLE_DOCUMENT_URL` - URL to test (e.g., CAD decree)
  - `EXPECTED_NAMESPACE` - Akoma Ntoso namespace URL
  - `ESSENTIAL_ELEMENTS` - list of required XML element names
- [ ] Create helper functions:
  - `parse_html_parameters(html_content)` - extract parameters from HTML
  - `validate_xml_structure(xml_content)` - check namespace and elements
  - `format_validation_error(error_type, details)` - format errors for reporting

**Validation**: Run `python -m pytest tests/test_schema_validation.py -v` successfully

---

### 2. Create GitHub Actions Workflow
- [ ] Create `.github/workflows/schema-validation.yml` with:
  - Schedule trigger: `cron: '0 9 * * 1'` (Monday 09:00 UTC)
  - Manual trigger: `workflow_dispatch`
  - Job steps:
    1. Checkout code
    2. Setup Python 3.9+
    3. Install dependencies (`pip install -e .`)
    4. Run schema tests (`pytest tests/test_schema_validation.py -v --tb=short`)
    5. Capture test results and failures
  - Conditional step: create issue on failure
- [ ] Configure workflow permissions:
  - `contents: read`
  - `issues: write`

**Validation**: Manually trigger workflow via GitHub Actions UI, verify execution

---

### 3. Implement Automated Issue Creation
- [ ] Add workflow step using `actions/github-script@v7` to:
  - Parse pytest output for failures
  - Extract failed test names and error messages
  - Create issue only if tests failed
- [ ] Issue template includes:
  - Title: `Schema validation failed - YYYY-MM-DD`
  - Body sections:
    - Summary: "Validation detected structural changes"
    - Which validation failed: HTML parsing / XML schema / Download
    - Error details (which parameter missing, which element missing)
    - Link to workflow run: `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}`
  - Labels: `["bug", "automated"]`
  - Assignee: `aborruso`
- [ ] Handle edge cases:
  - Don't create duplicate issues if already open
  - Close previous automated issues if tests now pass

**Validation**: Force test failure, verify issue created with correct content

---

### 4. Documentation Updates
- [ ] Update README.md with:
  - Section on "Automated Schema Validation" explaining weekly monitoring
  - Brief description: validates HTML parsing and XML schema stability
  - Link to workflow file
  - Explanation of automated issues
- [ ] Add comment in workflow file explaining:
  - What is being validated (HTML params extraction, XML schema)
  - Sample document URL being tested
  - How to run manually

**Validation**: Review docs for clarity and completeness

---

### 5. Testing and Refinement
- [ ] Run integration tests locally multiple times to ensure stability
- [ ] Test workflow manually with both success and failure scenarios
- [ ] Verify issue creation works correctly
- [ ] Confirm weekly schedule triggers as expected (wait for first Monday run)
- [ ] Review first automated issue for clarity and actionable information

**Validation**: Wait for first scheduled run on Monday, verify behavior

---

## Dependencies
- All tasks can be done in parallel except:
  - Task 2 depends on Task 1 (workflow needs tests to run)
  - Task 3 depends on Task 2 (issue creation is part of workflow)
  - Task 5 depends on Tasks 1-3 (final testing)

## Testing Checklist
- [ ] Integration tests pass locally
- [ ] Workflow executes successfully when manually triggered
- [ ] Issue is created when tests fail (simulate failure)
- [ ] Issue contains all required information
- [ ] No issue created when tests pass
- [ ] Workflow scheduled trigger is configured correctly
