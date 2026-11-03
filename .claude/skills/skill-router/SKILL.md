---
name: skill-router
description: "Tigran's skill menu. Use FIRST, without being asked, whenever a task touches content, video, image/visual, design, SMM/Instagram, marketing, copy, pitching/sales, screenwriting, books or brand: show the matching skills from his collection, recommend one with a reason, then start working. Also use when he asks which skills he has: «ինչ սքիլներ ունեմ», «որ սքիլով», «какие скилы», «what skills do I have»."
---

# Skill router

Tigran has collected many skills and does not remember all of them. He does not want to name a skill
every time. Your job: notice the domain, show him what he owns for it, recommend, and get to work.

## How to run it

1. **Spot the domain** from the request (table below). A task can hit two domains (e.g. a reel = video + SMM).
2. **Show a short menu** at the top of your reply, in Tigran's language (usually Armenian):
   - 2–5 skills that fit THIS task, one line each: what it is good for here, and a weakness if it matters.
   - **Recommendation** with the reason in one sentence ("խորհուրդ եմ տալիս X, որովհետև …").
   - Skills that fit poorly: leave them out. Do not dump the whole table.
3. **Then act:**
   - If the recommendation is clear → start working with it right away. Tigran can switch with one word.
   - If two skills would give really different results (e.g. Armenian brand voice vs. a viral English hook) →
     ask with AskUserQuestion, recommended option first, then continue with the answer.
4. **Chain** skills when needed and say the order in one line (e.g. film-crew → seedance-25-director → humanizer).
5. **Fixed rules that override the menu:**
   - Any image or video prompt → `film-crew` first, then the model skill (CLAUDE.md rule, 2026-11-03).
   - Anything published in the studio's or Ani's name → `maghakian-brand` (look/voice) is always on.
   - Text Tigran will publish or send → finish with `anthropic-skills:humanizer` if it reads stiff.
6. If nothing in his collection fits, check `skill-library` (archive) and say so; only then work without a skill.

## The map

### Video
| Skill | Best for | Notes |
|---|---|---|
| `film-crew` | Any shot, scene, trailer, ad, music video. 7 departments, style lenses (Kubrick, Parajanov, Tarkovsky, The King…) | **Always first** for video/image prompts |
| `seedance-25-director` | Final Seedance 2.5 prompt + UI settings | Default video model for our work |
| `cinema-worldbuilder-pro-2.0` | Final prompt for Veo, Kling, Sora, other engines | Use when the model is not Seedance |
| `higgsfield` | Higgsfield platform: model/preset choice, Soul ID, Cinema Studio, credits | Platform questions, not prompt craft |
| `shortfilm-prompt` | 5-stage short films: transformation, emotional, combat | Narrower than film-crew; good for viral one-idea shorts |
| `jackvsai-fashion-campaign-prompt-framework` | Fashion/streetwear campaign videos | Only for clothing |
| `remotion-video-creation` | Motion graphics, captions, animated text in code | For titles, lyric/kinetic text, explainers |
| `fal-ai-media` | Actually generating images/video/voice via fal.ai | Needs FAL_KEY |
| archive: `video-editing`, `manim-video`, `videodb` | Editing pipelines, math animation | via `skill-library` |
| Higgsfield connector (Editorial Motion Graphics) | Explainer from a topic: script, VO, subtitles | Through the connector |

### Image / visual / design
| Skill | Best for | Notes |
|---|---|---|
| `film-crew` | Shapes every still (look, costume, light) | **Always first** |
| `banana-pro-director-2.0` | Photoreal stills: characters, outfit refs, character sheets, plates | Our default still-image prompt skill |
| `gpt-image-prompting` | Only when GPT image model is chosen; text in images, infographics, mockups | Best at readable text inside images |
| `anthropic-skills:poster-design` | Posters, key art | |
| `anthropic-skills:canvas-design` | Art-style PNG/PDF made in code | Not photoreal |
| `maghakian-brand` / `anthropic-skills:maghakian-brand` | Logo, colors, templates, sizes | Always on for studio visuals |
| Adobe Express, Figma, Canva connectors | Editable layouts, carousels, decks | When Tigran wants to edit it himself |
| archive: `visual-designer`, `design-system`, `image-enhancer`, `frontend-design` | | via `skill-library` |

### SMM / Instagram / content
| Skill | Best for | Notes |
|---|---|---|
| `content-zavod` | Full production line: post, carousel, reel, article, promo, with gates | Strongest for finished, publish-ready pieces |
| `mini-scenario` | Instagram series: format, episode scripts, calendar, season arc, KPI | For serial content |
| `anthropic-skills:ani-digital-marketing` | Studio/Ani posts, calendars, bios, press, IMDb, SEO | Knows the studio's facts and voice |
| `trend-scout` | What is trending worldwide now (formats, audio, AI tools) | Run before planning a content batch |
| `maghakian-brand` | Captions and visuals in the brand voice | |
| archive: `content-strategy`, `content-engine`, `crosspost`, `content-creator` | | via `skill-library` |

### Marketing / sales / copy / SEO
| Skill | Best for | Notes |
|---|---|---|
| `anthropic-skills:ani-digital-marketing` | Pitches, outreach to platforms/producers, website | First choice for selling scripts and productions |
| `director-desk` (treatment) | Pitch deck / treatment structure + gap audit + branded PDF | Use with ani-digital-marketing for the words |
| `copywriting` | Landing pages, headlines, CTAs, website copy | Conversion-focused |
| `seo-audit` | Site SEO problems (maghakianscripts.com) | |
| `llm-council` / Roast Room (`maghakian-roast-room/`) | Pressure-test a big decision, offer, price, pitch | Before sending something high-stakes |
| `anthropic-skills:humanizer` | Make any text sound human | Last step for anything published |
| archive: `market-research`, `brand-strategist`, `brand-voice`, `copy-editing`, `email-ops`, `lead-intelligence`, `seo` | | via `skill-library` |

### Writing / screenwriting / books
| Skill | Best for | Notes |
|---|---|---|
| `anthropic-skills:ani-screenwriting-workflow` | Loglines, synopses, bibles, outlines, scenes, children's stories 0–16 | Default for story work |
| `director-desk` | Script → industry PDF/DOCX/FDX (Fountain, hy/ru/en), breakdown in eighths + CSV, storyboard sheet PDF, treatment/pitch deck PDF, ShotDeck search lines | Replaces KIT Scenarist, Storyboarder, Canva treatments |
| `content-zavod` | Screenplay or article as a produced piece with gates | |
| `anthropic-skills:docx` / `pdf` / `docs` | Book files, layouts, documents to send | Format step |

### Research
| `agent-reach` | Web/social/video/GitHub lookups | `trend-scout` for trends, `perplexity`/`firecrawl` connectors for deep search |

## Menu format (example)

> **Սքիլներ այս գործի համար**
> - `film-crew` → կադրի պլան (պարտադիր առաջինը)
> - `seedance-25-director` → վերջնական պրոմպտ Seedance 2.5-ի համար
> - `cinema-worldbuilder-pro-2.0` → եթե Kling/Veo ես ուզում
>
> **Խորհուրդ՝** film-crew → seedance-25-director, որովհետև թրեյլերի մնացած կադրերը Seedance-ով են։ Սկսում եմ։

Keep the menu under ~8 lines. Then do the work.

## Keep the map current
When a skill is added, removed or renamed in `.claude/skills/` (or a new connector appears), update this map
in the same session and push, so both sides (VS Code and Cloud) see it.
