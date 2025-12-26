# Product Guide - Normattiva2MD

## Initial Concept
Normattiva2MD is a specialized CLI tool designed to convert Italian legal documents from the complex Akoma Ntoso XML format (provided by normattiva.it) into AI-friendly Markdown. It aims to make legislation easily accessible for Large Language Models (LLMs), RAG systems, and automated legal analysis pipelines.

## Target Users
- **Developers:** Building legal tech applications, chatbots, and RAG systems that require structured legal context.
- **Data Scientists & AI Researchers:** Needing high-quality, pre-processed legal datasets for training or fine-tuning.
- **Legal Professionals:** Tech-savvy lawyers or researchers who need to process or search legislation locally using CLI tools.
- **Civic Hackers:** Individuals and groups working on open data projects and government transparency.

## Core Value Proposition
- **AI Readiness:** Bridges the gap between rigid, nested XML structures and the fluid, context-rich format required by modern LLMs.
- **Seamless Integration:** Provides a machine-to-machine ready output that integrates directly into data pipelines.
- **Accessibility:** Simplifies the retrieval of Italian legislation by handling the complexities of Normattiva's URL structure and search mechanisms.

## Critical Success Factors
- **Automated Intelligence:** Success is defined by the tool's ability to automatically download, lookup, and convert laws from a simple URL or a natural language search query (via Exa AI).
- **Granular Extraction:** The ability to handle cross-references and extract specific articles accurately is paramount for precise legal analysis.
- **Structural Integrity:** Ensuring high-fidelity conversion through automated validation and structural comparison between XML and Markdown.

## Design Philosophy
- **Zero-Config & Battery-Included:** The tool should work immediately with sensible defaults, automatically detecting URL types and handling downloads without manual user intervention.
- **Extensible & Modular:** While primarily a CLI, the codebase is structured to be integrated as a library into larger Python AI ecosystems.
- **Minimalist & Precise:** Maintains high-quality, lightweight conversion with minimal external dependencies, ensuring speed and portability.
