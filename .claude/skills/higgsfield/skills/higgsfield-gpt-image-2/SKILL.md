---
name: higgsfield-gpt-image-2
description: "Use for GPT Image 2.0 / gpt-image-2 prompting in Higgsfield, including UI mockups, infographics, text-heavy images, reference sheets, and layout-dense static assets."
user-invocable: true
metadata:
  tags: [higgsfield_gpt_image_2, higgsfield, workflow, verification]
  version: 3.1.0
  updated: 2026-08-25
  parent: higgsfield
---

# Higgsfield GPT Image 2

Concise entrypoint for this Higgsfield sub-skill. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before drafting image prompts.
- Keep layout, text, and asset requirements explicit and verifiable.
- Use overlay or programmatic text when exact typography is required.
- Verify current model availability/settings when it affects the user's run.

## Output Contract

- A paste-ready image prompt.
- Layout/text constraints and aspect ratio.
- A QA checklist for text, composition, and rights.

## Verification

- Verify current model, preset, app, plan, cost, UI, and parameter facts before spend or execution.
- Check any referenced files, specs, ledgers, or templates exist before relying on them.
- Run the smallest useful preflight, lint, or self-check before generation.

## Safety Boundaries

- Get explicit approval before spending credits, batch generation, publishing, uploading private media, or changing account state.
- Do not use private likeness, voice, identity, copyrighted material, or brand assets without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
