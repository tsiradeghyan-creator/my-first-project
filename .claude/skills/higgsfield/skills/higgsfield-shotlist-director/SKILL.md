---
name: higgsfield-shotlist-director
description: "Use to turn a script, brief, treatment, or story idea into a connected director shotlist with global style, asset glossary, and named per-scene Seedance prompts."
user-invocable: true
metadata:
  tags: [higgsfield_shotlist_director, routing, verification, workflow]
  version: 1.1.0
  updated: 2026-08-25
---

# Higgsfield Shotlist Director

This concise entrypoint routes the task and defines the contract. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` and `../higgsfield-seedance/SKILL.md` before creating or revising a shotlist.
- Produce one connected artifact, not scattered loose prompts.
- Preserve scene numbering and global style semantics when revising.
- Preflight-lint prompts when execution is intended.

## Output Contract

- A self-contained shotlist artifact or precise revision to one.
- Global style prefix, asset glossary, and named per-scene prompts.
- Any lint or generation-risk notes.

## Verification

- Confirm routed references/templates/tools exist before relying on them.
- Verify time-sensitive model, platform, pricing, workspace, or UI facts before presenting them as current.
- Run the smallest useful smoke check, lint, or self-check available for the workflow.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading sensitive/private media, or changing account state.
- Do not use private likeness, voice, identity, confidential business context, or copyrighted material without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
