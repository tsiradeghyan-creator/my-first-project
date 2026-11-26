---
name: cinema-worldbuilder-pro-2.0
description: Engine-agnostic AI video prompt director for cinematic scene prompts, reference-aware shot design, character/environment locking, motion, final-frame control, and diegetic sound specs. Use for video-generation prompts on engines other than Seedance 2.5 (that goes to seedance-25-director); not for still-image prompts, full short-film production pipelines, or platform/account troubleshooting.
metadata:
  version: 2.1.0
  architecture: progressive-disclosure
---

# Cinema Worldbuilder Pro 2.0 — AI Video Prompt Director
> Studio prompt craft: also apply `.claude/skills/film-crew/references/prompt-craft.md` (§2–§6 and the §10 check). Where it conflicts with this skill's engine adapter, the adapter wins.


Produce production-grade AI video prompts while keeping the heavy cinematography doctrine in `references/full-guide.md`.

## When To Use

Use this skill for:

- AI video prompts,
- cinematic scene breakdowns for video generation,
- narrative shots, action shots, performance scenes, fashion films, music-video-style scenes, and atmospheric environment plates,
- reference-aware character/environment locking,
- engine retargeting across Veo, Kling, Wan, Hailuo, Runway, Luma, or future models (Seedance 2.5 execution goes to `seedance-25-director`).

Do not use it for still images, full multi-stage short-film production, Higgsfield account/UI/model-picking support, or garment-led fashion campaigns when a more specific fashion skill applies.

## Before Writing

Before writing a prompt, run `film-crew` (single-shot mode for one shot, full mode for several) per CLAUDE.md, and take its plan as input. If a film-crew plan already exists, use it.

## Required Reference Loading

Read `references/full-guide.md` before writing final prompts. For quick routing, use this `SKILL.md` first and open the full guide after the mode/engine is clear.

Search the full guide for these anchors:

- `TARGET ENGINE ADAPTER`
- `HOW TO USE THIS SKILL`
- `CORE PHILOSOPHY`
- `TEN-BLOCK OUTPUT`
- `Frame Map`
- `Subject Lock`
- `Cross-Frame Rules`
- `Movement`
- `Last Frame`
- `Sound Bed`
- `FINAL QA`

## Operating Contract

1. Establish target engine and runtime. If unspecified, ask once which engine it runs on; if the user does not care, suggest Kling or Veo. If the target is **Seedance** (Seedance 2.5 on Dreamina/Jimeng/Higgsfield), hand the model-specific execution — modes, limits, @-reference binding, timestamps, extension/edit/Long Video syntax — to `seedance-25-director`; keep this skill's shot intent and continuity as its input. A **multi-shot sequence** (scene, short, ad, trailer, storyboard/раскадровка) is planned by `film-crew` in full mode first; this skill then writes the per-shot prompts for non-Seedance engines.
2. Read attached references and lock only what matters: identity, wardrobe, environment, props, screen position, and continuity anchors.
3. Choose the closest mode from the full guide.
4. Build the prompt around the ten production blocks in order:
   - Scene & Mood
   - Frame Map
   - Subject Lock
   - Cross-Frame Rules
   - Movement
   - Last Frame
   - World Plate
   - Sound Bed
   - Capture Realism
   - Camera Capture
5. Adapt syntax to the engine, but do not drop the underlying block content.

## Output Contract

Return:

- target engine and runtime,
- reference order or descriptor anchors,
- one copyable English prompt in a fenced code block,
- post-production sound note when the engine is silent,
- short QA note listing continuity, motion, final frame, realism, and rights checks.

## Verification

Before final answer:

- first and last frame are both specified,
- every character/object has a stable anchor,
- movement names what changes and what must stay locked,
- sound is diegetic only unless the user explicitly asks for music outside the prompt,
- no unsupported model capability is asserted without current confirmation,
- no face/likeness, brand, location, copyrighted material, or paid generation is approved silently,
- any Armenian text is proper Eastern Armenian Unicode and should be overlay text unless explicitly safe for generation.

## Safety Boundaries

Do not approve spending, publishing, face/likeness rights, brand use, location use, account changes, or sensitive claims. Flag them for the user instead.
