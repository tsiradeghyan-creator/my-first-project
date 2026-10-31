---
name: film-crew
description: AI film crew for multi-shot film, scene, trailer, music-video or ad pre-production. Seven departments work in a fixed order — Director, Production Designer, Costume Designer, Cinematographer (DP), Editor, Camera Operator, Sound Designer — so each shot is planned knowing the shots around it and the generated clips cut together. Delivers director's script, world bible, camera & light plan, pre-edit with a handoff contract per cut, exact camera moves, sound plan, storyboard, keyframe + video prompts and a generation plan, in the style of any named director, cinematographer or film — 12 lenses ready (Kubrick, Tarantino, Parajanov, Tarkovsky…), any other researched from real sources. Use for any multi-shot scene, even when the target is Seedance 2.5: "make a film/scene/ad with AI", "30-s scene in X style", storyboard / раскадровка / ռասկադրովկա, director's script, "in the style of" a named director, կինո AI-ով. Not for one isolated prompt (seedance-25-director, cinema-worldbuilder-pro-2.0).
metadata:
  version: 1.0.0
  updated: 2026-10-29
---

# Film Crew

AI models fail at filmmaking for one reason: they decide each shot alone. A real crew decides each shot knowing
the story, the world, the light, the cut before it and the cut after it. This skill runs that crew.

## Language

- Talk to the user in their language (Armenian in proper Armenian Unicode, Russian, English): the questions, the
  hand-over summary and the per-shot timeline are in their language.
- Department documents (00-10) are in **English by default** — the working language of the crew and of the
  prompts. Write them in the user's language only if the user asks. Reason (tested 2026-10-29): long Armenian
  documents take 3-4× longer to generate and the model occasionally emits corrupted letters (e.g. `֖`, `�`
  instead of `ֆ`); if you do write Armenian, scan for characters outside U+0531-U+058F before saving.
- **Every image/video prompt is in English** (dialogue stays in the character's language — see the target
  model's language limits).

## The crew and the order — never change it

| # | Department | Decides | File | Reads |
|---|---|---|---|---|
| 0 | Producer (you, the orchestrator) | format, budget of shots, model, style lens, generation units | `00_brief.md` | user input |
| 1 | Director | meaning, beats, subtext, visual thesis, style lens, how scenes should feel when cut | `01_director.md` | 00 |
| 2 | Production Designer | spaces, floor plans, geography, props, palette, period | `02_world.md` | 00-01 |
| 3 | Costume Designer | each character's locked look and wardrobe states per scene | `03_costume.md` | 00-02 |
| 4 | Cinematographer (DP) | lenses, light plan, axis/180° map, coverage strategy, camera grammar | `04_camera_light.md` | 00-03 |
| 5 | Editor (pre-edit) | shot order, cut points, cut types, rhythm, **handoff contract for every cut** | `05_edit_plan.md` | 00-04 |
| 6 | Camera Operator | the exact move of every shot: start frame, path, speed, end frame | `06_shot_list.md` | 00-05 |
| 7 | Sound Designer | diegetic layers, dialogue timing, J/L cuts, sound bridges, music policy | `07_sound.md` | 00-06 |
| 8 | Assembly (you) | storyboard cards: keyframe prompt + video prompt + handoff per shot | `08_storyboard.md` | all |
| 9 | Generation plan (you) | generation units, order, chaining method, references, QC per shot | `09_generation_plan.md` | all |
| 10 | Table read (all departments) | each department checks the assembled film; editor runs the virtual cut | `10_review.md` | all |

The editor works **before** the camera operator on purpose: the cut decides the camera, not the reverse.

The departments are **passes of one agent in one context**, not separate agents. Entering a pass, load its role
file from `roles/` (progressive disclosure — only that file), do the job, write the document. Because the same
agent holds every earlier decision, a later pass that finds a problem upstream **fixes the upstream file directly**
and adds a line to `CHANGELOG` at the bottom of `00_brief.md` ("pass 5 → 02_world: moved the window to the west wall
so the axis holds") — no note ping-pong.

## Step 0 — producer intake (`00_brief.md`)

Lock, and state every assumption:

- **What:** idea / logline / script pages / existing scene, and the deliverable (scene, short, trailer, ad, MV).
- **Format:** total duration, aspect ratio, platform, resolution.
- **Target video model:** default **Seedance 2.5** (if the `seedance-25-director` skill is available, its rules
  govern prompt syntax and limits). Other models: use `references/generation-strategy.md` adapters.
- **Style lens:** one director from `styles/` (or build a new card — see below). One lens per film; a second
  director may be quoted for one scene only if the user asks.
- **Shot budget:** total duration ÷ the lens's average shot length (ASL) = number of shots. Round to whole shots and
  show the math.
- **Ask once, only what changes the plan** (story absent, duration absent for a long piece, lens absent when the
  user clearly cares). Otherwise assume visibly and proceed.

Default if unstated: 30-60 s scene, 16:9 (9:16 for Reels/TikTok/Shorts), Seedance 2.5, 720p, lens chosen by the
Director to serve the story and named with a reason.

## Style lens

- Lens cards live in `styles/` (index: `styles/README.md`). A card turns a director into concrete decisions:
  framing, lenses, movement signatures, light and colour, editing (ASL, transitions, tricks), sound and music,
  performance, and "AI translation" — the exact phrases to put in prompts.
- The lens is applied by **every** department, not just the camera: production design, costume, cut rhythm and
  sound all change with it.
- **Never write a director's name inside an image or video prompt.** Prompts carry the translated craft
  ("symmetrical one-point perspective down a corridor, 18mm wide lens, slow steady glide at hip height"), never
  "in the style of Kubrick". Names invite moderation blocks and pastiche.
- **Any filmmaker works — the library is only a cache.** The user may name any director (or a cinematographer, an
  editor, a single film, a period: "early Scorsese", "Peleshyan's distance montage", "like *In the Mood for
  Love*"). Resolve the lens in this order:
  1. a card in `styles/` that matches the name *and* the period → use it;
  2. otherwise **research a new card from real sources** — never write a lens from memory alone:
     - Claude Code: dispatch the `film-style-researcher` subagent (name, period/films, project genre, save folder).
       Research is an independent path that reads many pages and returns one compact card — the case where a
       subagent pays off. Read the returned card, spot-check two sourced claims, then use it.
     - Without subagents (Claude.ai, Cowork, ChatGPT): do the same research in the loop with web search — 5-10
       sources, at least 3 independent — then write the card with `styles/_template.md`.
     - No web access: write the card from knowledge, mark every line "(verify)", and say so in the brief.
  3. Show the card's signature line, "Based on" films and top AI-translation phrases in the brief. Save new cards to
     `styles/` as `Status: researched-unreviewed`; mark `approved` only when the user confirms. Add a row to
     `styles/README.md`.
- Two names ("Tarkovsky's time with Wong Kar-wai's colour"): one primary lens for the whole film, the second only for
  the named dimension; write which dimension comes from which card in the brief.

## Architecture — what stays in the loop, what is a tool, what is a subagent

Based on Anthropic's "When to fold subagents into your main agent loop" (2026-10-22) and on measured runs
(`evals/ARCHITECTURE.md`):

- **Main loop (everything creative).** All seven departments, assembly and the generation plan run here. They chain
  on each other's output, read the same bible and are always called together — the article's definition of
  specialists to merge. Continuity, the whole point of this skill, needs one context that has seen every decision;
  split departments play a "telephone game" across handoffs.
- **Plan first.** In `00_brief.md` write a short plan: scenes, which passes need depth, shot budget, generation
  units. Revise it as passes reveal problems — the model that writes the plan carries it out.
- **Tool (hard limits).** Mechanical checks live in `scripts/validate_package.py`, not in your judgment: files
  present, one card and handoffs per shot, one complete contract per cut, prompts copy-ready (no placeholders, no
  director names), time slices continuous and in plain seconds, per-call duration and reference limits, corrupted
  characters. Run it before hand-over (`python3 scripts/validate_package.py <project-folder>`); a FAIL blocks
  hand-over. No code execution available → walk the same list by hand.
- **One subagent: independent continuity verification.** After the validator passes, in Claude Code dispatch
  `film-continuity-verifier` with the project folder. It reads only the deliverables in a fresh context (black-box
  verification — the article's recommended split) and returns a compact verdict. Check every finding against the
  files before changing anything; fix FAILs, decide RISKs, record both in `10_review.md`. Without subagents
  (Claude.ai, Cowork, ChatGPT): offer the user a verification pass in a **new chat** given only `02`-`05` and `08` —
  same fresh-eyes effect.
- **Subagents only on measured need.** Parallel per-scene assembly in fresh contexts is allowed only for long
  projects where a run has shown degradation from context size (e.g. many scenes, 40+ shots) — record the
  measurement in `10_review.md`. Do not split by department.

## Files and modes

- **Files:** with a filesystem, create a project folder (default `~/Desktop/film-crew/<project-slug>/`; if that is
  not writable, a `<project-slug>/` folder in the current directory — tell the user the exact path) and write one
  file per department using `references/templates.md`. Without one, deliver the same documents as sections of one
  document in the same order.
- **Mode:** default *full run* — all departments, then the review, then hand over. *Step mode* on request — stop
  after the Director (and after the Editor) for approval.

## The rule that makes clips cut together

Every cut gets a **handoff contract** written by the Editor (`references/editing-grammar.md`) before any shot is
designed:

```
CUT 3→4 | type: match on action | A ends: <exact last frame> | B starts: <exact first frame>
axis: camera stays on side X of the A–B line | screen direction: L→R kept | eyeline: B looks frame-left
size change: MS → CU (≥ 2 steps) or angle ≥ 30° | light: key from frame-left, warm, same | props/wardrobe: <states>
motion: <vector carried across the cut> | sound: <J-cut / L-cut / bridge> | generation: <same call / first-frame chain / extend / bridge>
```

The Camera Operator then designs each shot to **end** in the contract's A-frame and **start** in the B-frame. The
Assembly turns each frame into a keyframe prompt, and the generation plan picks how the cut is produced (see
`references/generation-strategy.md`).

## Step 8 — assembly (`08_storyboard.md`)

One card per shot (template in `references/templates.md`):

- shot number, scene, duration, size, angle, lens, move (from the shot list), purpose (from the director);
- **start keyframe prompt** (still image, English) and **end keyframe prompt** when the shot must land on an exact
  frame;
- **video prompt** in the target model's syntax (Seedance 2.5: asset declaration → one-line summary → timed plot →
  global supplement; time in plain seconds `[0-4s]`);
- locked continuity block (identity, wardrobe state, set, light direction, props) — the same words every time,
  **written out in full inside every prompt**. Prompts must be copy-ready: never leave placeholders such as
  "[paste LOOK: X verbatim]" — the user pastes prompts directly into the generator;
- handoff in and handoff out (copied from the edit plan);
- sound for this shot (from the sound plan).

## Step 9 — generation plan (`09_generation_plan.md`)

Group shots into generation units and choose a chaining method per cut: same multi-shot call, first-frame chain
(last frame of A → first frame of B), extension, bridge, or independent shot cut hard. List the generation order,
references to upload per unit (in upload order), and the QC check for each unit before moving on. Never claim a
video was generated; this skill plans. To generate, hand units to `fal-ai-media`, `higgsfield`, or Dreamina.

## Step 10 — table read (`10_review.md`)

Three layers, in this order:
1. **Self table read** — each department's checklist (end of each role file) against the assembled storyboard; the
   Editor runs the **virtual cut**: every contract against the two cards. Fix in place.
2. **Validator** — `scripts/validate_package.py`; fix every FAIL, judge every warning.
3. **Independent verifier** — `film-continuity-verifier` (Claude Code) or a fresh-chat pass elsewhere; verify each
   finding against the files, then fix.
Record results and changes in `10_review.md`. Do not hand over with an open FAIL.

## Hand-over to the user

1. 3-6 lines in the user's language: what the film is, lens, number of shots, total duration, how it will be
   generated.
2. The folder path (or the document) with all files.
3. The first generation unit, ready to paste.
4. Real risks only (e.g. dialogue language unsupported, a shot that depends on a hard physical action).

## Neighbours

Single prompt → `seedance-25-director` (Seedance 2.5) or `cinema-worldbuilder-pro-2.0` (other models). Stills for
keyframes in depth → `banana-pro-director-2.0`. Story development before a crew is needed → `shortfilm-prompt` or
the screenwriting skills. Maghakian brand content end-to-end → `content-zavod`, which may call this crew for its film
work.
