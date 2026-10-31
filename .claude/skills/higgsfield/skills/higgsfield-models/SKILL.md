---
name: higgsfield-models
description: "Use for Higgsfield model selection, capability comparison, parameter constraints, quality/speed/cost tradeoffs, and current model availability checks."
user-invocable: true
metadata:
  tags: [higgsfield_models, higgsfield, workflow, verification]
  version: 3.1.0
  updated: 2026-08-25
  parent: higgsfield
---

# Higgsfield Models

Concise entrypoint for this Higgsfield sub-skill. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before making model recommendations.
- Check local specs first, then verify live if the snapshot is stale or spend is likely.
- Separate image, video, audio, app, and Cinema Studio surfaces.
- State assumptions when exact current availability is not verified.

## Output Contract

- Recommended model and backup.
- Capability/cost/speed rationale.
- Parameter or platform caveats that affect generation.

## Verification

- Verify current model, preset, app, plan, cost, UI, and parameter facts before spend or execution.
- Check any referenced files, specs, ledgers, or templates exist before relying on them.
- Run the smallest useful preflight, lint, or self-check before generation.

## Safety Boundaries

- Get explicit approval before spending credits, batch generation, publishing, uploading private media, or changing account state.
- Do not use private likeness, voice, identity, copyrighted material, or brand assets without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
