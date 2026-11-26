---
name: higgsfield-prompt
description: "Higgsfield prompt settings and repair: the MCSLA layers, prompt types, length targets, identity-vs-motion split, iteration and diagnostic rules, and engine constraints. Use to adapt a planned prompt to Higgsfield or to fix a Higgsfield prompt that misfires."
user-invocable: true
metadata:
  version: 1.2.0
  updated: 2026-11-26
  parent: higgsfield
  architecture: progressive-disclosure
---

# Higgsfield Prompt Engineering

Read the relevant sections of `references/full-guide.md` before giving final settings, prompts or steps; broad routing starts at the parent `higgsfield` skill.

- **For:** the Higgsfield layer of a prompt: MCSLA structure (Model, Camera, Subject, Look, Action), length and one-action limits, the identity/motion split for Soul ID, and the one-variable iteration rule.
- **Use when:** a prompt is headed for a Higgsfield model and needs its settings, or a Higgsfield result misfires and needs diagnosis. Before writing a prompt, run `film-crew` (single-shot mode for one shot, full mode for several) per CLAUDE.md, and take its plan as input. If a film-crew plan already exists, use it.
- **Guide sections** (`references/full-guide.md`): The MCSLA Formula · Prompt Types · Narrative Structure · High-Performing Prompt Patterns · The Pre-Prompt Checklist · One Action Per Scene · Generic-Emotion Decomposition · Identity vs. Motion Separation · Conflict resolution between sub-skills · Common Prompt Mistakes · Systematic or Stochastic? · The Iteration Rule · Seedance 2.0 sections.
- **Hands off to:** the model skill writes the final text (`seedance-25-director`, `banana-pro-director-2.0`, `cinema-worldbuilder-pro-2.0`); model choice to `higgsfield-models`; engine detail to `higgsfield-seedance` (2.0) or `higgsfield-cinema`.
- **Limits:** do not spend credits, publish, change accounts or approve rights/likeness use without the user's go-ahead; verify time-sensitive model facts against `../../specs/` or live before stating them.
