---
name: maghakian-brand
description: Brand guidelines for Maghakian Script Writing Agency (founder Ani Maghakyan). Use when creating any content, copy, visuals, captions, hashtags, or social media assets for the agency in Armenian, English, or Russian — Instagram/Telegram/Facebook/LinkedIn posts, brand colors, typography (incl. Armenian fonts), tone of voice, posting cadence, or content strategy.
metadata:
  version: 1.2.0
---

# Maghakian Script Writing Agency — Brand Guidelines

## About This Skill

Use this skill when creating any content, copy, visuals, or social media assets for **Maghakian Script Writing Agency** (founder: Ani Maghakyan). These guidelines ensure all output is on-brand across languages and platforms.

---

## Brand Identity

**Full Name:** Maghakian Script Writing Agency
**Founder/Screenwriter:** Ani Maghakyan
**Languages:** Armenian (primary), English, Russian
**Core Offering:** Professional screenwriting, TV series, film scripts, branded storytelling

---

## Portfolio (Filmography)

Ani Maghakyan's full body of work — **46 projects, 2,200+ episodes, ≈ 80,000 pages of script, 2017–2026** — is in **[`portfolio.md`](portfolio.md)** (project list, year, episode counts, page estimates, totals, and approved post phrasings).

**Always read `portfolio.md` before** writing anything about her credentials, achievements, scope of work, or a specific project — and never represent a single show (e.g. «84-ի ամառը») as the whole career. Use the aggregate numbers instead.

---

## Brand Colors

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | Maghakian Purple | `#6450D2` | CTAs, headings, accent elements, logo background |
| Base | Deep Black | `#0D0D0D` | Backgrounds, body text on light surfaces |
| Surface | Off-White | `#FAFAFA` | Backgrounds, text on dark surfaces, breathing space |

### Color Pairing Rules
- **Purple on Black** — primary dark-mode combination (hero sections, covers, story frames)
- **Purple on White** — primary light-mode combination (documents, LinkedIn, editorial)
- **White on Black** — clean contrast for text-heavy layouts
- **Never** use purple text on white background at small sizes (contrast drops below WCAG AA)
- **Never** use pure `#FFFFFF` — always use `#FAFAFA` for warmth

---

## Logo

### Components
1. **Icon** — Cursive calligraphic "M" mark; elegant, handwritten character; functions as standalone symbol
2. **Wordmark** — "Maghakian" in bold italic serif; authoritative yet personal
3. **Tagline lockup** — "SCRIPT WRITING AGENCY" in spaced uppercase sans-serif beneath the wordmark; smaller scale

### Logo Lockup Hierarchy
```
  𝑀  (cursive icon)
  Maghakian  (bold italic wordmark)
  SCRIPT WRITING AGENCY  (tagline, tracked uppercase)
```

### Logo Usage Rules
- **Full lockup** — preferred for all primary placements (profile photos, headers, documents)
- **Icon only** — acceptable for small placements (favicon, watermark, story sticker)
- **Wordmark only** — acceptable for horizontal layouts where the icon doesn't fit
- Maintain clear space equal to the height of the "M" icon on all sides
- Never stretch, rotate, recolor, or add drop shadows to the logo
- On purple backgrounds: use white logo
- On white/light backgrounds: use black or purple logo

---

## Typography

### Primary Typeface — Headings
- **Style:** Bold italic serif (matches wordmark energy — think Playfair Display Italic Bold, or similar)
- **Use for:** Headlines, poster titles, series names, pull quotes
- **Feel:** Cinematic, literary, prestigious

### Secondary Typeface — Body / UI
- **Style:** Clean sans-serif (think Inter, Helvetica Neue, or Montserrat)
- **Use for:** Captions, descriptions, hashtags, UI labels, subtitles
- **Feel:** Modern, readable, professional

### Tagline / Label Typeface
- **Style:** Uppercase, wide letter-spacing (tracking: +200 to +300), light or regular weight
- **Use for:** "SCRIPT WRITING AGENCY" tagline, section labels, platform handles
- **Feel:** Editorial, structured, calm

### Type Scale (Social Media)
| Element | Size guidance |
|---------|--------------|
| Series/project title | Large, dominant — 60–80% of frame width |
| Screenwriter credit | Medium — clean, secondary |
| Tagline / platform label | Small, tracked uppercase |
| Caption body text | Legible at mobile screen size — 14–16sp equivalent |

---

### Typography — Armenian Fonts

Maghakian-ի բոլոր հայկական տեքստերը պետք է օգտագործեն հետևյալ շրիֆտները՝ ըստ կիրառման համատեքստի։ Բոլոր ընտրությունները համաձայնեցված են brand-ի `#6450D2` purple-ի հետ։

| Use Case | Շրիֆտ | Նկատառություններ |
|---|---|---|
| **Social media** | Mardoto, Noto Sans Armenian | Clean, modern — հիանալի readable է purple-ի վրա |
| **Editorial / magazine** | GHEA Mariam (body) + GHEA Aragast (display) | Cinematic, literary — համապատասխանում է brand-ի ոճին |
| **Branding / logo** | GHEA Grapalat | Geometric, scalable — purple վերնագրերի համար |
| **Long-form content** | Noto Serif Armenian | Elegant serif — մուգ ֆոնի վրա `#FAFAFA` գույնով |

#### Գույնային Կանոններ Armenian Type-ի Համար

- **Purple on Black** (`#6450D2` on `#0D0D0D`) — headings, series titles — Mardoto Bold
- **White on Purple** (`#FAFAFA` on `#6450D2`) — pull quotes, CTA buttons — GHEA Grapalat
- **White on Black** (`#FAFAFA` on `#0D0D0D`) — body text, captions — Noto Sans Armenian Regular
- **Purple accent** — screenwriter credit "Ani Maghakyan" — `#6450D2`, Noto Sans Armenian SemiBold

#### Google Fonts Import

```css
/* Maghakian — Armenian Web Fonts */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Armenian:wght@400;600;700&family=Noto+Serif+Armenian:wght@400;700&family=Mardoto:wght@400;700&display=swap');

:root {
  --color-purple: #6450D2;
  --color-black:  #0D0D0D;
  --color-white:  #FAFAFA;

  --font-display: 'Mardoto', 'Noto Sans Armenian', sans-serif;
  --font-body:    'Noto Sans Armenian', sans-serif;
  --font-serif:   'Noto Serif Armenian', serif;
}

/* Social media headings */
.heading-am {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--color-purple);
}

/* Editorial body */
.body-am {
  font-family: var(--font-serif);
  font-weight: 400;
  color: var(--color-white);
}

/* Long-form content */
.longform-am {
  font-family: var(--font-serif);
  line-height: 1.75;
  color: var(--color-white);
}
```

---

## Tone of Voice

### Brand Personality
Maghakian is **literary, warm, and confident** — the voice of a storyteller who has earned their seat at the table. Never boastful, never cold. Cinematic without being pretentious. Accessible without being casual.

### Tone Pillars
| Pillar | Means | Avoid |
|--------|-------|-------|
| **Cinematic** | Evokes feeling, imagery, scene | Purple prose, clichés |
| **Warm** | Personal, human, inviting | Overly formal or stiff |
| **Confident** | Assured, direct, no hedging | Arrogant, self-promotional |
| **Nostalgic** | Connects past to present | Sentimental or saccharine |
| **Precise** | Specific details over vague claims | Generic marketing language |

---

### Armenian (Հայերեն) — Primary Voice

- Warm, literary Eastern Armenian
- Use classical cadence when appropriate (for drama/series content)
- Avoid slang; prefer timeless phrasing
- Screenwriting/project announcements: poetic, scene-setting openings
- Direct CTAs: clear and active ("Դիտեք", "Կիսվեք", "Հետևեք")

**Sample phrase patterns:**
- Opening: *"Կային պահեր, որ ամբողջ կյանք էին..."*
- Announcement: *"Ani Maghakyan-ի նոր [ստեղծագործությունը] — [բնութագիր]"*
- CTA: *"Պրեմիերան [ժամկետ]։ Մի բաց թողեք։"*

---

### English — Secondary Voice

- Sophisticated but accessible
- Avoid corporate jargon ("synergy," "leverage," "innovative")
- Diaspora-aware: speaks to Armenian communities globally
- Industry-aware: film/TV professionals understand craft references

**Sample phrase patterns:**
- Opening: *"Some summers stay with you."*
- Announcement: *"[Series name] — a new [genre] by screenwriter Ani Maghakyan."*
- CTA: *"Premiering this [timeframe]. Don't miss it."*

---

### Russian (Русский) — Tertiary Voice

- Formal-warm register (not overly casual)
- Literary Russian — clean, without colloquialisms
- Appropriate for CIS Armenian diaspora audiences

**Sample phrase patterns:**
- Opening: *"Есть лето, которое не забывается."*
- Announcement: *"Новый [жанр] Ани Магакян — [название]."*
- CTA: *"Премьера [срок]. Не пропустите."*

---

## Social Media Visual Templates

### Universal Rules (All Platforms)
- Always use brand colors: `#6450D2`, `#0D0D0D`, `#FAFAFA`
- Logo or wordmark present on every asset
- No busy stock photography — prefer cinematic stills, textured gradients, or clean typography-forward layouts
- Text must be legible at thumbnail size
- Minimum logo clear space maintained at all sizes

---

### Instagram

**Profile:**
- Profile photo: Cursive M icon on `#6450D2` purple background
- Bio language: Armenian primary, English secondary
- Link: single link to latest project or agency site

**Feed Post Templates:**

*Type A — Series Announcement (Portrait 4:5 or Square 1:1)*
```
Background: #0D0D0D
Accent bar: #6450D2 (left edge or bottom strip)
Series title: Bold italic serif, #FAFAFA, large
Screenwriter credit: "Ani Maghakyan" — smaller, #6450D2 or #FAFAFA
Tagline/platform: tracked uppercase, #FAFAFA at 60% opacity
Logo: bottom-right corner, white version
```

*Type B — Quote / Pull Quote (Square 1:1)*
```
Background: #6450D2
Quote text: Bold italic serif, #FAFAFA, centered
Attribution: "— Ani Maghakyan" tracked, #FAFAFA at 70%
Logo: bottom-center, white version
```

*Type C — Behind the Scenes / Process (Landscape 1.91:1)*
```
Photo with #0D0D0D overlay at 50%
Caption overlay: #FAFAFA text, bottom-left aligned
Logo: top-right, white version
```

**Instagram Stories (9:16):**
```
Background: #0D0D0D or #6450D2
Central element: title or quote in bold italic serif
Bottom strip: #6450D2 or #FAFAFA bar with CTA text
Logo: top-left, appropriately colored version
Safe zone: keep all text within center 80% of frame
```

**Caption Structure:**
1. Hook (first line — before "more" cutoff, max ~125 chars)
2. Story/context (2–4 lines)
3. CTA (one clear action)
4. Line break
5. Hashtags (10–15, mix of Armenian-script and Latin-script)

**Hashtag Strategy:**
- Brand: `#MaghakianSWA` `#AniMaghakyan`
- Content-specific: series name in Armenian script
- Reach: `#ՀայկականՍերիալ` `#ArmenianSeries` `#HayFilm` `#Screenwriting`

---

### Telegram

**Channel identity:**
- Channel name: Maghakian / Maghakian SWA
- Profile photo: same as Instagram (cursive M on purple)
- Description: Armenian primary, concise

**Post Templates:**

*Announcement Post:*
```
🎬 [Series/project name in bold]

[2–3 sentence description — warm, cinematic tone]

📺 [Platform] | [Date/time]

#84իԱմառը #AniMaghakyan
```

*Short Update:*
```
[One punchy line]

[1–2 lines of context]

👉 [CTA with link]
```

- Telegram allows longer text — use it for deeper storytelling when announcing new projects
- Pin the most important announcement post
- Use Telegram polls for audience engagement ("Which era would you want a series about?")

---

### Facebook

**Page setup:**
- Cover photo: Full-width series key art or brand graphic (820×312px)
- Profile: Cursive M icon on purple
- About: Armenian + English description

**Post Templates:**

*Long-form Announcement (Facebook favors native long text):*
```
[Cinematic opening line]

[3–5 sentences: context, story premise, emotional hook]

[Screenwriter credit: "Written by Ani Maghakyan"]

[CTA: Watch / Share / Comment]

[Link in post body or first comment]

#ArmenianSeries #AniMaghakyan #[SeriesName]
```

*Video Post:*
- Thumbnail: matches feed post Type A template
- First 3 seconds: series title on black — no silence
- Captions/subtitles always on (most Facebook video is watched muted)

**Tone on Facebook:** Slightly warmer and more narrative than Instagram — audiences here read more. Use the space.

---

### LinkedIn

**Profile / Page:**
- Focus: professional screenwriting credentials, industry recognition, agency services
- Language: English primary, Armenian secondary
- Cover: horizontal brand graphic — wordmark on `#6450D2` purple or `#0D0D0D` black

**Post Templates:**

*Professional Announcement:*
```
[Confident, direct opening — one sentence]

[2–3 sentences: project details, professional context, craft angle]

[1 sentence: what this means for the industry or audience]

[CTA: Link, DM for collaboration inquiries]

#Screenwriting #ArmenianFilm #TVSeries #ScriptWriting #FilmIndustry
```

*Thought Leadership (craft/industry insight):*
```
[Observation or insight about screenwriting/Armenian TV/storytelling]

[Brief personal context — "In writing [series name]..."]

[Takeaway or question for the audience]

#Screenwriting #Storytelling #TVDevelopment
```

**Tone on LinkedIn:** Most professional of all platforms. Lead with craft and credentials. Still warm — not corporate. Ani Maghakyan is a creative professional, not a brand manager.

---

## Project Spotlight Carousels — Template, Rules & Performance Learnings

The recurring "Project Spotlight" carousel (one per project from `portfolio.md`) is the proven content engine. Treat this section as the spec.

### Slide structure (7 slides — depth matters)

7-slide carousels meaningfully outperform 4-slide ones (more time-on-post → more reach). Use this order:

1. **Poster / title** — official key art or a cinematic composite; large gold-or-brand display title; one-line tagline (the show's emotional hook); **add a small line "Սցենարիստ՝ Անի Մաղաքյան"**; logo.
2. **Scale + credits** — big display number ("24 ՄԱՍ" / "421 ՍԵՐԻԱ"); then `Սցենարի հեղինակ — Անի Մաղաքյան` (always first), `Ռեժիսոր — …`, `Հեռարձակում — …`, `Թողարկման տարեթիվ — YYYY`.
3–4. **Quote slides** — literary, cinematic lines in the show's voice (e.g. *«Երբ կյանքը խլում է ամեն ինչ — մնում է մեկ բան․ ԵՐԱԶԱՆՔԸ»*). Light serif body + accent colour for the key word.
5. **Logline + setting** — location label + the protagonist's dream/conflict in 1–2 sentences.
6. **Cast** — `ԴԵՐԱՍԱՆՆԵՐ` + actor names (verify spelling against the show's titres).
7. **Closing CTA** — where to watch (e.g. "Shant TV YouTube ալիքում") + "Հետևեք @maghakianscripts-ին" + Armenian action row **«Հավանիր · Պահպանիր · Տարածիր»** + logo.

### Palette decision (resolves the "always use brand colors" tension)

- **Project Spotlight posts** may use a **per-project cinematic palette** that fits the show's world (e.g. gold/sepia/black for a 1990s Gyumri period drama). Brand purple `#6450D2` would look wrong on a period piece — don't force it.
- **Agency-level content** (profile photo, bio graphics, non-project posts, craft/personal-voice posts, LinkedIn) **must** use brand colours `#6450D2` / `#0D0D0D` / `#FAFAFA`.
- On every spotlight slide keep the **MAGHAKIAN SCRIPTS logo / cursive-M monogram** visible — that's what carries brand identity when the palette varies.
- The **agency Latin wordmark stays elegant serif**; the Armenian display type should be a refined literary face (GHEA Aragast / GHEA Grapalat / Mardoto), **not** a heavy generic condensed font.

### Pre-publish checklist (every post)

- [ ] No unfilled template placeholders — search every slide for `[ ]`, `[YYYY]`, `xxx`, lorem-style stand-ins.
- [ ] Armenian proofread — every word in correct Eastern Armenian Unicode, no transliteration; common slips: `Զգացմունք` (not `Չգացմունք`), `Ինչու` (not `Իչու`), no hanging genitives.
- [ ] Cast / crew names verified against the show's titres.
- [ ] Ani Maghakyan credited — on slide 1 (small line), slide 2 (first credit), and in the caption.
- [ ] CTA action row in Armenian first («Հավանիր · Պահպանիր · Տարածիր»), not English.
- [ ] Caption: cinematic hook in the first ≤125 chars · Ani's name · one clear CTA · `#MaghakianSWA` + 10–15 hashtags (Armenian-script + Latin mix, e.g. `#Գյումրի #ԹղթեԵրազանք #ՀայկականՍերիալ #ArmenianSeries #AniMaghakyan #Screenwriting`).
- [ ] Where possible, prefer real promo stills / show frames over AI-looking composites.
- [ ] 4:5 portrait; if it's a video carousel, consider using the show's **original theme music** as the audio (strong nostalgia trigger — see below).

### What the data says (May 2026 baseline)

Three spotlight posts:

| Post | Age | Views | Likes | Comments | Shares | Saves | New follows |
|---|---|---|---|---|---|---|---|
| «Օտարը» | 1 wk | 11,763 | 127 | 11 | 15 | 27 | 16 |
| «Էլենի օրագիրը» | 5 d | **85,980** | 1,261 | 174 | **407** | 331 | **72** |
| «Էլենի օրագիրը 2» | 3 d | 54,296 | 624 | 91 | 102 | 113 | 22 |

- **The winning pattern** = recognizable nostalgic show + the show's **original theme song** as audio + **7-slide** structured spotlight + **comment-bait hook** ("how old were you when…", "season 1 or 2?"). «Էլենի» got ~7× the reach of «Օտարը» in less time and 72 follows from one post. **Shares** are the distribution driver — write hooks people forward to a friend.
- «Օտարը» is the floor (~12K): less universally nostalgic genre, foreign trending audio (Kavinsky), only 4 slides, posted before momentum.
- **Saves are strong** (331 / 113) — the structured data-table format is reference-worthy; keep it.
- Audience ≈ 85–87% women — current content serves the diaspora/fan audience well; the LinkedIn/industry audience is **not** served by spotlights — that needs separate craft/personal-voice content.
- **Bio-link clicks ≈ 1–2 per post** — current CTAs are reach-oriented (comment/save), no funnel. If a website/portfolio/contact goal exists, add an occasional "link in bio" CTA; otherwise accept reach as the goal.
- **Facebook cross-post ≈ 0 views** — fix the auto-share or stop counting FB as a channel.

### Posting cadence & timing

- Every **2–3 days** (matches the 3×/week target). Don't stack a new post on top of one that's still climbing.
- Best slot: **~20:00–21:00 Yerevan time** (the «Էլենի 2» 20:11 post performed well). Weekday evenings or Sunday evening.
- **Alternate** high-recognition long-runners («Օտարը», «Բեկորներ», «Կախվածություն», «Իրար դեմ») with emotionally distinctive ones («Թղթե երազանք», «84-ի ամառը», «Բլոկադա») — don't burn all the best-known titles at once; keep the feed varied in mood.
- Tie a spotlight to a date only when it genuinely fits (e.g. a Gyumri-set show near December 7) — don't delay otherwise; the emotional themes are evergreen.
- Vary format too — not every post should be a spotlight. Mix in behind-the-craft, Ani's personal voice, a standalone "~80,000 pages / 46 projects" graphic, "which of these shows did you watch?" carousels.

---

## Content Pillars

| Pillar | Content Type | Frequency |
|--------|-------------|-----------|
| **Project announcements** | Series launches, episode drops, premieres | As needed |
| **Behind the craft** | Writing process, script development, research | Weekly |
| **Cultural storytelling** | Armenian history, nostalgia, cultural context | Weekly |
| **Social proof** | Reviews, press mentions, audience reactions | As available |
| **Personal voice** | Ani's perspective on storytelling, cinema, writing | Bi-weekly |

---

## Do / Don't

| Do | Don't |
|----|-------|
| Open with a cinematic, sensory line | Open with "Exciting news!" or "We are pleased to announce" |
| Name the screenwriter (Ani Maghakyan) prominently | Bury the creator credit |
| Use specific details (year, place, emotion) | Use vague superlatives ("amazing," "incredible") |
| Write in the audience's language first | Default to English when Armenian is primary |
| Let the story sell itself | Over-explain or over-hype |
| Use `#MaghakianSWA` on every post | Forget brand hashtag consistency |

---

## Competitive Analysis & Strategy

### Reference Accounts Analyzed

| Account | Platform | Followers | Key Strength |
|---|---|---|---|
| **Shondaland** (Shonda Rhimes) | Instagram | 900K | Personal voice, emotional hooks |
| **A24 Films** | Instagram + Twitter | Millions | Character-world content, cult community |
| **Armenian Film Society** | Instagram | 28K | Diaspora-first, event-driven community |
| **Panarmenian TV** | Instagram | ~4K | Local Armenian audience |
| **Armenian Entertainment** | Instagram | ~3.8K | Entertainment-focused, bilingual |

---

### Best Practices — What Works

**Shondaland Model**
- Warm, storytelling-first captions — never "Excited to announce", always emotional opening line
- Ani Maghakyan's personal name and voice front and center, not the agency as a faceless brand
- Consistent visual identity across every post — no visual noise

**A24 Model**
- Character-driven content: story-world extensions on social (characters' own "accounts", in-world posts)
- 95% of marketing budget online — zero TV, zero print → full force on digital
- Carousel posts for behind-the-scenes and editorial content (highest engagement format at 0.55%)
- Cult following built through authenticity and specificity, not polish

**Armenian Film Society Model**
- Community-first posting — followers feel like members, not audience
- Diaspora language awareness — speaks to LA, London, Yerevan simultaneously
- Event anchoring — every post connects to a real moment (screening, festival, premiere)

---

### 8 Things Missing from Armenian Screenwriter Accounts

These gaps are Maghakian's competitive opportunity:

1. **Screenwriter personal voice** — all accounts post as faceless organizations; Ani Maghakyan's individual voice is unused and unreplicated
2. **Behind-the-craft content** — zero process visibility; audiences see announcements but never the work of writing
3. **Trilingual diaspora strategy** — Armenian, English, and Russian used inconsistently or not at all
4. **Carousel & Reels formats** — highest-reach formats (Reels for discovery, carousels at 0.55% engagement) are largely absent
5. **LinkedIn presence** — industry credibility platform entirely empty for Armenian screenwriters
6. **Character/story-world content** — no one extends the story universe onto social media (A24 model)
7. **Telegram community** — used as broadcast channel only; no polls, Q&A, or two-way conversation
8. **Posting consistency** — irregular cadence means algorithm de-prioritizes; no account maintains a reliable weekly rhythm

---

### Maghakian's 5 Unique Advantages

1. **Ani Maghakyan's personal voice** — the only Armenian screenwriter building a named, individual public creative identity; this is the primary differentiator
2. **Trilingual reach** — Հայաստան + Armenian diaspora (LA, London, Moscow) + international film industry professionals; no competitor covers all three
3. **Character/story-world content** — the A24 playbook applied to Armenian TV series; extend series universes onto social before and after air
4. **LinkedIn thought leadership** — first Armenian screenwriter to own the craft/industry conversation on LinkedIn; zero competition in this space
5. **Established brand system** — `#6450D2` purple, cinematic tone, logo, and identity already defined; consistency is execution, not starting from zero

---

### Weekly Posting Rhythm

#### Instagram

| Day | Content Type | Format | Notes |
|---|---|---|---|
| Monday | Behind the craft | Reel or carousel | Writing process, research, character work |
| Wednesday | Quote / pull quote | Static post | `#6450D2` purple bg, GHEA Grapalat font |
| Friday | Project update or cultural storytelling | Static or carousel | Armenian history, nostalgia, series context |
| Daily | Stories | 1–3 stories | Poll, question box, process peek, BTS |

**Caption structure every post:**
1. Hook — cinematic opening line (before "more" cutoff, ≤125 chars)
2. Story / context — 2–4 lines
3. CTA — one clear action
4. Hashtags — 10–15 (`#MaghakianSWA` on every post)

#### LinkedIn

| Frequency | Format | Content |
|---|---|---|
| 3× per week | Document carousel | Highest reach format — craft breakdowns, process insights |
| Weekly | Native video | Short expert insight or behind-the-scenes clip |
| Bi-weekly | Text post | Personal story — "In writing [series], I discovered…" |

**Tone on LinkedIn:** Lead with craft and credentials. Warm but professional. Specific stories outperform polished announcements — name the project, the challenge, the lesson.

#### Telegram

| Type | Cadence | Format |
|---|---|---|
| Project announcements | As needed | Long-form, cinematic opening, full context |
| Audience poll | Weekly | "Which era would you want a series about?" |
| Exclusive script excerpts | Bi-weekly | Short excerpt, watermarked, visually styled |
| Updates / behind scenes | 2–3× per week | Conversational, direct, no need for visual production |

- Pin the most important active project announcement
- Respond to comments — Telegram rewards conversation, not just broadcast
- 100% message delivery (no algorithm filtering) — use it for time-sensitive announcements

#### Facebook

- Mirror Instagram feed posts with longer caption versions
- Facebook audiences read more — use the space for deeper storytelling
- Video thumbnails: match Instagram feed template Type A
- First 3 seconds of video: series title on black — no silence, no logo intro

---

### A24 Playbook — Applied to Maghakian

For each active series, create **story-world social extensions**:
- A scene-specific Telegram post written from a character's perspective
- An Instagram story "from" the era of the series (archival photo + in-world caption)
- A pull-quote carousel from the script — styled as editorial, not promotional

This is zero-budget, requires no production, and builds cult engagement before premiere. No Armenian production company or screenwriter is doing this.

---

## Reddit-ի Միտումները և Բովանդակության Ռազմավարությունը 2025

### Սցենարական առաջատար subreddit-ները

| Subreddit | Անդամներ | Ֆոկուս |
|---|---|---|
| **r/screenwriting** | 1M+ | Արհեստ և կարիերա — ամենամեծ սցենարական համայնքը |
| **r/Filmmakers** | Հարյուր հազարավոր | Պրոդակշն, տեխնիկա, միկրոբյուջե, դիստրիբյուցիա |
| **r/TrueFilm** | Մեծ | Կինոյի ինտելեկտուալ վերլուծություն, սինեֆիլ քննարկում |
| **r/television** | Միլիոնավոր | Սերիալների քննարկում, սցենարի որակի բանավեճեր |
| **r/writing** | Մեծ | Գրելու արհեստ, պատմվածքի հիմունքներ |

---

### 7 Տրենդային Թեմա 2025-ին

**1. ԱԲ-ն ընդդեմ մարդկային սցենարիստի**
Ամենաշատ քննարկվող թեման — «Կարո՞ղ է ԱԲ-ն իրական սցենար գրել» բանավեճը viral է հազարավոր thread-երում։ Հեղինակային իրավունքի վեճեր (Midjourney ընդդեմ ստուդիաների), սցենարիստների աշխատատեղերի անվտանգություն, ինքնատիպություն ընդդեմ ավտոմատացման։ Հայկական անկյունը՝ ԱԲ-ն չի կարող վերարտադրել ապրած մշակութային հիշողությունը։

**2. Հեռուստատեսություն մուտք գործելը — writer's room-ի հասանելիություն**
- Spec script ընդդեմ բնօրինակ pilot-ի բանավեճ
- Fellowship-ները (NBC, CBS, WB)՝ որպես ապացուցված ճանապարհ
- «Ապրած փորձը» բազմիցս հաստատվել է որպես №1 տարբերակիչ — հեռուստաշոուների ղեկավարները ուզում են գրողներ, ովքեր ապրել են իրենց հերոսների աշխարհում

**3. Հեռուստասերիալի pilot-ի արհեստը**
- Ինչպես է pilot-ը համոզում դիտողին շարունակել դիտումը
- Հերոսի աղեղը առաջին դրվագում — ի՞նչ բացահայտել, ի՞նչ պահել
- «Story engine» — ինչպես մեկ pilot-ում կառուցել ողջ սեզոնը

**4. Լավագույն գրված սերիալների վերլուծություն**
Reddit-ում ամենաբարձր engagement-ը ստացած քննարկումը 2025-ին.
- **Andor** — քաղաքականապես բարդ, հասուն, հայ դիտողին հարազատ թեմաներ
- **Severance** — պարզ premise, համարձակ պատում, էքզիստենցիալ խորհրդածություն
- **The Pitt** — իրական ժամանակում պատում, արդիական սոցիալական խնդիրներ մեկ օրում
- **Breaking Bad / Better Call Saul** — ոսկե ստանդարտ, որ վկայակոչվում է ամեն արհեստի thread-ում

**5. Երկխոսություն — «Ինչն է աշխատում»**
Ամենահետևողականորեն քննարկվող հարցը բոլոր subreddit-ներում։ Հիմնական կետեր՝ ենթատեքստ՝ բացահայտ բացատրության փոխարեն, բնական, շեղվող խոսք, լռությունը՝ որպես պատմելու միջոց, դիտողին վստահելը։

**6. Ինքնատիպություն և ապրած փորձ**
2025-ի viral Reddit պահը — սցենարիստ, որը Reddit համայնքից հասավ Sundance (հունվար 2025)։ Հիմնական եզրակացությունը՝ **կոնկրետ անձնական պատմություն + համառություն = տարբերակիչը**։ Հայ սփյուռքից ստեղծագործողը հումորը քաղեց ընտանեկան պատմություններից և viral դարձավ սփյուռքում։ Ապրած փորձը փափուկ ակտիվ չէ — դա մրցակցային առավելությունն է։

**7. Հայկական պատմողականություն — բաց պատուհանը**
Սև Օհանյանը (հայ-ամերիկացի պրոդյուսեր) ունեցավ 2025-ի ամենամեծ տարին — *Sinners*, *Ironheart*, *Eyes of Wakanda*։ Reddit-ում ընդարձակ քննարկվեց հայ ձայների մուտքը մեյնսթրիմ։ Պատուհանը բաց է, տարածքը՝ չզբաղեցված։

---

### Շաբաթական կրկնվող ձևաչափեր — Ամենաբարձր engagement

| Ձևաչափ | Օր | Ինչն է հավաքում upvote-ներ |
|---|---|---|
| **Logline Monday** | Երկուշաբթի | Կոնկրետ, անսպասելի logline-ներ՝ հստակ խաղադրույքով |
| **Dialogue Friday** | Ուրբաթ | Ենթատեքստով հագեցած երկխոսություններ, բնական ձայներ |
| **AMA նիստեր** | Փոփոխական | Աշխատող պրոֆեսիոնալներ՝ իրական կարիերային ուղիների մասին |
| **Անձնական ճանապարհի փոստեր** | Ցանկացած | «Ինչպես անցա X-ից Y» — հետևողականորեն ամենաշատ upvote-ները |

---

### Maghakian-ի բովանդակության գաղափարներ — Reddit-ի միտումների հիման վրա

#### Tier 1 — Viral ներուժ

Սրանք ուղղակիորեն համապատասխանում են Reddit-ի ամենաբարձր engagement-ի ձևաչափերին՝ անձնական ճանապարհ + կոնկրետ արհեստ + թերներկայացված ձայն։

| Փոստի գաղափար | Տրենդի կեռիկ | Հարթակ |
|---|---|---|
| *«Ինձ ասում էին՝ հայ դիտողը չի նայելու «Էլենի օրագիրը» — իսկ այն դարձավ Google Armenia-ի №1 հարցումը 2018-ին»* | Անձնական ճանապարհ + ընդդեմ բոլոր դժվարությունների | Instagram, LinkedIn |
| *«ԱԲ-ն չի կարող հայկական մելոդրամա գրել — ահա ինչու»* | ԱԲ ընդդեմ մարդու բանավեճ + հայկական յուրահատկություն | LinkedIn carousel, Instagram |
| *«Առաջին անգամ թատրոնի համար սցենար գրեցի — Արցախի մասին. ահա ինչ փոխվեց»* | Ապրած փորձ + արհեստի խոցելիություն | Instagram, LinkedIn |

#### Tier 2 — Համայնքի կառուցում

| Փոստի գաղափար | Տրենդի կեռիկ | Ձևաչափ |
|---|---|---|
| *«Ինչպես գրեցի «84-ի ամառը»-ի pilot-ը — կառուցվածքը»* | TV Pilot Craft thread | LinkedIn document carousel |
| *«Ինչպես ստեղծել սեզոնի աղեղը հայկական հեռուստատեսությունում»* | Սեզոնի աղեղի վերլուծություն + հայկական ՀՀ համատեքստ | Instagram carousel |
| *«Երկխոսություն հայերենով — ինչու է ավելի դժվար, քան թվում է»* | Dialogue Friday ձևաչափ | Instagram + LinkedIn |
| *«Ի՞նչ է prestige drama-ն հայկական համատեքստում»* | TrueFilm-ի ոճով վերլուծություն, r/television-ի կեռիկ | Երկար ֆորմատ՝ Facebook / LinkedIn |
| *«Սև Օհանյանից հետո — ինչպե՞ս բերել հայ սցենարիստին մեյնսթրիմ»* | Հայկական անկյուն + 2025-ի թափ | LinkedIn thought leadership |

#### Tier 3 — Պատմական աշխարհի ընդլայնումներ

Սրանք Maghakian-ի սերիալների աշխարհները տարածում են սոցցանցերում՝ A24-ի playbook-ը կիրառելով հայկական բովանդակության վրա։

| Սերիալ | Բովանդակության գաղափար |
|---|---|
| **«84-ի ամառը»** | *«Ինչպիսին է 40 տարվա բարեկամությունը մեկ տեսարանում»* — երկխոսության վերլուծություն շոուից |
| **«Էլենի օրագիրը»** | *«Ինչու սերիալը դարձավ №1 հարցումը — ինչ է սա նշանակում սցենարիստի համար»* — խորհրդածական փոստ |
| **«Բլոկադա» (թատրոն)** | *«Ինչպես գրել շրջափակման մասին՝ առանց դիտողին մանիպուլյացիայի ենթարկելու»* — արհեստի էթիկայի փոստ |

---

### Reddit-ի հիմնական դասը Maghakian-ի համար

Reddit-ը ամենից շատ պարգևատրում է երեք բան՝
1. **Կոնկրետ անձնական պատմություններ** — ոչ ընդհանուր խորհուրդներ
2. **Արհեստի վերլուծություններ իրական, անվանված նախագծերից** — ոչ տեսություն
3. **Թերներկայացված ձայն՝ ապրած փորձով** — Անի Մաղաքյանն ունի 46 նախագիծ (2,200+ սերիա, ~80,000 էջ սցենար, 2017–2026 — տես [`portfolio.md`](portfolio.md)), 700+ լրագրողական հոդված, թատերական պիեսներ, ապրած հայկական պատմություն։ Այս ծավալից գրեթե ոչինչ դեռ հանրությանը տեսանելի չէ որպես անձնական ստեղծագործական ուղի։ Հենց այդ բացն է բովանդակության ռազմավարությունը։

---

## Official Social Media Accounts

### Ani Maghakyan — Personal

| Platform | URL |
|---|---|
| **Instagram** | [instagram.com/ani_maghaqia](https://www.instagram.com/ani_maghaqia/) |
| **Facebook** | [facebook.com/ani.maghaqyan](https://www.facebook.com/ani.maghaqyan?locale=hy_AM) |
| **LinkedIn** | [linkedin.com/in/ani-maghaqyan-5ba6804b](https://www.linkedin.com/in/ani-maghaqyan-5ba6804b/) |

### Maghakian Script Writing Agency

| Platform | URL |
|---|---|
| **Instagram** | [instagram.com/maghakianscripts](https://www.instagram.com/maghakianscripts/) |

---

## Quick Reference Card

```
Brand:     Maghakian Script Writing Agency
Founder:   Ani Maghakyan
Colors:    #6450D2 (purple) · #0D0D0D (black) · #FAFAFA (white)
Logo:      Cursive M + bold italic "Maghakian" + "SCRIPT WRITING AGENCY"
Type:      Bold italic serif (display) + clean sans-serif (body)
Tone:      Cinematic · Warm · Confident · Nostalgic · Precise
Languages: Armenian (primary) · English · Russian
Hashtag:   #MaghakianSWA #AniMaghakyan
Posting:   Instagram 3×/week + daily stories · LinkedIn 3×/week · Telegram 2–3×/week
Edge:      Personal voice · Trilingual · A24 story-world model · LinkedIn ownership
Portfolio: 46 projects · 2,200+ episodes · ≈80,000 script pages · 2017–2026 → portfolio.md
```
