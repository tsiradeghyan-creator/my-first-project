---
name: higgsfield-canvas
description: "Use for Higgsfield Canvas, node graphs, infinite boards, connected prompt-image-video pipelines, reusable templates, assets-as-nodes, and shared canvas workflows."
user-invocable: true
metadata:
  tags: [higgsfield_canvas, research, workflow, verification]
  version: 1.1.0
  updated: 2026-08-25
---

# Higgsfield Canvas

This concise entrypoint preserves routing and safety. The complete older guide is stored in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before user-facing work from this skill.

## Operating Contract

- Read `references/full-guide.md` before describing Canvas workflows.
- Verify current node types, supported models, costs, and collaboration limits when the user plans to build or spend.
- Route model-specific prompt craft to the relevant Higgsfield sub-skill.
- Design pipelines as reusable graph patterns rather than one-off loose steps.

## Output Contract

- A node-graph plan or Canvas workflow.
- Required input assets and downstream model handoffs.
- Cost/credit caveats when generation nodes are involved.

## Verification

- Verify current platform names, UI labels, model support, costs, or backend availability before treating them as current.
- Confirm source files, references, or commands exist before citing them.
- Prefer the smallest useful check before spending credits or running a larger workflow.

## Safety Boundaries

- Do not publish, message, post, comment, like, buy, spend credits, or mutate accounts without explicit approval.
- Do not upload sensitive/private media or confidential files unless the user has clearly authorized that workflow.
- Do not delete, overwrite, or move user files unless explicitly asked.
- Respect IP, likeness, privacy, and platform terms.
