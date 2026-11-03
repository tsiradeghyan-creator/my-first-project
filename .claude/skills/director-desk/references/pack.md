# Script Pack: how to write pack.md

`pack.py facts` counts; you write. Read `facts.md` AND the script before writing a word.
Every event, name, age and place in pack.md must be in the script. If the script doesn't say it, leave it out
or ask Tigran/Ani. Don't invent a backstory and don't sell the story better than it is.

## File format
```
---
title: ...
format: Դրամա · սերիալ · 8 × 45'
format_en: Drama · series · 8 × 45'
contact: Maghakian Scripts · maghakianscripts.com
---
## logline            one sentence: who, what they want, what stands in the way, the stakes
## tagline            optional, poster line
## synopsis_paragraph 100–150 words, whole story incl. the ending
## synopsis_page      ≤ 600 words (Sundance ≤ 750, Micro-series ≤ 500), incl. the ending
## synopsis_long      optional, 2–5 pages
## characters         ### NAME (exactly as in the script cues) + 50–120 words: want, wound, contradiction
## world              series: where and when, the rules of this world
## tone               tone & style, 2–4 references in words
## season_arc         series: where the season starts and ends
## episodes           series: ### Ep 1 + 60–120 words each
## why_now            why this story, why now, why us
## audience           who watches it, which platform
## comps              2–4 comparable titles + one line why
## team               Ani + studio facts from maghakian-roast-room/business.md only
## logline_en / synopsis_paragraph_en / synopsis_page_en / characters_en   English versions
```
Only `logline` + `synopsis_paragraph` are required; every missing piece is listed in CHECK.md.

## Rules
- Synopses tell the ending. Buyers and labs want it; a "teaser" synopsis is a beginner's mark.
- Present tense, third person, no rhetorical questions, no "this powerful story".
- English versions are written for an English reader, not translated word by word. Names keep the script's
  transliteration (Արամ → Aram).
- Pass the final texts through `anthropic-skills:humanizer` before they go out.
- Story work (stronger logline, structure): `anthropic-skills:ani-screenwriting-workflow`.

## What each recipient gets (folders)
| Folder | For | Files |
|---|---|---|
| 01_producer | producer, agent | one_pager.pdf, logline_synopsis.pdf |
| 02_platform | streamer, broadcaster | series_bible.pdf (feature: pitch_deck.pdf), episode_synopses.pdf |
| 03_production | line producer, director | script PDF/DOCX/FDX, breakdown md/csv per episode, season.md/csv |
| 04_casting | casting director, actors | casting_breakdown.pdf/csv, sides/NAME.pdf (top scenes by the role's dialogue) |
| 05_international | foreign buyers, funds | one_pager_en.pdf |
| 06_competition | labs, funds, contests | application_<preset>.pdf |

## Presets (limits checked in CHECK.md)
| Preset | Source (checked 2026-11) | Limits |
|---|---|---|
| sundance_feature | sundance.org/programs/feature-film | logline ≤ 75 words, synopsis ≤ 750, up to 3 bios ≤ 150; English |
| sundance_microseries | collab.sundance.org Micro-Series terms | logline ≤ 75, synopsis ≤ 500, bible 1–3 pages; English |
| eurimages | coe.int/eurimages regulations 2025 | synopsis 1 page, English script required |
| generic | studio default | logline ≤ 50, paragraph ≤ 150, page ≤ 600, bio ≤ 120 |
Check a lab's current rules before each submission; add a preset to `PRESETS` in `scripts/pack.py`.

## Not yet
Full HY/RU → EN script translation in format, deck with images, submission tracker. See NOTES.md.
