---
name: higgsfield-troubleshoot
description: "Use when a Higgsfield generation fails, looks wrong, ignores the prompt, wastes credits, has identity/style/motion/audio problems, or needs a repair plan."
user-invocable: true
metadata:
  tags: [higgsfield_troubleshoot, routing, verification, workflow]
  version: 3.1.0
  updated: 2026-08-25
---

# Higgsfield Troubleshooting

This concise entrypoint routes the task and defines the contract. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` and any relevant sub-skill before diagnosing.
- Start from observed symptoms and source inputs, not generic advice.
- Separate prompt problems from model/workspace/input/schema/platform problems.
- Recommend the cheapest useful retry before high-cost regeneration.

## Output Contract

- Likely cause ranked by confidence.
- Concrete fix or rewritten prompt segment.
- Preflight checks before the next generation.

## Verification

- Confirm routed references/templates/tools exist before relying on them.
- Verify time-sensitive model, platform, pricing, workspace, or UI facts before presenting them as current.
- Run the smallest useful smoke check, lint, or self-check available for the workflow.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading sensitive/private media, or changing account state.
- Do not use private likeness, voice, identity, confidential business context, or copyrighted material without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
