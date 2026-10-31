---
name: higgsfield-content-factory
description: "Use for Higgsfield campaign pipelines: research, plan, generate, publish-prep, report, batch ads, UGC variations, cost tracking, and production orchestration."
user-invocable: true
metadata:
  tags: [higgsfield_content_factory, higgsfield, workflow, verification]
  version: 3.1.0
  updated: 2026-08-25
  parent: higgsfield
---

# Higgsfield Content Factory

Concise entrypoint for this Higgsfield sub-skill. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before planning a campaign pipeline.
- Keep research, generation, approval, publishing, and reporting as distinct gates.
- Require explicit approval before batch generation, publishing, or spend.
- Track artifacts, prompts, costs, and outcomes as receipts.

## Output Contract

- Campaign pipeline with phases and gates.
- Artifact list and batch limits.
- Approval points and measurement plan.

## Verification

- Verify current model, preset, app, plan, cost, UI, and parameter facts before spend or execution.
- Check any referenced files, specs, ledgers, or templates exist before relying on them.
- Run the smallest useful preflight, lint, or self-check before generation.

## Safety Boundaries

- Get explicit approval before spending credits, batch generation, publishing, uploading private media, or changing account state.
- Do not use private likeness, voice, identity, copyrighted material, or brand assets without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
