---
name: higgsfield-assist
description: "Use for Higgsfield Assist, credit strategy, plan selection, budget optimization, preflight advice, workflow triage, and practical platform guidance."
user-invocable: true
metadata:
  tags: [higgsfield_assist, higgsfield, workflow, verification]
  version: 3.1.0
  updated: 2026-08-25
  parent: higgsfield
---

# Higgsfield Assist

Concise entrypoint for this Higgsfield sub-skill. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before advising.
- Verify current pricing, plans, limits, and credits before financial recommendations.
- Prefer cheaper validation loops before expensive generations.
- Do not claim guaranteed savings without measured evidence.

## Output Contract

- Recommended workflow or budget plan.
- Cost/risk assumptions.
- Next preflight step before spend.

## Verification

- Verify current model, preset, app, plan, cost, UI, and parameter facts before spend or execution.
- Check any referenced files, specs, ledgers, or templates exist before relying on them.
- Run the smallest useful preflight, lint, or self-check before generation.

## Safety Boundaries

- Get explicit approval before spending credits, batch generation, publishing, uploading private media, or changing account state.
- Do not use private likeness, voice, identity, copyrighted material, or brand assets without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
