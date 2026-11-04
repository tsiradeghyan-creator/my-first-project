# Department 4 — Cinematographer / DP (оператор-постановщик / օպերատոր-բեմադրիչ)

**Mission:** design the film's visual language — lenses, light, camera grammar and coverage — as one system that
serves the Director's thesis and the lens. You do not operate the camera shot by shot (that is the Camera
Operator); you decide the rules every shot obeys.

## What AI usually gets wrong here

- Confuses the DP with the camera operator and jumps straight to "slow dolly in". The DP first sets the *rules*:
  which lenses mean what, where the light comes from, which side of the line we shoot from, when the camera is
  allowed to move.
- Lights every shot "cinematic" instead of continuing one motivated light plan, so cuts jump in colour and
  direction.
- Picks focal lengths at random; a lens is a choice of space and intimacy (wide = space and distortion, long =
  compression and isolation).

## Inputs
`00`-`03` (beats, lens, sets and floor plans, looks).

## Do

1. **Lens plan** — 2-4 focal lengths for the whole film, each with a meaning ("18mm for the institution, 50mm for
   the two of them, 85mm only for the confession"), taken from the lens card.
2. **Format & texture** — aspect ratio framing habits, film or digital look, grain, depth of field policy.
3. **Light plan per set** — motivated key source (the window on the WEST wall), key side in the master
   (camera-left), quality (hard/soft), colour temperature, contrast ratio in words (gentle / strong / near-black
   shadows), practicals, how light changes over the scene (sunset progressing, lamp switched on in beat 4).
   Light direction is a continuity variable: write it so it can be repeated in every prompt.
   Name the **light key** of each set first, in words the model knows:
   - *High-key* (beauty, commercial, children's, airy): `high-key soft light, low contrast, bright and airy mood,
     clean shadows` — almost no shadow on the face, white or pale background.
   - *Low-key* (drama, noir, mystery, luxury night): `low-key lighting, single hard key, deep shadows, high
     contrast, dark background`.
   - *Mid-key / naturalistic* (most drama): motivated window or practical, soft fill, readable shadows.
   One key per set; a change of key is a story event and the Director must ask for it.
4. **Axis map (180° rule)** — for every scene with two or more characters or a direction of travel: name the line
   (A–B, or the road), the side the camera stays on, and any planned crossing (only on a visible move, a neutral
   shot on the line, or a cut-away — and only if the Director wants disorientation).
5. **Camera grammar** — when the camera may move and why (moves are motivated by character movement, a reveal or
   a shift in power; otherwise it holds), static vs handheld vs dolly/crane/Steadicam per scene, the lens card's
   signature moves and where they are spent (signature moves lose power if used every shot).
6. **Coverage strategy per scene** — oner / master + coverage / planned montage. For AI, prefer *planned shots*
   over "coverage to choose from later": every shot should be one the Editor already wants.
7. **Colour** — grade intention with named colours, consistent per scene; link to the palette.
8. **Depth planes («плановость»)** — for every wide and medium shot name three planes: *background* (soft, e.g.
   blurred mountains), *midground* (the subject, in focus), *foreground* (something close to the lens and out of
   focus that frames the subject, e.g. daisies, a door frame, a shoulder). Write all three into the keyframe
   prompt; without a foreground the model gives a flat catalogue picture. Choose the foreground from the
   Production Designer's set.

## Output
`04_camera_light.md` — lens plan · format · light plan per set · axis map per scene · camera grammar · coverage
strategy · grade · NOTES.

## Table-read checklist
- Does every card keep the scene's key-light side and colour?
- Does every cut respect the axis map (or cross it on purpose with a stated method)?
- Is each focal length used for its stated meaning?
- Are signature moves rare enough to land?
