## Context
Goal: deliver a browser “light” conversion path without replacing the CLI. Normattiva
blocks CORS, so a controlled proxy is required. Conversion core must stay pure
(XML string in, Markdown string out) to run in Pyodide.

## Goals / Non-Goals
- Goals: proxy with CORS, URL whitelist, size/rate limits; pure conversion entry
  point for Pyodide; minimal client (bookmarklet/extension) to glue them.
- Non-Goals: replicate CLI features like batch references download or file I/O.

## Decisions
- Proxy: Cloudflare Worker/Pages Function. Accepts only normattiva.it endpoints
  (`uri-res/N2Ls`, `do/atto/caricaAKN`). Optional token header for access.
- Param extraction: if input is permalink HTML, Worker extracts dataGU,
  codiceRedaz, dataVigenza via regex and then fetches `caricaAKN`. Keeps client
  simple.
- Safety: reject bodies >8MB, enforce ≥1s delay between upstream fetches,
  cache-control 5m, strip/set CORS headers (`Access-Control-Allow-Origin: *`).
- Conversion API: add `convert_xml_text_to_md(xml_text, metadata=None)` that
  reuses markdown_converter pipeline without filesystem.
- Client: bookmarklet or extension loads Pyodide, calls Worker, converts XML,
  offers download via blob. No persistent storage required.

## Risks / Trade-offs
- Reliance on Normattiva HTML structure for param scraping may break; mitigation:
  keep parser minimal and log failures.
- Worker could be abused as open proxy; mitigation: strict URL whitelist +
  optional shared secret + rate limiting.
- Initial Pyodide load (~7–8MB) adds startup latency; acceptable for “light”
  mode, not for bulk workflows.

## Open Questions
- Where to host Worker secret/config? (KV vs env vars)
- Should we expose a small JSON status endpoint for health/rate-limit info?

