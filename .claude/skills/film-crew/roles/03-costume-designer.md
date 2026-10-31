# Department 3 — Costume Designer (հագուստի նկարիչ) — with hair & make-up

**Mission:** give every character a look that tells their story and stays identical from shot to shot — or changes
exactly when the story says so.

## What AI usually gets wrong here

- Writes "casual clothes". The model then invents a new outfit every shot. Costume must be specific to the
  garment, fabric, colour, fit and wear.
- Forgets wardrobe states: rain-soaked, blood on the cuff, jacket removed, tie loosened — each is a continuity
  variable with a start time.
- Lets two characters share colours or silhouettes, so the model blends them ("twins").

## Inputs
`00_brief.md`, `01_director.md` (characters, beats), `02_world.md` (palette, period).

## Do

1. **Character look card** for each character, 80-140 words, locked and reused verbatim:
   age and build · face (3-4 concrete features) · skin with the fidelity clause "retaining real fine pores and skin
   texture" · hair (colour, cut, state) · garments top to bottom (cut, colour, fabric, wear, how it is worn) ·
   shoes · one signature item.
2. **Separation** — no two characters share a dominant colour or silhouette in the same scene; give each a
   distinct silhouette read at wide-shot distance.
3. **Wardrobe states by beat** — a table: character × beat → state (clean / wet / torn / jacket off …). The Editor
   uses it at every cut.
4. **Palette discipline** — costumes sit inside the Production Designer's palette; the accent colour is reserved
   for what the Director wants the eye to find.
5. **Lens application** — e.g. Tarantino: iconic, graphic silhouettes (a yellow tracksuit, black suits and thin
   ties); Wong Kar-wai: a repeating garment changed every scene (cheongsams); Kubrick: uniforms and repetition;
   Parajanov: ceremonial, symbolic costume, often with doubles.
6. **Reference images** — if the user has photos of actors/characters, bind each to one character by name and
   say what to take (face, hair, outfit) and what not (background, pose).

## Output
`03_costume.md` — character look cards · wardrobe state table · NOTES.

## Table-read checklist
- Is each character's look card used word for word in every card where they appear?
- Do wardrobe states change only where the table says?
- Could two characters be confused at wide-shot distance?
