# Eval results, 2026-11-26: Tigran's skills, with vs without

> Tigran: vote in `blind.md` **before** reading this file.

## Setup
- **Tasks:** 15 real studio tasks, 3 each for seedance-25-director, film-crew, gpt-image-prompting, banana-pro-director-2.0 and cinema-worldbuilder-pro-2.0 (see `tasks.json`).
- **WITH:** the full workspace (CLAUDE.md + all skills).
- **WITHOUT:** the same model with skills disabled and no CLAUDE.md.
- **Both arms:** no web, no MCP, non-interactive, one run each.
- **Judge:** a blind model judge (same model family, so a possible bias) scored each pair on 4 criteria (1–5). Tigran's blind vote is the main verdict.

## Totals (model judge)

| | model_fit | craft | brief_fidelity | copy_ready | wins |
|---|---|---|---|---|---|
| WITH skills | **4.00** | **4.80** | 4.27 | **3.73** | **12** |
| WITHOUT | 3.07 | 3.80 | 4.20 | 3.20 | 3 |

**Cost and time per run:**
- WITH averages about $0.43 and 73 s.
- WITHOUT averages about $0.09 and 32 s.
- Full film-crew mode (F1, F2) took 4–5 min and about $1.2.

**Routing:** WITH used film-crew first in all 15 runs, then the right model skill. F1 used film-crew alone.

## Per task (winner by the judge, total score with / without)

| Task | Winner | With | Without |
|---|---|---|---|
| S1 | with | 17 | 14 |
| S2 | with | 17 | 13 |
| S3 | with | 17 | 12 |
| F1 | with | 17 | 13 |
| F2 | with | 17 | 11 |
| F3 | **without** | 13 | 17 |
| G1 | with | 18 | 16 |
| G2 | with | 18 | 14 |
| G3 | with | 19 | 13 |
| B1 | **without** | 14 | 16 |
| B2 | with | 19 | 12 |
| B3 | with (tie on points) | 16 | 16 |
| C1 | **without** | 15 | 17 |
| C2 | with | 18 | 17 |
| C3 | with | 17 | 13 |

## What the losses show (fix list)
1. **F3, children's poster.** banana-pro-director-2.0 turned two cartoon kids into photoreal children, left out the title and padded the prompt with "no CGI" negatives. It needs a stylized / illustration lane, or film-crew should route non-photoreal stills elsewhere.
2. **B1, character sheet.** The final prompt dropped the brief's facts (age 41, translator, 2026), mixed shallow-depth bokeh with an "evenly sharp seamless backdrop", and repeated skin text and internal "Mode" labels. Brief facts must reach the identity block, and internal labels stay out of the final prompt.
3. **C1, Kling.** cinema-worldbuilder lost the location name (Gyumri) and buried the prompt under settings and QA notes. Every noun from the brief must reach the final prompt, and notes go after it.
4. **General.** Skills win on model facts and craft but lose points on bloat (copy_ready). The final block should be the prompt plus settings only.
5. **Minor.** S3 (fixing a failed clip) also went through film-crew. By design, fixes go straight to seedance-25-director.

## Re-run after fixes (3 runs per arm, `out-v2/`, judge in `out-v2/judge.json`)

| Task | Before | After the fix (3 runs each) | Mean total with / without |
|---|---|---|---|
| B1, character sheet | lost | **with wins 3 of 3** | 16.7 / 12.7 |
| C1, Kling, Gyumri | lost | **with wins 3 of 3** | 18.0 / 17.3 |
| F3, children's poster | lost | without wins 3 of 3, but with scores higher on average | 17.7 / 17.0 |

**F3:**
- The style problem is fixed: the poster is now a storybook illustration, not photoreal kids.
- What is left is a policy choice. The skill leaves the Armenian title out of the image, as clean space for an overlay, because AI image models often break Armenian letters (the studio's glyph rule). The judge prefers rendering the title in the image.
- The judge also liked shaping each kid from the meaning of the names (Մտմտիկ = the thinker, Պրպտիկ = the digger). This is a small improvement to add.
- Decision for Tigran: overlay the Armenian title, or try rendering it with a fallback.
