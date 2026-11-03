---
name: bab-production
description: "BAB Production: a film/TV production board of the world's best department heads (simulated from their public work) with Tigran's own line-producer seat at the centre. Phase 1, the board debates a project or decision and gives a scored verdict (Roast Room machinery). Phase 2, each head runs its department with the studio's tools (film-crew, director-desk, pack, plan, banana-pro, seedance…). Use when Tigran says «BAB», «BAB Production», «բաբ», «խորհուրդ նախագծի համար», «քննարկեք նախագիծը», «ինչ կասեին լավագույնները», or brings a film/series project, script, budget or production decision to be judged and developed."
---

# BAB Production

A production company in a box: seven heads at the table, buyers on call, every head with a team of sub-agents.
Built on the Roast Room in `maghakian-roast-room/` (same rounds, scoring, live room, verdict). Seats are
simulations built from public work (quick-web brains, 7 to 20 sources each, refresh with `/newroaster` when the
cloud network allows the hosts). Tigran's seat is built from his own interview with his consent.

## The table

| Seat (key) | Head of | Owns the question | Team (sub-agents / tools) |
|---|---|---|---|
| **Tigran** (`tigran`) · centre | Line producing | Can we make this at this price, in these days, with these people, and where will the money leak? | second director's time plan, budget, prices, cost control: `director-desk` `plan.py master/day/report`, `production.py` (Կազմ, Ծախսեր, Գնացուցակ) |
| Rhimes (`rhimes`) | Showrunning, story | Will this story hold an audience across many episodes and seasons? | `ani-screenwriting-workflow`, `director-desk` proofreading, `pack.py` synopses, bible |
| Villeneuve (`villeneuve`) | Directing | What is this really about, and how should it feel? | `film-crew` director dept, scene overview |
| Blum (`blum`) | Producing | Can we make this cheaply and still sell it big? | `pack.py` one-pager, deck, `report finance` |
| Deakins (`deakins`) | Camera and light | What should this look like, and does every image serve the story? | `film-crew` DP + camera depts, storyboard sheet, image/video prompts (`banana-pro-director-2.0`, `seedance-25-director`) |
| Vermette (`vermette`) | Production design | Does this world feel real, and can we build it? | `film-crew` design + costume depts, `banana-pro-director-2.0` plates, props/costume sheets from `plan.py day` |
| Murch (`murch`) | Edit and post | Will this cut together, and what is the emotion of each cut? | `film-crew` editor + sound depts, `remotion-video-creation` titles |
| Buyers on call: Bloys (`bloys`, HBO premium), Quinn (`quinn`, NEON festivals), Bajaria (`bajaria`, Netflix local-to-global) | Selling | Would they buy it, and by which route? | `pack.py` 02 Platform, 07 International, 08 Competition |

Board: the seven above. Add one or two buyers when the question is about selling, financing or a platform
(max nine). The Roast Room industry seats (`buyer`, `copro`, `lineprod`, `showrunner`) can be added for
Armenian/CIS market reality.

## Phase 1: the board

1. Ask (AskUserQuestion, Armenian, one screen) only what is missing: the project or decision; the material
   (script, season master, budget, project.xlsx); buyers needed (none · Bloys · Quinn · Bajaria).
2. Work inside `maghakian-roast-room/` and follow `.claude/skills/roast-room/SKILL.md` with
   `--seats tigran,rhimes,villeneuve,blum,deakins,vermette,murch[,buyers]`. Read `business.md` first.
3. Chair rules on top of the Roast Room's:
   - **Tigran is the centre.** In every round he speaks last and prices every ask the other seats made
     (days, money, people, safety). An ask he cannot price stays open, not accepted.
   - Real numbers win: when a `project.xlsx` or `master.xlsx` exists, the board uses them (pages left,
     price list, costs so far). Never invent a price; label assumptions.
   - Safety is a veto: a risky scene without a safety plan cannot be approved.
   - Thin brains: seats say "no recorded position" instead of guessing; the Chair keeps quotes only with ids.
4. Verdict in Armenian in chat and `verdict.md` (verdict.json stays in English for the PDF), titled
   "BAB Production verdict".

## Phase 2: the departments

After the verdict ask (multi-select, "Բոլորը" first) which departments should start, then run each head's team
from the table above, in this order: story → director → design → camera → edit/sound → producing → line
producing (Tigran closes with days and money for everything the others produced). Rules that still apply:
every image or video prompt goes through `film-crew` first; documents for people go through the ask-first
menu (`director-desk/references/documents.md`); everything sent out uses the brand (`maghakian-brand`).

## Honest limits
- Seats are simulations, not the people. Never present their words as real unless quoted with a source id.
- Brains are quick-web (search excerpts). Say so when a decision is big.
- Tigran's seat never commits money or speaks for Tigran.
- Bajaria's current role at Netflix is uncertain (Oct 2026 reports); the seat models her public statements only.
