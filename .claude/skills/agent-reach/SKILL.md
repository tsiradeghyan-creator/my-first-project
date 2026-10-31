---
name: agent-reach
description: "Use for internet research or platform lookup across web, social, video, GitHub, jobs, RSS, and market-discussion sources when the user asks to search, research, look up, or inspect a URL/platform."
user-invocable: true
metadata:
  tags: [agent_reach, research, workflow, verification]
  version: 1.1.0
  updated: 2026-08-25
---

# Agent Reach

This concise entrypoint preserves routing and safety. The complete older guide is stored in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before user-facing work from this skill.

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
