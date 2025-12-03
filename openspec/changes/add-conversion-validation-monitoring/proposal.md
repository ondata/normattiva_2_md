# Proposal: add-conversion-validation-monitoring

## Summary
Implement automated weekly testing to validate that Akoma Ntoso → Markdown conversion rules remain correct over time. Monitor for structural changes in normattiva.it data or conversion breakage, automatically opening issues when failures are detected.

## Background
The conversion from Akoma Ntoso XML to Markdown relies on specific XML structures and normattiva.it API behavior. These can change without notice:
- normattiva.it may alter XML schema or HTML structure
- New Akoma Ntoso elements may appear in documents
- Conversion logic may produce different output over time

Currently, there's no automated monitoring to detect when conversion rules break or need updates.

## Goals
1. Verify HTML parameter extraction from normattiva.it pages still works (dataGU, codiceRedaz, dataVigenza)
2. Verify XML Akoma Ntoso schema stability (namespace, base elements unchanged)
3. Run validation weekly via GitHub Actions scheduled workflow
4. Automatically open GitHub issues assigned to @aborruso when validation fails

## Non-Goals
- Not testing full Markdown conversion (only data extraction and XML schema)
- Not validating Markdown output quality or formatting
- Not testing all possible legal documents (focus on single representative sample)
- Not implementing auto-fix mechanisms (manual review required)

## Success Criteria
- Weekly workflow runs successfully on schedule
- Test failures produce actionable GitHub issues
- Issues include specific failure details and affected documents
- Workflow can be manually triggered for on-demand validation

## Open Questions
- Should the workflow also test PyPI-installed version vs local code?
- How many documents to test (balance coverage vs execution time)?
- Should we cache successful conversion outputs for diff comparison?
