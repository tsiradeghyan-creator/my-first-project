---
name: higgsfield-recall
description: "Use for Higgsfield generation memory, past failure checks, kept/rejected/flagged result logging, takes-per-kept analysis, and credit-efficiency recall."
user-invocable: true
metadata:
  tags: [higgsfield_recall, higgsfield, workflow, verification]
  version: 3.1.0
  updated: 2026-08-25
  parent: higgsfield
---

# Higgsfield Recall

Concise entrypoint for this Higgsfield sub-skill. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before logging or applying memory.
- Check prior failures before repeating a prompt pattern.
- Log only user-provided or run-observed outcomes.
- Separate remembered evidence from inference.

## Output Contract

- Relevant prior memory or an explicit no-match result.
- Applied fix or logging entry.
- Confidence and any missing evidence.

## Verification

- Verify current model, preset, app, plan, cost, UI, and parameter facts before spend or execution.
- Check any referenced files, specs, ledgers, or templates exist before relying on them.
- Run the smallest useful preflight, lint, or self-check before generation.

## Safety Boundaries

- Get explicit approval before spending credits, batch generation, publishing, uploading private media, or changing account state.
- Do not use private likeness, voice, identity, copyrighted material, or brand assets without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
