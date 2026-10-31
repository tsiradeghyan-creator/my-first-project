---
name: agent-harness-construction
description: Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates.
origin: ECC — light update 2026-10-15 (deferred tools, caching, parallelism, re-test per model)
---

# Agent Harness Construction

Use this skill when you are improving how an agent plans, calls tools, recovers from errors, and converges on completion.

## Core Model

Agent output quality is constrained by:
1. Action space quality
2. Observation quality
3. Recovery quality
4. Context budget quality

## Action Space Design

1. Use stable, explicit tool names.
2. Keep inputs schema-first and narrow.
3. Return deterministic output shapes.
4. Avoid catch-all tools unless isolation is impossible.

## Granularity Rules

- Use micro-tools for high-risk operations (deploy, migration, permissions).
- Use medium tools for common edit/read/search loops.
- Use macro-tools only when round-trip overhead is the dominant cost.

## Observation Design

Every tool response should include:
- `status`: success|warning|error
- `summary`: one-line result
- `next_actions`: actionable follow-ups
- `artifacts`: file paths / IDs

## Error Recovery Contract

For every error path, include:
- root cause hint
- safe retry instruction
- explicit stop condition

## Context Budgeting

1. Keep system prompt minimal and invariant.
2. Move large guidance into skills loaded on demand.
3. Prefer references to files over inlining long documents.
4. Compact at phase boundaries, not arbitrary token thresholds.
5. Defer rarely used tools: list them by name only and load a tool's full schema on first use, as Claude Code's deferred tools and tool search do. Dozens of always-loaded schemas cost context on every turn.
6. Keep the cached prefix stable (system prompt, tool list, early messages) so prompt caching keeps hitting. A tool list that changes order per call silently destroys the cache.

## Parallelism

- Let the model issue independent tool calls in one turn; return each result separately, with the same shape.
- Hand broad, read-heavy searches to a subagent that returns a conclusion, not file dumps, so the main context stays small.

## Architecture Pattern Guidance

- ReAct: best for exploratory tasks with uncertain path.
- Function-calling: best for structured deterministic flows.
- Hybrid (recommended): ReAct planning + typed tool execution.

## Benchmarking

Track:
- completion rate
- retries per task
- pass@1 and pass@3
- cost per successful task

Re-run the benchmark whenever the model changes. Every piece of scaffolding encodes an assumption about what the model cannot do alone. Remove one component at a time, keep what is still load-bearing, and drop the rest (see `gan-style-harness` → *Re-test the harness with every new model*). Measure with `eval-harness`.

## Anti-Patterns

- Too many tools with overlapping semantics.
- Opaque tool output with no recovery hints.
- Error-only output without next steps.
- Context overloading with irrelevant references.
