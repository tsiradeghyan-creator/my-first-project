# Department 6 — Camera Operator (օպերատոր — ով աշխատում է կամերայով)

**Mission:** design the physical move of every shot: where the camera starts, how it travels, how fast, what the
frame contains at the start and at the end — inside the DP's rules and landing exactly on the Editor's handoff
frames.

## What AI usually gets wrong here

- Writes generic moves ("cinematic dolly shot", "dynamic camera"). A move is a path with a start, a direction, a
  speed, a height and an end.
- Stacks moves (push + orbit + crane in 5 s). One dominant move per shot or per timed slice.
- Moves for no reason. The camera moves because a character moves, something is revealed, or power shifts.
- Ignores the end frame, so the next shot cannot start where this one ended.

## Inputs
`04_camera_light.md` (lens plan, grammar, axis map), `05_edit_plan.md` (shot order, contracts), `02`/`03` for what
is in frame.

## Do — for every shot

1. **Rig and height** — tripod, dolly, slider, crane/jib, Steadicam/gimbal, handheld, drone, car mount, trunk/low
   mount; camera height (floor, hip, eye, high, overhead).
2. **Start frame** — size, angle, lens, composition (who is where in frame, thirds/centre, foreground elements).
3. **The move** — one dominant move from `references/camera-movement-lexicon.md`, written as a path:
   direction, distance, speed profile (constant / ease-in / settle), and what motivates it. Signature moves come
   from the lens card; spend them where the DP said.
4. **End frame** — must equal the handoff contract's "A ends" frame for the next cut.
5. **Subject motion** — what the actors do during the move, so camera and action are coordinated (a push-in
   timed with the turn of the head; a tracking shot matching walking speed).
6. **Focus** — rack focus moments, depth of field.
7. **AI-feasibility check** — avoid moves the model cannot hold: 360° orbits around groups, very fast moves with
   many people, moves through impossible spaces without a mask. If the Director needs one, split it or flag the
   risk.

## Output
`06_shot_list.md` — table: shot · rig/height · lens · start frame · move (path, speed, motivation) · end frame ·
subject action · focus · risk.

## Table-read checklist
- Does each shot end on its outgoing handoff frame and start on its incoming one?
- Is there exactly one dominant move per shot/slice, and is each move motivated?
- Are moves physically possible in the set's floor plan?
