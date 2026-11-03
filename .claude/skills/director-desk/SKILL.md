---
name: director-desk
description: "Director's and producer's desk: does the jobs of KIT Scenarist / Story Architect / WriterDuet / Pisar, Storyboarder, ShotDeck search and Canva treatments in one place. (1) Screenplay formatting: Fountain → industry 'American' format PDF, DOCX, Final Draft FDX, in Armenian, Russian or English. (2) Line-producer breakdown: scenes, page eighths, characters, locations, INT/EXT, day/night, CSV for a stripboard/schedule. (3) Storyboard sheet PDF from stills + shot list (film-crew output). (4) Treatment / pitch deck: structure, gap audit, branded PDF. (5) Reference hunting: ShotDeck / Film-grab search terms per shot. Use for: format a script, сценарий в американке, սցենարը ֆորմատավորել, page count / runtime, breakdown, раскадровка в PDF, storyboard sheet, treatment, тритмент, պիչ դեք, pitch deck."
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

Converting from Word/KIT/PDF: read the source, rewrite into Fountain line by line (do not edit Ani's text),
run the script, then look at page 1–2 of the PDF as images (`pdftoppm -r 60 -png`) before handing it over.

Format: Letter by default (industry), `--paper a4` for local buyers. Courier-metric 12 pt, 1.5"/1" margins,
character 3.7", dialogue 2.5" × 3.5", page numbers top right, (MORE)/(CONT'D) on split dialogue
(`--lang` sets the labels: hy `(ՇԱՐՈՒՆԱԿԵԼԻ)`/`(ՇԱՐ.)`, ru `(ДАЛЬШЕ)`/`(ПРОД.)`; confirm the Armenian
labels with Ani once and update `LABELS` in the script if she uses others). 1 page ≈ 1 screen minute.
DOCX uses Courier New (Word substitutes a font for Armenian); FDX opens in Final Draft / WriterDuet / KIT.

## 2. Line-producer breakdown

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
