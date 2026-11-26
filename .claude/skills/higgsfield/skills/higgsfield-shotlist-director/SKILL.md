---
name: higgsfield-shotlist-director
description: "Formatter that turns a film-crew shot plan into one connected Higgsfield shotlist: a single editable HTML artifact with a global style prefix, an @-asset glossary, named per-scene prompts and their Higgsfield settings. Use when a film-crew plan exists (or has just been made) and the user wants it as a Higgsfield shotlist, or wants an existing shotlist revised. Not for planning the shots themselves; that is film-crew's job."
user-invocable: true
metadata:
  tags: [higgsfield_shotlist_director, formatter, film-crew, shotlist, verification, workflow]
  version: 1.2.0
  updated: 2026-11-26
  parent: higgsfield
---

# Higgsfield Shotlist Director

This sub-skill is the formatter between `film-crew` and Higgsfield. `film-crew` plans the shots (director, design, costume, DP, editor, camera, sound); this skill lays that plan out as one connected Higgsfield shotlist with the settings each shot needs. The full playbook (HTML skeleton, layers, edit-once semantics) is in `references/full-guide.md`.

## Where it sits

- **Before:** `film-crew` (full mode for several shots, single-shot mode for one). If no film-crew plan exists, run `film-crew` first and take its plan as input. If a plan already exists, use it.
- **Prompt text:** the model skill writes the final prompt wording from the plan: `seedance-25-director` for Seedance 2.5 (the default), `higgsfield-seedance` for Seedance 2.0-only work, `cinema-worldbuilder-pro-2.0` for other video engines.
- **This skill:** global style prefix, `@`-asset glossary, scene numbering (1a, 1b, 2a…), per-scene Higgsfield settings (model, duration, aspect ratio, references, presets), preflight notes, and the single HTML artifact.
- **After:** `higgsfield-pipeline` for production handoffs, `higgsfield-recall` to log kept and rejected takes.

## Operating Contract

- Read `references/full-guide.md` before building or revising a shotlist.
- Keep the film-crew plan's shot order, beats and handoff contracts; do not re-plan shots here. If the plan has a gap, send it back to `film-crew` rather than inventing shots.
- Produce one connected artifact, not scattered loose prompts.
- Preserve scene numbering and global style semantics when revising.
- Check model settings against `../../specs/model-specs.yaml`; if the snapshot is older than ~30 days or the model is new, verify live.
- Preflight-lint prompts when execution is intended.

## Output Contract

- A self-contained shotlist artifact or a precise revision to one.
- Global style prefix, asset glossary, named per-scene prompts and their Higgsfield settings.
- Any lint or generation-risk notes.

## Verification

- Confirm routed references, templates and tools exist before relying on them.
- Verify time-sensitive model, platform, pricing, workspace or UI facts before presenting them as current.
- Run the smallest useful smoke check, lint or self-check available for the workflow.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading sensitive or private media, or changing account state.
- Do not use private likeness, voice, identity, confidential business context or copyrighted material without clear authorization.
- Do not delete, overwrite or move user files unless explicitly asked.
