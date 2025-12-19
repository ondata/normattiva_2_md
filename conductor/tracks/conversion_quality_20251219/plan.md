# Track Plan: Conversion Quality & Validation

This plan outlines the steps to enhance the quality and robustness of the Normattiva to Markdown conversion.

## Phase 1: Foundation & Gold Standard Data [checkpoint: 06db5e5]
Goal: Establish the baseline for quality measurement and validation.

- [x] Task: Create a dedicated `test_data/gold_standard/` directory with diverse XML examples. [ca860c7]
- [x] Task: Define the schema for the conversion validation report (JSON/Markdown). [ee1862b]
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation' (Protocol in workflow.md)

## Phase 2: Structural Validation Logic [checkpoint: 9c5f643]
Goal: Implement the core logic to validate Markdown output against expected structural rules.

- [x] Task: Write tests for the `MarkdownValidator` class (detecting header hierarchy, front matter completeness). [cd58e41]
- [x] Task: Implement `MarkdownValidator` to pass the tests. [cd58e41]
- [x] Task: Write tests for `StructureComparer` (comparing XML nodes count vs MD structure). [e3a2a64]
- [x] Task: Implement `StructureComparer`. [e3a2a64]
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Validation Logic' (Protocol in workflow.md)

## Phase 3: Monitoring & CLI Integration [checkpoint: ebc93c3]
Goal: Integrate validation into the main CLI and provide actionable feedback.

- [x] Task: Write tests for the `--validate` flag in the CLI. [cd2aeb9]
- [x] Task: Implement the `--validate` flag to trigger validation after conversion. [cd2aeb9]
- [x] Task: Create a summary report generator for conversion quality metrics. [da871c7]
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration' (Protocol in workflow.md)
