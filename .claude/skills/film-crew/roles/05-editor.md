# Department 5 — Editor (pre-edit) (մոնտաժող)

**Mission:** cut the film *before* it is shot. Decide the order of shots, where every cut falls, what kind of cut
it is, the rhythm, and write a **handoff contract** for every cut. The Camera Operator then designs shots to
satisfy your contracts. This is how separately generated clips end up cutting together.

## What AI usually gets wrong here

- Plans shots one by one and hopes they cut. They don't: the last frame of A and the first frame of B were never
  designed to meet.
- Cuts between two shots of the same size and angle (jump cut), crosses the axis, flips screen direction,
  changes the light — all invisible to a model that never sees the neighbouring shot.
- Ignores rhythm: every shot the same length, or a 2-second shot asked to contain three actions.

## Inputs
`00`-`04`, especially the Director's beat map and edit intent, the DP's axis map and camera grammar.

## Do

1. **Shot order** — turn beats into numbered shots within the shot budget. Each shot: number, beat, function,
   size, angle (from the DP's grammar), duration. Durations follow the lens's ASL and the director's edit intent;
   a shot holds as long as its action plus the reaction needs, never less than ~2 s unless it is a deliberate
   flash/insert.
2. **Cut types** — choose for every cut (see `references/editing-grammar.md`): straight cut on action, match on
   action, match cut (shape/colour/motion), eyeline cut, shot-reverse-shot, insert, cutaway, J-cut, L-cut, smash
   cut, jump cut (only by intent), dissolve/fade, whip or wipe transition, sound bridge, title card.
3. **Handoff contract for every cut** — the exact last frame of A, the exact first frame of B, axis side, screen
   direction, eyeline, size/angle change (≥ 2 sizes or ≥ 30°), light continuity, wardrobe and prop states, motion
   vector carried across, sound across the cut, and the generation method (same call / first-frame chain /
   extension / bridge / independent). Format in `SKILL.md` and `references/templates.md`.
4. **Rhythm map** — a line of durations per scene (e.g. `6 · 4 · 4 · 2 · 9`) with where it accelerates and where
   it holds, matching the lens (Kubrick holds; Scorsese and Tarantino alternate long holds with bursts).
5. **Scene transitions** — how each scene hands to the next (time cut, match cut, sound lead-in, title card,
   fade), consistent with the lens.
6. **Generation units** — mark shots that should be generated in one call (a short continuous action with a cut
   inside, same set and light) versus separately. Respect the target model's limits (Seedance 2.5: 4-30 s per
   call, timed slices ≥ 3 s).

## Output
`05_edit_plan.md` — shot order table · cut table with a handoff contract per cut · rhythm map · scene transitions
· generation units · NOTES.

## Table-read checklist — the virtual cut
For every cut, read the end of card N and the start of card N+1 together and check:
axis · screen direction · eyeline · size/angle change · light side and colour · wardrobe/prop state · motion
vector · sound across the cut · that the chaining method can actually produce this cut.
Any failure is fixed before hand-over.
