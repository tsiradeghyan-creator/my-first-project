---
name: graphify
description: "Use for questions about a codebase, folder, architecture, file relationships, or project content, especially when graphify-out/graph.json exists. Builds or queries a persistent knowledge graph with audit trails, community detection, HTML, GraphRAG JSON, and GRAPH_REPORT.md."
metadata:
  version: 1.1.0
---

# Graphify

Concise entrypoint for graph-backed project understanding. The complete legacy runbook is preserved in `references/full-guide.md`; load it before executing anything beyond a simple existing-graph query.

## Fast Routing

- If the user asks `/graphify --help` or `/graphify -h`, read the `## Usage` section from `references/full-guide.md`, print that section verbatim, and stop.
- If `graphify-out/graph.json` exists and the user asks a natural-language question about the corpus, run the query path from `references/query.md`; do not rebuild by default.
- If the user asks to build, update, merge, export, transcribe, watch, push to Neo4j/FalkorDB, or install hooks, read `references/full-guide.md` plus the named reference file for that mode.
- If no path is given for a build, use the current working directory.

## Required References

- `references/full-guide.md` — complete pipeline and command details.
- `references/query.md` — existing-graph questions, paths, explanations, fallbacks.
- `references/github-and-merge.md` — GitHub URLs or multi-repo merges.
- `references/transcribe.md` — video/audio corpora.
- `references/exports.md` — wiki, SVG, GraphML, Neo4j, FalkorDB, MCP, benchmarks.
- `references/add-watch.md` — URL ingestion and watch mode.
- `references/hooks.md` — commit hook and native integration.

## Output Contract

- For builds: corpus summary, skipped-sensitive count, generated output paths, token/cost summary, and selected GRAPH_REPORT.md sections.
- For queries: answer only from graph output, cite source locations when specific facts are used, and name traversal/fallback mode.
- For updates/exports: exact command path used, files written, and any skipped or failed step.

## Verification

- Confirm `graphify-out/.graphify_python` or resolve the interpreter before subcommands.
- Check `graphify-out/graph.json` exists before query/path/explain flows.
- Run the graph health check from `references/full-guide.md` after a build before reporting success.
- Never hide failed chunks, missing semantic files, or low cohesion scores.

## Safety Boundaries

- Get explicit approval before installing packages, cloning private repos, pushing to databases, starting watch mode, or processing sensitive folders.
- Do not ask for unrelated API keys; Graphify can run code extraction without them.
- Do not delete source files. Cleanup applies only to Graphify temporary files listed in the runbook.
- Warn before HTML visualization on very large graphs.

## Honesty Rules

- Never invent nodes or edges.
- Distinguish EXTRACTED, INFERRED, and AMBIGUOUS relationships.
- Treat the graph as evidence, not omniscience.
