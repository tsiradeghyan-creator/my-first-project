---
name: llm-council
description: "Use when the user explicitly asks to council, pressure-test, stress-test, debate, or evaluate a meaningful decision with real tradeoffs and stakes."
user-invocable: true
metadata:
  tags: [llm_council, routing, verification, workflow]
  version: 1.1.0
  updated: 2026-08-25
---

# LLM Council

This concise entrypoint routes the task and defines the contract. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before running a council.
- Use the council only for decisions with meaningful uncertainty, tradeoffs, and stakes.
- Gather only directly relevant local context before framing the question.
- Keep advisor outputs independent and synthesis decisive.

## Output Contract

- Council verdict with agreement, clashes, blind spots, recommendation, and one first step.
- Any assumptions or missing context that materially affect the verdict.
- No council for simple factual lookups or ordinary generation tasks.

## Verification

- Confirm routed references/templates/tools exist before relying on them.
- Verify time-sensitive model, platform, pricing, workspace, or UI facts before presenting them as current.
- Run the smallest useful smoke check, lint, or self-check available for the workflow.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading sensitive/private media, or changing account state.
- Do not use private likeness, voice, identity, confidential business context, or copyrighted material without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
