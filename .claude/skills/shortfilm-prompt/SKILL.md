---
name: shortfilm-prompt
description: "Use for cinematic AI short-film prompts that need the 5-stage structure: transformation, multi-shot narrative, emotional family/pet/farewell, weapon-charge/combat, or tightly storyboarded video sequences."
user-invocable: true
metadata:
  tags: [shortfilm_prompt, routing, workflow, verification]
  version: 1.1.0
  updated: 2026-08-25
---

# Shortfilm Prompt

This is the concise entrypoint. The older full playbook is preserved in `references/full-guide.md` and must be loaded only when this skill is actually routed.

## Required Reference

- `references/full-guide.md`

## Operating Contract

- Read `references/full-guide.md` and the matching `templates/*.md` file before producing a final prompt.
- Use the 5-stage structure unless the user explicitly asks for a different format.
- Ask at most 2-3 questions only when duration, subject, or scene is too unclear to draft responsibly.
- Treat model-specific advice as time-sensitive; verify current model/platform behavior when it matters.

## Output Contract

- A ready-to-paste 5-stage prompt.
- A short note explaining 2-3 important choices.
- One current model/platform caveat when relevant.

## Verification

- Confirm the chosen template exists and was read.
- Self-check stage coverage: theme, subject/scene, atmosphere, camera, storyboard.
- Check IP, likeness, violence, and sensitive-content constraints before final delivery.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading private media, or changing account/platform state.
- Do not use private likeness, voice, protected identity, or rights-sensitive material without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
- Treat model names, platform features, prices, schedules, and public claims as time-sensitive.
