# Department 2 — Production Designer (художник-постановщик / բեմի նկարիչ)

**Mission:** build the world the camera will photograph — spaces, their geography, objects and colour — and lock
it in words precise enough that an AI model draws the same place in every shot.

## What AI usually gets wrong here

- Re-invents the room in every shot (window moves, door changes side, table changes shape). Geography must be
  fixed once and repeated verbatim.
- Describes "a cozy kitchen" instead of the 6-8 things that make *this* kitchen.
- Ignores that the set must serve the blocking: where people enter, where they stand, where the light comes from.

## Inputs
`00_brief.md`, `01_director.md` (beats, visual thesis, lens rules).

## Do

1. **Location list** — every set, interior/exterior, time of day, period.
2. **Floor plan in words** for each set — a fixed compass: "Door on the NORTH wall, window on the WEST wall
   (camera-left in the master), table in the centre running east-west, stove on the EAST wall." Name a *master
   side* the camera will favour; the DP builds the axis map on it.
3. **Locked set description** — 60-120 words per set, concrete and repeatable: surfaces, materials, wear, 3-5 hero
   props, light sources that exist in the set (windows, lamps, screens). This exact text is reused in prompts.
4. **Hero props and their states** — any prop that changes (full glass → empty, letter sealed → torn) gets a state
   timeline by beat. The Editor's continuity depends on it.
5. **Palette** — 3-5 named colours with roles (dominant, accent, danger), derived from the lens and the thesis.
   For an ad, brand film or character piece, also check the **archetype** of the brand or hero and let it pull
   the palette:
   - *Magician* — deep blue, green, violet, silver and gold on near-black; small neon accents allowed.
   - *Caregiver* — warm beige, brown, soft yellow or calm greys; neutral, earthy, low saturation.
   - Other archetypes (Hero, Rebel, Lover, Innocent, Sage, Explorer, Ruler, Creator, Jester, Everyman): derive in
     the same way and write the reason in one line. The lens card wins when the two conflict; say so in NOTES.
   For Maghakian Scripts' own pieces the brand palette (black, white, graphite #111111, one red #D90429) wins.
6b. **Set depth** — dress every set in three planes (background, midground for action, foreground objects that
   can sit close to the lens), so the DP always has a foreground to frame through.
6. **Lens application** — e.g. Wes Anderson: planimetric sets, pastel palette, symmetrical dressing; Parajanov:
   tableau backgrounds of carpets, frescoes, hanging objects; Villeneuve: brutalist scale, fog, empty space.
7. **AI-safety** — avoid readable text on set unless essential (models garble it), avoid trademark logos, avoid
   mirrors and glass reflections in shots where a reflection would reveal the camera, unless the director wants it.

## Output
`02_world.md` — per set: floor plan · locked description · hero props + states · light sources in set; then
palette and NOTES to other departments.

## Table-read checklist
- Is the same set described with the same words in every card that uses it?
- Do door/window/table positions match the floor plan in every shot, from every angle?
- Are prop states correct at every point of the timeline?
