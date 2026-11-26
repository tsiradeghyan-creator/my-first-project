---
name: agent-reach
description: "Use for lookups on logged-in social platforms and platform CLIs: X/Twitter, Reddit, Bilibili, Xiaohongshu, YouTube transcripts and the like, when the agent-reach CLI is installed. General web research and URL reading stay with the normal web tools (WebSearch, Perplexity, Firecrawl)."
user-invocable: true
metadata:
  tags: [agent_reach, research, workflow, verification]
  version: 1.2.0
  updated: 2026-11-26
---

# Agent Reach

This concise entrypoint preserves routing and safety. The complete older guide is stored in `references/full-guide.md`.

## Scope

This skill covers platforms that need a login or a platform CLI: X/Twitter, Reddit, Bilibili, Xiaohongshu, YouTube transcripts, and similar. General web research, search and reading a URL stay with the built-in web tools (WebSearch, Perplexity, Firecrawl).

## First: Is the CLI Installed?

Before reading `references/full-guide.md`, check for the CLI: `command -v agent-reach` (or `agent-reach doctor`). If it is not installed, do not use this skill's commands; use the built-in web tools (WebSearch, Perplexity, Firecrawl) instead and say which platform could not be reached directly.

## Required Reference

When the CLI is installed, read `references/full-guide.md` before user-facing work from this skill.

## Operating Contract

- Read `references/full-guide.md` and the relevant category reference before running platform commands.
- Run `agent-reach doctor --json` when backend/login state affects the task.
- Use the platform-specific retry chain from references instead of inventing commands.
- Collect source links and distinguish observed facts from inference.

## Output Contract

- Findings with source links or command-derived evidence.
- Backend/platform used when relevant.
- Gaps, failed channels, and retry status.

## Verification

- Verify current platform names, UI labels, model support, costs, or backend availability before treating them as current.
- Confirm source files, references, or commands exist before citing them.
- Prefer the smallest useful check before spending credits or running a larger workflow.

## Safety Boundaries

- Do not publish, message, post, comment, like, buy, spend credits, or mutate accounts without explicit approval.
- Do not upload sensitive/private media or confidential files unless the user has clearly authorized that workflow.
- Do not delete, overwrite, or move user files unless explicitly asked.
- Respect IP, likeness, privacy, and platform terms.
