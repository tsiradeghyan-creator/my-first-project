---
name: higgsfield-facs
description: "Facial Action Coding (FACS) guide for Higgsfield character work: Action Unit codes, emotion-to-AU recipes, FACS reference sheets and AU-per-beat dialogue acting. Use when an expression or micro-performance must be precise rather than an emotion label."
user-invocable: true
metadata:
  version: 1.2.0
  updated: 2026-11-26
  parent: higgsfield
  architecture: progressive-disclosure
---

# Higgsfield FACS Director

Read the relevant sections of `references/full-guide.md` before giving final settings, prompts or steps; broad routing starts at the parent `higgsfield` skill.

- **For:** precise facial expressions written as Action Unit codes (AU6, AU12…) instead of emotion words, plus a labelled FACS reference sheet.
- **Use when:** a close-up, monologue or dialogue beat needs a specific, mixed or uncanny expression, or the user asks which AU code fits an emotion. Plan 3–4 expressions per generation.
- **Guide sections** (`references/full-guide.md`): What FACS Is · Provenance and the "Not a Guarantee" Rule · The Plan-First Workflow · Step 1 Generate the FACS Reference Sheet · Step 2 Put AU Codes in the Seedance Prompt · AU Code Reference · Emotion → AU Recipes · Dialogue & Monologue Facial Acting · Worked Examples.
- **Hands off to:** the AU beats go into the prompt the model skill writes from the `film-crew` plan (`seedance-25-director` for Seedance 2.5); lip-sync timing to `higgsfield-audio`; identity to `higgsfield-soul`. The guide's examples use Seedance 2.0.
- **Limits:** do not spend credits, publish, change accounts or approve rights/likeness use without the user's go-ahead; verify time-sensitive model facts against `../../specs/` or live before stating them.
