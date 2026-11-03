---
name: director-desk
description: "Director's and producer's desk: proofreading of Armenian scripts (punctuation, spelling, typos, continuity) into a Word working version with highlighted changes and comments plus a clean final PDF with the Maghakian logo; does the jobs of KIT Scenarist / Story Architect / WriterDuet / Pisar, Storyboarder, ShotDeck search and Canva treatments in one place. (1) Screenplay formatting: Fountain → industry 'American' format PDF, DOCX, Final Draft FDX, in Armenian, Russian or English. (2) Line-producer breakdown: scenes, page eighths, characters, locations, INT/EXT, day/night, CSV for a stripboard/schedule. (3) Storyboard sheet PDF from stills + shot list (film-crew output). (4) Treatment / pitch deck: structure, gap audit, branded PDF. (5) Reference hunting: ShotDeck / Film-grab search terms per shot. Use for: format a script, сценарий в американке, սցենարը ֆորմատավորել, page count / runtime, breakdown, раскадровка в PDF, storyboard sheet, treatment, тритмент, պիչ դեք, pitch deck."
---

# Director's desk

Five tools for the work around a script. Scripts are in `scripts/`, fonts in `fonts/` (FreeMono has Courier
metrics with Armenian + Cyrillic; DejaVu Sans for decks/boards). Needs Python 3 + reportlab, Pillow, python-docx.
Paths below are relative to this skill folder (`.claude/skills/director-desk/`).

## 1. Script format (KIT Scenarist / Pisar / WriterDuet)

Write or convert the script into **Fountain** (plain text). Then:

```bash
python3 scripts/screenplay.py path/script.fountain --all --lang hy        # pdf + docx + fdx + breakdown md + csv
python3 scripts/screenplay.py path/script.fountain --pdf --paper a4 --scene-numbers --lang ru
```

Fountain cheat sheet (tell Ani if she writes directly in it):
- Scene heading: line starting `INT.` `EXT.` `ИНТ.` `НАТ.` `ЭКСТ.` `ԻՆՏ.` `ԷՔՍՏ.` `ՆԵՐՍ.` `ԴՐՍ.`, or any line forced with a leading `.`
  (`.ԺԱՄԱԳՈՐԾԻ ԱՐՀԵՍՏԱՆՈՑ - ԱՌԱՎՈՏ`). Optional scene number at the end: `#12#`.
- Character: a line in CAPITALS after a blank line, dialogue right under it; `(parenthetical)` on its own line.
  Force with `@` if the name has lowercase. `(Ձ.Կ.)`, `(V.O.)`, `(З.К.)` extensions are fine.
- Transition: `> CUT TO:` / `> ԿՏՐՈՒՄ` (always use `>` in Armenian and Russian). Centered: `>THE END<`.
- `# Section` and `= synopsis` lines don't print; they feed the breakdown. `[[note]]` and `/* boneyard */` are hidden.
- `===` page break. Title page: `Title:`, `Credit:`, `Author:`, `Draft date:`, `Contact:` at the top.

**Ani's scripts come as KIT Scenarist .docx exports.** Convert them with the dedicated script (reads KIT
paragraph styles and Ani's house layout: "N. ՏԵՍԱՐԱՆ" → location line → cast line → "1984Թ"; "ՊԵՐԵԽՈԴ",
"ՖԼԵՇԲԵՔԻ ՍԿԻԶԲ", "ՓԼԵՅՍՄԵՆԹ" as supers/tags; "/ՆԵՂՎԱԾ/" → parentheticals). Words and punctuation stay as written;
only separators in location lines are unified so the breakdown can group them. Ani's format has no INT/EXT, so the
converter adds **ՆԵՐՍ. / ԴՐՍ. / ՆԵՐՍ./ԴՐՍ.** from the location words (ԴԻՄԱՑ, ԲԱԿ, ՓՈՂՈՑ, ՄՈՏ… = outside; rooms,
house, restaurant = inside; ՍԵՆՅԱԿԻ ԴԻՄԱՑ = inside; car = inside, car + outside place = both). Unsure ones get
`= IE?` and show as ❓ in the breakdown for Ani to confirm. `--no-int-ext` turns it off. Tigran asked for this (2026-11-03).
```bash
python3 scripts/kit_docx_to_fountain.py ep*.docx --series "84-ի ամառը" --outdir out/
for f in out/*.fountain; do python3 scripts/screenplay.py "$f" --all --lang hy; done
python3 scripts/season.py out/*.fountain --out out/season
```
Tested 2026-11-03 on 8 real episodes (84-ի ամառը 1/2/3/7/9 + 3 eps of the Vilo series): scene counts match the
sources, no words lost. Other sources (Word without styles, PDF): rewrite into Fountain by hand, line by line.
Always look at page 1–2 of a PDF as images (`pdftoppm -r 60 -png`) before handing it over.
**Ani's scripts are private: never commit them or their outputs to the repo; work in the scratchpad.**

Format: Letter by default (industry), `--paper a4` for local buyers. Courier-metric 12 pt, 1.5"/1" margins,
character 3.7", dialogue 2.5" × 3.5", page numbers top right, (MORE)/(CONT'D) on split dialogue
(`--lang` sets the labels: hy `(ՇԱՐՈՒՆԱԿԵԼԻ)`/`(ՇԱՐ.)`, ru `(ДАЛЬШЕ)`/`(ПРОД.)`; confirm the Armenian
labels with Ani once and update `LABELS` in the script if she uses others). 1 page ≈ 1 screen minute.
DOCX uses Courier New (Word substitutes a font for Armenian); FDX opens in Final Draft / WriterDuet / KIT.

## 1b. Proofreading (սրբագրում) → working Word + final PDF

Read `references/proofreading_hy.md` first (rules: question mark on the stressed vowel, dialogue keeps the
character's colloquial voice, meaning problems = remarks only). Then:
1. Convert to Fountain (above). Run `proofread.auto_fixes` once and read that text scene by scene (chunks of ~8).
2. Write a corrections JSON (`scene`, `find` copied exactly, `replace`, `type`, `why`; no `replace` = remark).
3. `python3 scripts/proofread.py ep01.fountain corrections.json --out proof/` →
   `ep01_WORK.docx` (yellow = changed, turquoise = remark, a Word comment on each), `ep01_FINAL.pdf` (clean, logo),
   `ep01_FINAL.docx/.fdx/.fountain`, `ep01_corrections.md` (table + automatic checks: speakers missing from the cast
   line, duplicate scene numbers, names written two ways, Latin/Cyrillic letters in Armenian words).
Check "applied X/Y"; fix any "❌ text not found" and rerun. Check every scene; say how many were checked.

**Logo:** `assets/maghakian_logo_dark.png` (on white) and `_light.png` (on dark), from Tigran's file 2026-11-03.
screenplay.py puts it on the title page and small in the footer of every PDF and Word page (`--no-logo` to skip).

**ChatGPT pack:** `gpt/` holds the Custom GPT instructions (`INSTRUCTIONS.md`), Tigran's Armenian guide
(`HOW_TO_hy.md`) and `build_pack.py`, which copies the scripts, fonts, logo and rules into
`Maghakian_Script_Desk_GPT.zip`. Rebuild and resend the pack whenever a script or rule here changes.

## 2. Line-producer breakdown (per episode and per season)

`season.py` merges episodes: pages and scenes per episode, **sets across the season** (main location →
rooms, in which episodes: shoot each set as one block), **characters × episodes** matrix (actor days,
contracts), product placement scenes (💰, from "ՓԼԵՅՍՄԵՆԹ" lines), and a ⚠️ list of names/locations
probably written two ways (typos like ՎՎԻԼՈ / ՎԻԼՈ, ՌԵՍՈՏՈՐԱՆ / ՌԵՍՏՈՐԱՆ): give that list to Ani.


Comes with `--report` / `--csv` (or `--all`): pages and runtime, each scene with page and length in
**eighths**, speaking characters per scene, character table (scenes, dialogue lines), locations table
(INT/EXT, time of day, scenes, total eighths). The CSV opens in Sheets/Excel as the base of a stripboard and
shooting schedule: sort by location, then time of day, to group shooting days. Use it for budgets and for
the "production scale" page of a pitch deck.

## 3. Storyboard sheet (Storyboarder / Make Storyboard)

```bash
python3 scripts/storyboard_sheet.py shots.json --out board.pdf [--paper letter] [--logo logo.png]
```
`shots.json`: title, subtitle, aspect (`16:9`, `2.39:1`, `9:16`…), shots with `id, image, shot, lens, move,
action, duration, sound, note` (format in the script header). Build it from film-crew files: `06_shot_list.md`
(lens, move, action), `05_edit_plan.md` (order, durations), `07_sound.md` (sound); images = the stills.
Shots without an image get an empty frame. Example: `reels/tigran-the-great/film-crew_09-16/storyboard_sheet.json`.
3×2 per page for horizontal, 4×1 for vertical (override with `columns`/`rows`). Stills are downscaled to keep
the PDF light. For pre-stills blocking, the lebera grey-blockout method in NOTES (2026-11-02) is the 3D option.

## 4. Treatment / pitch deck (Canva / Supa, but with structure)

Read `references/treatment.md` first: structure per format (series, feature, children's), and the **gap audit**.
Run the audit on any existing material and tell Tigran what is missing before building.
Write the deck as Markdown (format in the script header, example `examples/treatment_hy.md`), then:

```bash
python3 scripts/treatment_pdf.py deck.md --layout deck     # A4 landscape, one idea per page
python3 scripts/treatment_pdf.py deck.md --layout doc      # A4 portrait, classic treatment
```
Brand is built in (black cover, white pages, graphite text, one red accent). For a deck Tigran will edit by hand,
send the same content to the Artifact Slides type, Canva/Adobe Express or the `pptx` skill instead.
Studio facts only from `maghakian-roast-room/business.md`; text passes `humanizer` before it goes out.

## 5. Reference hunt (ShotDeck / Film-grab)

We can't scrape ShotDeck (paid, licensed). Instead, for each key shot give Tigran ready search lines:
- **ShotDeck** (filters exist for these): film title(s) from the style lens + shot type + lighting + colour +
  time of day + lens/framing, e.g. `The King 2019 · wide · overcast · desaturated · battle · low angle`.
- **Film-grab** (free, search by film title): 2–3 film titles that match the lens.
- Also one line for Google Images / Pinterest in the source language.
He picks a frame and sends it back; it becomes an `@Image` reference for film-crew / the model skill.

## Not covered (use the real tool)
Frame.io / Wipster (timecoded review on video drafts): file sizes are too big for anything we can host;
the free Frame.io plan is the answer. Collaborative live editing like WriterDuet: share the Fountain file
through this repo or Google Drive.
