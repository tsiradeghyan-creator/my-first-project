---
name: higgsfield-seedance
description: "Seedance 2.0 on Higgsfield: the filter model, fail diagnostics, six-slot formula, prompt modes, reference roles, frame coordinates, keyframes, the preflight linter and failure loops. Use for Seedance 2.0-only work or to diagnose a Seedance run on Higgsfield; Seedance 2.5 prompts go to seedance-25-director."
user-invocable: true
metadata:
  version: 1.2.0
  updated: 2026-11-26
  parent: higgsfield
  architecture: progressive-disclosure
---

# Higgsfield Seedance Director (Seedance 2.0)

Read the relevant sections of `references/full-guide.md` before giving final settings, prompts or steps; broad routing starts at the parent `higgsfield` skill.

- **For:** Seedance 2.0 work on Higgsfield and the platform side of any Seedance run: filter rejections, instant vs delayed fails, reference roles, the preflight linter (`../../scripts/seedance_lint.py`), extensions and repair loops.
- **Use when:** the user is on Seedance 2.0, a Seedance run on Higgsfield failed, or a prompt needs preflight before spending credits. New work defaults to Seedance 2.5 (`seedance_2_5`, verify live) with `seedance-25-director` writing the prompt.
- **Guide sections** (`references/full-guide.md`): The Filter Model · Instant Fail vs. Delayed Fail · The Seedance Prompt Formula · Prompt-Craft Laws · Official Block Scaffold · Prompt Modes · Continuation Prompt Formula · Reference Roles · Frame Coordinate System · Spatial Layout Block · Two-Layer Prompt Authoring · Keyframe Workflow · Pre-flight Linter · The Rewrite Playbook · Failure Loop. Also `ENGINE-RULES.md`, `FAILURE-MODES.md`, `PRODUCTION-PATTERNS.md` in this folder.
- **Hands off to:** shot plans come from `film-crew`; Seedance 2.5 syntax and limits to `seedance-25-director`; footage transforms to `higgsfield-seedance-vfx`; facial codes to `higgsfield-facs`.
- **Limits:** do not spend credits, publish, change accounts or approve rights/likeness use without the user's go-ahead; verify time-sensitive model facts against `../../specs/` or live before stating them.
