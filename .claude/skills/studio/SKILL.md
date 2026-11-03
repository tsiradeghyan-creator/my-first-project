---
name: studio
description: "One entry point to the whole Maghakian production toolkit: from idea and script to shooting days, money, AI film and release. Asks which track (script & documents · live-action production · AI film · pitch & promotion), shows the stages of that track with the skill that does each one, and starts at the stage Tigran is at. Use when he says «ստուդիա», «սկսենք նախագիծ», «նոր նախագիծ», «որտեղից սկսեմ», «ամբողջ շղթան», «студия», «новый проект», «start a project», or names a project without saying which tool."
---

# Studio: one door to everything

Tigran has many skills; this one only routes. It never re-does what a skill below already does.

**Judging or developing a whole project with the world's best heads:** `bab-production` (board of seven
heads with Tigran's line-producer seat at the centre, then each head runs its department).

## 1. Ask (AskUserQuestion, Armenian, one screen)
**Q1. Ո՞ր ուղղությունն է** (one choice):
- **Սցենար և փաստաթղթեր** · գաղափարից մինչև սցենար և ամբողջ փաստաթղթային փաթեթ
- **Իրական նկարահանում** · սեզոնի պլան, օրվա ռազբիվկա, մարդիկ, ծախսեր, հաշվետվություններ
- **AI ֆիլմ** · ռասկադրովկա, կադրեր, շարժում, ձայն, մոնտաժ AI-ով
- **Պիչ և առաջխաղացում** · պլատֆորմ, ֆոնդ, Instagram, մամուլ

**Q2. Ո՞ր քայլում ես հիմա** (show that track's stages from section 2 as options; "Սկզբից" first).
If he already said what he needs, skip the questions and go straight to the stage.

Then: say in one line which skill runs this stage and which comes next, and start.
Before making documents for someone, `director-desk` asks who they are for (`references/documents.md`).

## 2. Tracks and stages

### A. Սցենար և փաստաթղթեր
| # | Stage | Skill / command |
|---|---|---|
| 1 | Գաղափար, լոգլայն, կառուցվածք | `anthropic-skills:ani-screenwriting-workflow` |
| 2 | Սցենար (գրել, վերանայել) | `anthropic-skills:ani-screenwriting-workflow` |
| 3 | Ֆորմատ (PDF/Word/Final Draft), KIT ներմուծում | `director-desk` §1 (`screenplay.py`, `kit_docx_to_fountain.py`) |
| 4 | Սրբագրում | `director-desk` §1b (`proofread.py`) |
| 5 | Փաթեթ ըստ ստացողների | `director-desk` §4b (`pack.py`) |

### B. Իրական նկարահանում
| # | Stage | Skill / command |
|---|---|---|
| 1 | Սեզոնի գլխավոր ցուցակ (ձեր Excel-ից) | `director-desk` §4c `plan.py master` |
| 2 | Կազմ, դրույքներ | `plan.py init project.xlsx` |
| 3 | Օրվա ռազբիվկա + օրվա տեքստեր | `plan.py day … --project` |
| 4 | Ծախսեր, չեկեր | `plan.py expense` |
| 5 | Հաշվետվություններ (ծախս, վճարներ, ընթացք) | `plan.py report finance|payroll|progress` |
| 6 | Casting, sides | `pack.py` (05, 06) |

### C. AI ֆիլմ (rule: every image/video prompt goes through `film-crew` first)
| # | Stage | Skill |
|---|---|---|
| 1 | Գաղափար և սցենար | `ani-screenwriting-workflow` or `shortfilm-prompt` (one-idea shorts) |
| 2 | Ռասկադրովկա և ոճ | `film-crew` (director + style lens) → `director-desk` §3 storyboard sheet |
| 3 | Հերոս և աշխարհ | `film-crew` (production + costume) → `banana-pro-director-2.0` (character sheets, plates) |
| 4 | Կադրեր և լույս | `film-crew` (DP) → `banana-pro-director-2.0` |
| 5 | Շարժում | `film-crew` (camera) → `seedance-25-director` (Seedance) or `cinema-worldbuilder-pro-2.0` (Veo, Kling…); platform: `higgsfield` |
| 6 | Ձայն և մոնտաժ | `film-crew` (sound, editor); titles/captions `remotion-video-creation` |
| 7 | Պրեմիերա և վերլուծություն | **not built yet**: plan by hand with `anthropic-skills:ani-digital-marketing`; say so |

### D. Պիչ և առաջխաղացում
| # | Stage | Skill |
|---|---|---|
| 1 | Pitch deck, treatment, bible | `director-desk` §4 / §4b |
| 2 | Նամակներ պլատֆորմներին, պրոդյուսերներին | `anthropic-skills:ani-digital-marketing` |
| 3 | Instagram, պոստեր, ռիլս | `content-zavod`, `mini-scenario`, `trend-scout` |
| 4 | Ստուգել մեծ որոշումը (գին, առաջարկ) | `llm-council` / Roast Room |
| 5 | Վերջին տեքստ | `anthropic-skills:humanizer` |

Brand rules (`maghakian-brand`) are on for everything that leaves the studio.

## 3. Keep it honest
- A stage marked "not built yet" stays that way until Tigran asks to build it; do not improvise a fake tool.
- When a skill is added or renamed, update this table and `skill-router` in the same session and push.
