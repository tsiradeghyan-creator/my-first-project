---
name: bab-production
description: "BAB Production: a film/TV production board of the world's best department heads (simulated from their public work) plus Tigran's own line-producer seat. Phase 1, the board runs the original Roast Room council on a project decision, unchanged (board pick, brief, three rounds, draft resolution, ratification, quote check, scored verdict). Phase 2, each head runs its department with the studio's tools (film-crew, director-desk, pack, plan, banana-pro, seedance…). Mode 2 carries a project from idea to screen through gates, each gate being one Roast Room council. Use when Tigran says «BAB», «BAB Production», «բաբ», «խորհուրդ նախագծի համար», «քննարկեք նախագիծը», «ինչ կասեին լավագույնները», or brings a film/series project, script, budget or production decision to be judged and developed."
---

# BAB Production

BAB is a set of seats plus a department layer on top of the Roast Room in `maghakian-roast-room/`. The council itself is the Roast Room's, used exactly as it ships, with no rules added, removed or reordered. That repo is tested and works; BAB does not change how it decides.

**Rule (Tigran, 2026-11-04).** Every BAB council runs `maghakian-roast-room/.claude/skills/roast-room/SKILL.md` step by step, with its own files in `maghakian-roast-room/.claude/skills/roast-room/references/`: `round-prompts.md`, `scoring.md`, `report-template.md`, `live-room.md` and `seats.md`. Every BAB seat is built the way `/newroaster` builds a seat. Where this file and the Roast Room disagree, the Roast Room wins.

## The seats

| Seat (key) | Pillar | Owns the question | Department tools (phase 2 only) |
|---|---|---|---|
| Tigran (`tigran`) | Line producing | Can we make this at this price, in these days, with these people, and where will the money leak? | `director-desk` `plan.py master/day/report`, `production.py` (Կազմ, Ծախսեր, Գնացուցակ) |
| Rhimes (`rhimes`) | Showrunning, story | Will this story hold an audience? | `ani-screenwriting-workflow`, `director-desk` proofreading, `pack.py` synopses, bible |
| Villeneuve (`villeneuve`) | Directing | What is this really about, and how should it feel? | `film-crew` director dept |
| Blum (`blum`) | Producing | Can we make this cheaply and still sell it big? | `pack.py` one-pager, deck, `report finance` |
| Deakins (`deakins`) | Camera and light | What should this look like, and does every image serve the story? | `film-crew` DP + camera depts, `banana-pro-director-2.0`, `seedance-25-director` |
| Vermette (`vermette`) | Production design | Does this world feel real, and can we build it? | `film-crew` design + costume depts, `banana-pro-director-2.0` plates, props/costume sheets |
| Murch (`murch`) | Edit and post | Will this cut together, and what is the emotion of each cut? | `film-crew` editor + sound depts, `remotion-video-creation` |
| Bloys (`bloys`), Quinn (`quinn`), Bajaria (`bajaria`) | Buying | Would they buy it, and by which route? | `pack.py` 02 Platform, 07 International, 08 Competition |
| Levi (`levi`) | Selling formats from a small market | Can this story travel as a format, and how do we sell it? | `pack.py` 07 International, bible |
| Mungiu (`mungiu`) | Low-budget auteur cinema, co-production | Can we make this small, true and finished, with European money? | `pack.py` 08 Competition and fund applications, `plan.py` |
| Line Producer (`lineprod`) | Industry line-producing practice (composite) | What do the best production companies do here? | `director-desk` breakdown, `plan.py` |

They are ordinary Roast Room seats in `roster.json`. Tigran's seat has no special powers: it speaks in the same rounds as everyone, in parallel, and its weight comes from `seats.md` like any seat's. For a money, days or production call it usually gets a 3, and it is the downside seat the board recommendation asks for.

## Phase 1: the council

1. Work inside `maghakian-roast-room/`. Read its `CLAUDE.md` and `business.md`.
2. Run `/roast-room` on the decision, exactly as its SKILL.md says:
   - **Pick the board.** Recommend from the BAB seats above (and any other roster seat whose pillar the decision touches), then confirm with Tigran in one AskUserQuestion. Five to seven seats for a full council, four for `--quick`, never more than nine.
   - **Step 1, the brief.** Under 300 words. Options as A, B, C, always including "don't do it" or "keep doing what we do now". Real numbers come from `business.md`, `project.xlsx` and `master.xlsx` when they exist; assumptions are marked.
   - **Step 2.** Set the weights per `seats.md` BEFORE Round 1, and write `brief.md` and `council.json`.
   - **Steps 3 to 6.** Round 1, Round 2, `draft-resolution.md`, Round 3 ratification.
     - Use the prompts in `round-prompts.md` word for word, so the cards carry every field: stance, option scores, pillar score, confidence, ruin risk, door, moved.
     - Write the cards, Chair notes and live-room files as each round lands.
   - **Step 7.** Run `check_quotes.py`. The script only sees quotes in "…" marks, so also check by hand every quote in «…» marks against that seat's brain (the Step 7 fallback). Then score per `scoring.md` with its overrides (ruin cap, one-way door, unanimity), write `verdict.md` from `report-template.md` and `verdict.json`, and give the short chat verdict.
3. Language follows `maghakian-roast-room/CLAUDE.md`. Tigran writes in Armenian, so the cards and the verdict are in Armenian, the field labels and JSON keys stay in English, and `verdict.json` text is in English.
4. Mode: full for anything hard to undo; `--quick` only for reversible calls, as the Roast Room says.

## Phase 2: the departments

After a verdict, ask (multi-select, «Բոլորը» first) which departments should start, then run each head's tools from the table above. Phase 2 is work, not a council: no scoring, no verdict.

Rules that still apply:
- every image or video prompt goes through `film-crew` first;
- documents for people go through the ask-first menu (`director-desk/references/documents.md`);
- everything sent out uses the brand (`maghakian-brand`).

## Mode 2: from zero (idea to screen)

The board builds a project from the idea, stage by stage.
- **Gates.** Each stage ends at a gate. The gate is one `/roast-room` council run as in Phase 1, and Tigran decides: go, change or kill. Nothing moves on without his yes.
- **Authorship.** Ani is the writer of record. The board proposes and critiques; the pages are hers.

**Where state lives.** In `projects/<slug>/`, committed: `00_seed.md` · `01_ideas.md` · `02_concept.md` · `03_story.md` · `04_pilot/` · `05_package/` · `06_preprod/` · `gates.md`. `gates.md` records every gate: date, scores, Tigran's decision and why. Read `gates.md` first in every session.

**How each stage uses the Roast Room, unchanged:**

- **Making material** (ideas, concept, story, pilot, package) is not a council.
  - For ideas: the Roast Room's own single-seat consult, `/roast-room ask <seat>`, with its consult prompt. Rhimes, Villeneuve and Blum each pitch two original ideas, in separate consults.
  - For concept, story, pilot and package: Phase 2 departments.
- **Deciding** is a council at the gate.
  - The material becomes the options A, B, C…, plus "none of these: go back a stage" or "kill".
  - The council runs all three rounds and the ratification.

| Stage | Material made by | Gate council decides |
|---|---|---|
| 0 Seed | Tigran (format, audience, language, budget range, buyer, deadline) | no council: Tigran confirms the brief |
| 1 Ideas | consults: Rhimes, Villeneuve, Blum (2 ideas each) | which idea we develop (options = the ideas + none) |
| 2 Concept | departments: story (Rhimes), director (Villeneuve), producing (Blum), edit (Murch), line producing (Tigran) | is this concept worth a treatment and script (develop / change / kill) |
| 3 Story | Rhimes with Ani: treatment or bible, outlines | does the story hold (go / revise / kill) |
| 4 Script or pilot | Ani writes; notes from Rhimes, Villeneuve, Murch as consults | ready to sell or shoot (go / revise / kill) |
| 5 Package | Blum and the buyers: deck, one-pager, mock pitches as consults | sell, fund, or produce ourselves |
| 6 Pre-production | Villeneuve, Deakins, Vermette, Tigran departments (`film-crew` first) | green light (go / wait / kill) |
| 7 Production and post | departments, plus a council for any big weekly decision | per decision |

Rules for this mode:
- Ideas are original: no remakes, no borrowed IP. Comps are for positioning only.
- Every gate verdict goes into `gates.md`, with Tigran's decision in his words.
- Killing early is a good outcome.

## Brains: built exactly like the original seats

A BAB seat's knowledge must be built the way `/newroaster` builds every seat:
- WebSearch for sources, then `fetch.mjs` into a corpus;
- parallel extraction agents, then `check_quotes.mjs`;
- three writer agents, then `_hot.md`;
- the agent file, a test consult and a portrait.

Depth: standard (30 to 50 sources, 250k+ words) at least; `--deep` (80+ sources) where the person's public work allows, to match the original seven.

**State on 2026-11-26, after the rebuild** (brain words; every quote passes `check_quotes.mjs` with 0 errors):

| Seat | Sources | Brain words | Note |
|---|---|---|---|
| Villeneuve | 126 | 22,247 | |
| Murch | 94 | 20,565 | 2020–2026 video talks unreachable (YouTube), no AI position |
| Rhimes | 113 | 16,722 | |
| Deakins | 95 | 13,943 | |
| Bloys | 129 | 13,406 | corpus 132k words: no books, podcasts paywalled |
| Quinn | 79 | 12,559 | corpus 124k words: same reason |
| Mungiu (new) | 101 | 12,499 | Low-budget auteur cinema and co-production; on call |
| Blum | 97 | 12,010 | |
| Bajaria | 81 | 10,501 | Netflix 2016–2026 philosophy; corpus 90k words |
| Line Producer (composite) | 66 | 10,385 | industry practice, Armenia rebate decision 412-N |
| Levi (new) | 32 | 9,349 | Selling formats from a small market; on call; thin English record, corpus 51k words |
| Tigran | 7 | 4,206 | grows from his own material, see `sources/tigran/HOW-TO-FEED.md` |
| Vermette | | 2,040 | kept light on purpose (Tigran, 2026-11-26) |

Seats with a corpus under 250k words are thinner on recent views; the Chair says so when such a seat decides a crux. Default board: Rhimes, Villeneuve, Blum, Murch, Bloys, Tigran. Villeneuve against Mungiu is the intended big-film vs small-film tension.

**BAB Room page** (https://claude.ai/artifact/ViA4NX26TzgBE6gKhiAvtW, source `maghakian-roast-room/bab-room/`). Tigran types the decision, picks 4–9 seats, and watches the Chair, R1, R2 and R3 stream live, then gets the scored verdict. Councils are saved in the page's db. After any brain changes: `python3 maghakian-roast-room/bab-room/build_data.py`, then republish `data/seats.json` and `data/context.json` with publish_files (patch mode).
- **Where to rebuild.** From the cloud (cloud-only since 2026-11-26): fetching works with
  `NODE_USE_ENV_PROXY=1 node .claude/skills/newroaster/scripts/fetch.mjs build/<slug> --list sources/<slug>/urls.txt`.
  YouTube refuses cloud IPs, so talks need transcript pages instead. Use `/newroaster <name>` in refresh mode on the same
  slug, from step 3 onward. The corpus stays in `build/` (gitignored).
- **Tigran's seat.** It is built from his own material (`fetch.mjs --add`, with his consent). It needs more of his material (interviews, notes, voice-note transcripts) to reach the newroaster minimum of about 15 sources or 60,000 words.

## Honest limits
- Seats are simulations, not the people. Never present their words as real unless quoted verbatim with a source id.
- Tigran's seat never commits money or speaks for Tigran.
- The Bajaria seat models how Netflix bought and scheduled under her (2016–2026). She left Netflix in October 2026, and Peter Rice became Chief Content Officer. The seat speaks for that buying philosophy, not for Netflix today.
- The bab-feature-01 Gate 1 debate (rounds D1 and D2) and the stage 2 concept round of 2026-11-03 ran before this rule, with a custom procedure. They had no Round 3 ratification, the cards had no confidence, ruin-risk or door fields, and weights were set after the scores. Treat those results as provisional until a standard council confirms them.
