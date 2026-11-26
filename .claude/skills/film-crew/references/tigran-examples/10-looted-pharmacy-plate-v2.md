# 10: Looted pharmacy, revised plate (iteration of 09)

Shared by Tigran on 2026-11-26 right after 09. It is the same plate, revised, so the useful lesson is **how a prompt gets iterated**. The prompt is verbatim below.

```text
Cinematic film still. Interior of a thoroughly looted pharmacy inside an abandoned small-town clinic, late autumn day. No people, environment plate.

COMPOSITION: 35mm, camera at chest height just inside the pharmacy entrance, looking in along the length of the room; a heavy roll-down steel security grate fills the foreground, pulled down to the floor but levered and bent upward at one corner to leave a forced gap roughly a metre wide — the camera looks through and past this gap into the room; beyond it, two long parallel shelving units run away from the camera with a narrow aisle between them; a dispensing counter along the right wall; the back wall at the far end carrying a single small high window; low ceiling with a suspended acoustic grid.

THE FORCED GRATE: galvanised steel roll-down shutter, slats buckled and torn at the lower left corner where a bar has been worked under and levered repeatedly, the metal peeled back and the edges bright and scratched where paint and oxide have been scraped away — the only recently disturbed surface in the building; the floor guide rail bent out of true; the padlock hasp twisted and hanging.

THE LOOTING — heavy and specific: this room was stripped early and hard; three quarters of the shelf space is completely bare, showing only clean rectangles and rings in the dust where stock stood; plastic divider bins pulled out and dumped on the floor in a scatter down the aisle, several cracked; one shelf deck collapsed at one end and hanging; the near shelf unit pulled a foot away from the wall and leaning slightly, its top shelf emptied by sweeping an arm along it; cardboard cartons torn open along their seams and discarded flat on the floor, their contents long gone; empty blister packs everywhere, their foil popped through, drifted into the corners; old scuffed footprints in the spilled powder across the vinyl, set hard under a year of dust.

WHAT IS LEFT — the residue nobody wanted, varied in container and colour: a cluster of squeeze tubes of ointment and antifungal cream, their printed cartons in faded teal, mustard and dull red; rows of small plastic eye-drop bottles in a tipped bin; brown glass bottles of cough syrup, several on their sides, one with a dried dark ring beneath it; large white HDPE tubs of generic vitamins and antacid tablets; a shelf of laxatives and antihistamines in cardboard boxes printed in washed-out blue and green; small glass ampoules in a moulded plastic tray, half the wells empty; a stack of saline bottles in clear plastic; boxes of gauze and surgical tape in plain buff card; a row of unlabelled amber prescription vials with white child-proof caps, all of them empty, upended; obscure brand names on everything; a shelf of baby formula tins, dented, two of them rolled onto the floor.

WHAT IS GONE: the amber pharmacy vials that held anything useful, swept entirely; the antibiotic and painkiller sections reduced to bare board; the refrigerated stock; every section that mattered.

THE COUNTER: a laminate dispensing counter along the right wall with a dead computer terminal, a label printer with a curl of blank labels hanging, a pill counting tray and spatula, a tipped basket; behind it a wall-mounted hanging rack of white paper prescription bags filed alphabetically by surname, each stapled shut with a printed label, perhaps forty of them still hanging exactly where they were left, never collected, grey with dust — the only orderly thing in the room.

THE REST: a glass-fronted refrigerator against the far wall, dark and dead, door standing open, racks stripped bare; a narcotics safe set into the wall below the counter, its door hanging open and interior empty, the surrounding wall gouged and splintered where it was attacked with a tool; a tipped stool; a waste bin overflowing with crushed packaging; hand-written paper notices taped to the shelf ends, curled; thick even undisturbed dust over everything except the forced grate.

THE LIGHT: two weak sources only — a small high window in the back wall, frosted and fitted with security bars, throwing a soft grey slab down the far end of the aisle and across the upper shelves; and grey corridor daylight leaking through the forced gap in the grate behind the camera, raking low across the floor for a couple of metres and dying; the middle of the room sits in deep cool shadow that still holds detail; shelf tops and ceiling dark; no artificial light, no emergency lighting, no flashlight.

THE GRADE: cold and desaturated; both sources read grey-blue and neutral; shadows cool and open, nothing crushed to pure black; the packaging colours present but heavily muted by the cold light and the dust film — teals going grey-green, reds going brick-brown, yellows going khaki; low to moderate contrast.

PALETTE: 40% cold grey-blue — the two light sources, the suspended dust, the lit shelf faces; 30% deep cool shadow — the middle of the room, shelf tops, ceiling; 30% dusty muted packaging — brown glass, off-white tubs, faded teal, mustard, brick-red and washed blue cartons, galvanised steel.

LIGHTING restated: a barred high window at the far end and corridor light through the forced grate behind camera as the only sources; no artificial light, no practical, no fill; the window slab the brightest value, the ceiling and shelf tops the darkest.

Focus: deep focus, the torn grate edge in the foreground, the dumped bins and spilled packaging on the floor, the remaining stock and the far window all sharp and readable; anamorphic elongated vertical oval bokeh on the dust motes crossing the window slab.

Shot on real 35mm film, tungsten-balanced 500-speed colour negative film, visible grain, natural halation on the window slab; anamorphic 35mm lens, rectilinear, straight verticals; suspended dust; tech tail palette: cold grey-blue 40%, deep cool shadow 30%, dusty muted packaging 30%; gritty documentary realism, available light only; absolutely no CGI, no render look, no colour grade, no dramatic lighting, no teal-and-orange, no video-game styling, no blood, no bodies. Clean environment plate, no people, no flashlight in frame. No text overlay, no watermark. Aspect ratio 2.39:1.
```

## What changed from 09, and why it matters (Cloud, 2026-11-26)

**Kept identical:** composition, the forced grate, the counter and the bags, the light, the focus and the stock. The revision touches only what the first version left to the model's defaults. That is the right way to iterate: change one layer and freeze the rest.

**Changed or added:**
1. **"THE LOOTING — heavy and specific."** v1 said "heavily picked over". v2 says how:
   - three quarters bare;
   - bins dumped down the aisle, some cracked;
   - one shelf deck collapsed;
   - the near unit pulled from the wall;
   - the top shelf "emptied by sweeping an arm along it";
   - cartons torn along their seams;
   - popped blister packs drifted into corners.
   
   Each one is a verb with a visible result. A "looted" room left to the model's default looks tidy; this does not.
2. **"WHAT IS LEFT — the residue nobody wanted."** Ointments, eye drops, cough syrup, laxatives, vitamins, gauze, empty vials. The leftovers follow scarcity logic: looters take antibiotics and painkillers and leave the rest. The plate now shows what people needed by showing what they did not take.
3. **"WHAT IS GONE."** Absence is designed as a block of its own: the antibiotic and painkiller sections are bare board.
4. **Variety against AI repetition.** v1 had rows of identical white bottles, an invitation to cloned objects. v2 varies container (tubes, brown glass, HDPE tubs, ampoules, tins) and colour.
5. **Colour drift under the grade.** "teals going grey-green, reds going brick-brown, yellows going khaki". The packaging keeps its colour but stays inside the cold palette. The palette moves from 25% off-white to 30% "dusty muted packaging".
6. **Timeline fixed.** "Old scuffed footprints in the spilled powder… set hard under a year of dust" settles the v1 conflict between undisturbed dust and footprints, and dates the looting.
7. **Contrast note.** The bags behind the counter are "the only orderly thing in the room".
8. **"Obscure brand names on everything"** keeps real brands out of the frame.

**Still open from 09:**
- "THE GRADE" against "no colour grade";
- deep focus against bokeh;
- "tech tail palette" and the palette written twice;
- in-scene text;
- the aspect ratio in the prompt.

**Iteration lesson for our skills:**
- When a plate or shot comes back generic, don't rewrite it. Find the line the model filled with its default ("looted", "stocked", "messy"). Replace it with concrete verbs and visible results, plus the logic behind them (what is left, what is gone, and why).
- Add variety wherever the model is likely to clone objects.
- Freeze everything that already worked.
