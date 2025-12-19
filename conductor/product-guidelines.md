# Product Guidelines - Normattiva2MD

## Prose Style & Markdown Standards
- **AI-Ready Conciseness:** Generated Markdown must be clean and free of unnecessary XML boilerplate. The output should prioritize a structure that is immediately useful for LLM context windows.
- **Semantic Integrity:** While removing noise, ensure that the semantic meaning of the legal text is preserved.
- **GitHub Flavored Markdown:** All documentation and output must adhere to standard GFM for maximum compatibility and clean rendering.

## Brand & Messaging
- **Community-First (onData):** The project is rooted in the values of the *onData* community. Messaging should be open, collaborative, and focused on the democratization of legal data.
- **Civic Tech Identity:** Position the tool as a bridge between official government sources and modern digital citizens/hackers.

## Documentation Principles
- **Example-Driven:** Provide rich, practical examples for every major feature (URL conversion, search, article extraction).
- **Comprehensive References:** Maintain detailed guides (like `URL_NORMATTIVA.md`) to help users navigate the complexities of legal data sources.

## Quality & Utility Guidelines
- **Problem-Centric Development:** Feature prioritization is driven by real-world utility for developers and civic hackers.
- **Accuracy over Aesthetics:** In the conversion process, the structural accuracy of the law (correct article numbering, modification highlighting) is more important than visual styling.

## Technical & Architectural Constraints
- **Wide Compatibility:** Must maintain support for Python 3.7+ to ensure availability on older systems or constrained environments.
- **Lightweight & Portable:** Minimize external dependencies to ensure the tool is easy to install and distribute as a standalone binary.
- **Strictly Cross-Platform:** CLI behavior and file handling must be consistent across Linux, Windows, and macOS.
