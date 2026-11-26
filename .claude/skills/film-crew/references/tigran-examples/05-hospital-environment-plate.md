# 05: Abandoned hospital forecourt, environment plate (still image)

Shared by Tigran on 2026-11-26. This is a still-image prompt for the world reference of the John series; its viewpoint is exactly the one prompt 04 bans for video ("no three-quarter view from the left corner"). The prompt is verbatim below.

```text
Cinematic film still. The main entrance and the wide forecourt of a large abandoned American hospital, on an overcast morning, months after everyone left; quiet, vast, desolate.

Three-quarter angle, camera set at the far left corner of the forecourt, looking diagonally across the whole empty forecourt toward the hospital entrance, lens at chest height, level.

In frame, foreground to background: in the near foreground, at the bottom of the frame, the edge of a shallow puddle on the cracked asphalt and a tuft of dry weeds pushing up through a crack. Then the forecourt opens out wide across the lower half of the frame: a vast, empty expanse of cracked grey asphalt, the faded white lines of the parking bays barely visible, weeds and dry grass growing along the cracks in long uneven lines, scattered dead leaves, a few shallow puddles reflecting the grey sky, a few shards of broken glass. In the midground, on the left third of the frame, the abandoned white box ambulance, parked crooked across the drive near the entrance, its paint dulled with dust and grime, a faded orange stripe along its side with no lettering, two flat tyres, its rear doors hanging half open; near it, a toppled wheelchair on its side by the kerb. Beyond, filling the upper and right part of the frame, the hospital: a large four-storey building of concrete and pale brick, long rows of identical windows across every floor, many panes cracked or dark, grime streaks running down the concrete beneath them. At ground level, a wide flat concrete canopy on square columns runs out over the drive-through entrance, and under it a row of tall glass sliding doors, the central pair jammed half open, a dark gap between them, the lobby inside lost in shadow. A long blank weathered sign panel runs along the edge of the canopy, its letters long gone. In the background, beyond the end of the building, a line of bare trees fading into a light haze.

Palette: 60% muted grey and dirty white (sky, concrete, asphalt, ambulance), 30% faded olive and brown (weeds, dry grass, leaves, brick), 10% faded orange (the stripe on the ambulance).

Lighting: soft, flat, diffused daylight from a fully overcast sky, cool neutral colour temperature around 6000K, coming from above and slightly behind the hospital; low contrast, soft shadows under the canopy and the ambulance, the dark gap between the sliding doors the deepest black in the frame. The brightest area is the pale band of overcast sky just above the hospital's roofline.

Focus locked on the ambulance, camera about 10 m from it, lens wide open. The puddle edge and the tuft of weeds at the bottom of the frame melt into creamy out-of-focus; the forecourt stays readable from the ambulance outward; the hospital façade softens gently; the trees behind dissolve into the haze. 84° diagonal field of view, anamorphic rectilinear character. Anamorphic bokeh with elongated vertical oval highlights on the puddles and the shards of broken glass across the forecourt, and a long, faint, pale blue horizontal streak flare off the bright band of overcast sky above the roofline.

Shot on real 35mm film, daylight-balanced 250-speed colour negative film, fine grain; anamorphic 24mm lens with subtle horizontal flare and gentle highlight bloom; rule-of-thirds composition; natural true-to-life color; realistic environment physics — light haze in the air, dead leaves resting in still puddles; gritty documentary film realism, indistinguishable from a real photograph, absolutely no CGI or render look. No cloned or duplicated elements. Clean environment plate, no characters. No text, no watermark, no logo. Aspect ratio 2.39:1.
```

## What is new (Cloud, 2026-11-26)

1. **A plate-first workflow.** The world is built first as a still reference. The video prompts then attach it as a reference and ban its own viewpoint, so every video shot finds a new angle in the same world. This is a full pipeline: world plate, then character and prop references, then shots.
2. **Still-image anatomy:**
   - one-line logline;
   - an exact camera position (corner, diagonal, chest height, level);
   - an inventory from foreground to background, using three depth planes;
   - a palette in proportions (60 / 30 / 10, the classic design rule);
   - lighting with a Kelvin value, a direction, and named extremes ("the deepest black in the frame", "the brightest area");
   - a focus plan: what is sharp, the distance, and how sharpness falls off plane by plane;
   - a lens character with its artefacts (vertical oval anamorphic bokeh, a pale blue horizontal streak flare);
   - an anti-artefact line ("no cloned or duplicated elements").
3. **Storytelling props.** A toppled wheelchair, rear doors hanging open, a blank sign panel "its letters long gone": each one tells "everyone left" without a person in frame.

**Weak spots to watch:**
- **The plate does not match prompt 04.** This plate has one upright ambulance and a blank sign. Prompt 04 demands three ambulances, one overturned, and the sign CEDAR RIDGE MEMORIAL CLINIC, all "matching the reference exactly". If 04 used this plate, the model has to choose between the reference and the text, and that conflict usually produces drift. Either re-make the plate with what the shots need, or write 04 to add the extras ("add two more ambulances…") instead of claiming they are in the reference.
- **Optics vs physics.** A 24 mm lens wide open, focused at 10 m, keeps the façade fairly sharp in reality. The prompt's soft façade is a look, not optics. Models follow the words, so this is fine, but don't copy it into a DP plan as fact.
- **The aspect ratio is written into the prompt text.** Our banana-pro rule keeps ratios in the UI setting, because some engines print or misread them. Keep it out of the prompt unless the target engine reads it.

**Pattern so far (01–05):** everything from 01–04, plus a plate-first world reference, depth-plane inventories, palette proportions, lighting extremes and a focus falloff plan for stills. The text of the shots and the plate must stay consistent.
