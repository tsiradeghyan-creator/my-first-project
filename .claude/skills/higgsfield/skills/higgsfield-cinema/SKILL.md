---
name: higgsfield-cinema
description: "Higgsfield Cinema Studio guide (versions 2.5, 3.0 and 3.5; 4.0 exists, verify live): version detection, Elements, Soul Cast, genre/style/camera settings, the 512-character prompt cap, shot modes, color grading and output settings. Use when the user works in Cinema Studio or needs its settings for a planned shot."
user-invocable: true
metadata:
  version: 1.2.0
  updated: 2026-11-26
  parent: higgsfield
  architecture: progressive-disclosure
---

# Higgsfield Cinema Studio

Read the relevant sections of `references/full-guide.md` before giving final settings, prompts or steps; broad routing starts at the parent `higgsfield` skill.

- **For:** running shots in Cinema Studio: picking the version, Elements (@Characters/@Locations/@Props), Soul Cast, the settings strip, prompt limits and output controls. The guide covers 2.5, 3.0 and 3.5; Cinema Studio 4.0 exists and is not yet covered here, so verify its settings live.
- **Use when:** the user names Cinema Studio, or a film-crew plan needs to be set up and run there. Ask which version they have before giving settings.
- **Guide sections** (`references/full-guide.md`): Version Detection · The 10-Step Workflow · Elements System · Soul Cast · Color Grading · Optical Physics · Director Panel · Shot Modes · Reference Anchor System · Hero Frame · Prompt Character Limit (512) · Model Selection · Cinema Studio 3.0 · Cinema Studio 3.5 · Resolution Decision Matrix.
- **Hands off to:** shot planning comes from `film-crew`, and prompt text from the model skill (`seedance-25-director` for Seedance 2.5); identity locks to `higgsfield-soul`; multi-shot formatting to `higgsfield-shotlist-director`.
- **Limits:** do not spend credits, publish, change accounts or approve rights/likeness use without the user's go-ahead; verify time-sensitive model facts against `../../specs/` or live before stating them.
