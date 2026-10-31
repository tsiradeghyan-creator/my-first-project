---
name: higgsfield-camera
description: "Use for Higgsfield camera controls, camera movement presets, shot grammar, framing, lens/motion advice, and prompt camera lines."
user-invocable: true
metadata:
  tags: [higgsfield_camera, higgsfield, workflow, verification]
  version: 3.1.0
  updated: 2026-08-25
  parent: higgsfield
---

# Higgsfield Camera

Concise entrypoint for this Higgsfield sub-skill. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before naming camera controls.
- Use exact camera/control names from the reference or verified platform data.
- Match movement to subject action and shot duration.
- Verify current enums when the user will spend credits.

## Output Contract

- Recommended camera move or shortlist.
- A paste-ready camera line.
- Risk notes for complex motion, faces, or continuity.

## Verification

- Verify current model, preset, app, plan, cost, UI, and parameter facts before spend or execution.
- Check any referenced files, specs, ledgers, or templates exist before relying on them.
- Run the smallest useful preflight, lint, or self-check before generation.

## Safety Boundaries

- Get explicit approval before spending credits, batch generation, publishing, uploading private media, or changing account state.
- Do not use private likeness, voice, identity, copyrighted material, or brand assets without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
