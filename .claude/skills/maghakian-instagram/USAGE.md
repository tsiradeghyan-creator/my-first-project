# USAGE.md – Quick Start Guide

How to invoke and use this skill for @maghakianscripts content.

## 🚀 3 Ways to Invoke

### Method 1 — Auto-trigger (recommended, easiest)
Just write your task naturally. Skill auto-activates when any of these keywords appear:
- **English**: caption, hook, reel, post, story, carousel, instagram, poster, image, visual, title card, thumbnail, banner
- **Հայերեն**: ինստագրամ, առաջխաղացում, հուկ, նկար, պոստեր
- **Project names** (any of 47): Ելենի օրագիրը, Hotel Grand, Բեկորներ, Երկուսով, Մալենա, etc.

### Method 2 — Explicit
> «Use the maghakian-instagram skill to [task]»
> «Skill-ով կատարիր [task]»

### Method 3 — Slash command (in Claude Code UI)
Type `/` and select the skill if shown.

---

## 📋 Prompt Templates (copy-paste ready)

### Template A — Full content package
```
[Skill, project-name] project-ի համար ստեղծիր.
- 1 primary reel/carousel
- 3 reel hook variants
- 1 story sequence (5-7 stories)
- 1 IMAGE_PROMPTS poster variant

Goal: [save / comment / DM / follow]
Voice: [Personal Անի / Agency «մենք» / Hybrid]
Run Research Protocol if project data is missing.
```

### Template B — Single caption
```
Caption գրիր [project-name]-ի [event/angle]-ի համար:
- Format: feed post / reel / carousel
- Voice: [pick]
- Goal: [primary metric]
- Existing visual: [attached / describe]
```

### Template C — Poster only
```
IMAGE_PROMPTS-ով poster prompt տուր [project / event]-ի համար:
- Template: [1-7 from IMAGE_PROMPTS.md, or describe]
- Tool: [Midjourney / ChatGPT / Flux / Ideogram]
- Aspect: [9:16 / 1:1 / 4:5]
- Armenian text on poster: [exact text or placeholder]
```

### Template D — Analyze existing content
```
Վերլուծիր skill-ի rubric-ով այս post-ը:
[attach image / paste caption]
- Run QUALITY_GATE
- Score by gate breakdown
- Suggest specific improvements
```

### Template E — Strategy / research
```
Research protocol-ով անցիր [project-name]-ի վրա:
- Web search
- Cache update in PROJECT_LIBRARY.md
- Ask user for gaps if any
- Then suggest content angles
```

---

## 🎯 Module Quick-Reference

What to ask if you need a specific module:

| Need | Ask for... |
|------|-----------|
| Hook idea | «Hook variants HOOKS_LIBRARY-ից» |
| CTA selection | «CTA suggestion CTA_LIBRARY-ից, goal = X» |
| Psychology trigger check | «PSYCHOLOGY-ով audit արա այս post-ը» |
| Caption framework | «FRAMEWORKS Pixar/PAS/BAB-ով caption» |
| Scroll-stopper opening | «PATTERN_INTERRUPTS-ից տուր 3 variant» |
| Engagement mechanic | «ENGAGEMENT_TACTICS #N-ով կառուցիր» |
| Reel editing | «REELS_EDITING-ով audit արա» |
| Posting time | «CONTENT_CALENDAR-ից suggest» |
| Hashtags | «HASHTAGS-ից set 1/2/3» |
| Post idea bank | «POSTS_BANK-ից 5 idea պատահական» |
| Metric review | «METRICS-ով evaluate performance» |
| Bio rewrite | «BIO_HIGHLIGHTS-ի 3 variant» |
| DM funnel | «DM_RESPONSES-ով կառուցիր funnel» |
| Pre-publish check | «QUALITY_GATE 30-check audit» |
| Project facts | «PROJECT_LIBRARY-ից բաց արա [project]» |
| 2026 algorithm | «ALGORITHM_2026-ով audit» |
| Keyword SEO | «KEYWORD_SEO-ով rewrite» |
| Trial Reels strategy | «TRIAL_REELS-ով plan» |
| Broadcast Channel | «BROADCAST_CHANNEL-ով setup» |

---

## ⚙️ Setup Requirements

### Skill location
Currently lives at: `.claude/skills/maghakian-instagram/`

### To use across all projects (not just this repo)
```bash
cp -r .claude/skills/maghakian-instagram ~/.claude/skills/
```

### To make available in main branch of this repo
```bash
git checkout main
git merge claude/instagram-story-preview-hbCwI
git push origin main
```

---

## 🧪 Quality Expectations

When skill is invoked correctly, output will include:
- ✅ Research Protocol execution (per RESEARCH_PROTOCOL.md)
- ✅ Provenance documentation (📚 sources / ✅ verified / ⚠️ hypothetical)
- ✅ QUALITY_GATE 30-check audit
- ✅ At least 1 Maghakian Doctrine tactic (12 available)
- ✅ At least 2 psychological triggers stacked
- ✅ Voice matching Voice Decision Matrix
- ✅ Anti-pattern free
- ✅ Brand-locked aesthetic (if visual)

If any of these are missing in output → the skill underperformed. Tell it to re-run with explicit reference to the missing module.

---

## 💡 Best Practices

### DO
- Provide project name explicitly
- Attach posters / scenes / screenshots when available
- State the goal (save / DM / follow / etc.)
- Trust the Research Protocol — let it ask you gaps
- Review the QUALITY_GATE score before publishing

### DON'T
- Don't ask for «something quick» without context — quality drops
- Don't skip the Research Protocol — fabrication kills trust
- Don't use the skill for non-Maghakian content (it's brand-locked)
- Don't ignore «pre-publish requirements» in output (PDF brief, handle verification, etc.)

---

## 🎓 Learning Loop

After each post:
1. Track metrics (save, send, comment, profile visits)
2. Compare to METRICS.md benchmarks
3. Update PROJECT_LIBRARY.md with what worked
4. Refine HOOKS_LIBRARY / POSTS_BANK with new patterns
5. Skill gets smarter every cycle

---

## 🔗 Skill Architecture (22 files)

```
SKILL.md                    # Main entry (start here)
USAGE.md                    # This file — quick start
README.md                   # (n/a)

# Founding strategy modules
ACCOUNT_CONTEXT.md          # Brand identity, analytics, manifesto
HOOKS_LIBRARY.md            # 130 hooks
CTA_LIBRARY.md              # 60 CTAs
PSYCHOLOGY.md               # Cialdini + Mystery
FRAMEWORKS.md               # Pixar/PAS/BAB/AIDA/Hero
PATTERN_INTERRUPTS.md       # 15 scroll-stoppers
ENGAGEMENT_TACTICS.md       # 15 mechanics
REELS_EDITING.md            # Cinematic rules
CONTENT_CALENDAR.md         # 30-day + 14-day launch
HASHTAGS.md                 # 3 sets × 30
POSTS_BANK.md               # 100 ideas
METRICS.md                  # Tracking + A/B test
IMAGE_PROMPTS.md            # AI image generator (7 templates)

# Process & guardrails
RESEARCH_PROTOCOL.md        # Pre-write web + ask user
PROJECT_LIBRARY.md          # 47-project research cache
QUALITY_GATE.md             # 30-check pre-publish

# Conversion
BIO_HIGHLIGHTS.md           # Profile optimization
DM_RESPONSES.md             # Lead funnel templates

# 2026 updates
ALGORITHM_2026.md           # DM sends = #1, keywords > hashtags
KEYWORD_SEO.md              # Profile/caption SEO
TRIAL_REELS.md              # Test with non-followers (at 1K+)
BROADCAST_CHANNEL.md        # Inner circle (at 5K+)
```
