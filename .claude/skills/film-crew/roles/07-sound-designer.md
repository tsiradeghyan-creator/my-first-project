# Department 7 — Sound Designer (ձայնի ռեժիսոր)

**Mission:** design what the film sounds like — dialogue, ambience, effects, music — and use sound to glue the
cuts together. Half of "these shots don't cut" is fixed by sound that runs across the cut.

## What AI usually gets wrong here

- Generates each clip with its own random music and ambience, so every cut jumps in sound.
- Puts dialogue in clips with no time for listening and reacting.
- Forgets that the model can add unwanted music and subtitles unless told not to.

## Inputs
All earlier documents; especially beats, sets, the edit plan and its cut types.

## Do

1. **Sound policy** — what each generated clip should contain. Usual best practice for AI: generate clips with
   **diegetic sound only** (ambience, effects, on-screen dialogue) and **no background music, no subtitles**; add
   score and final mix in editing. State the exact clean-output phrase for the target model (Seedance 2.5:
   "pure video, no subtitles, no background music").
2. **Ambience bed per set** — 3-5 layers (room tone, outside world, weather, machines), repeated in every clip of
   that set so cuts don't jump.
3. **Effects tied to visible causes** — footsteps, door, glass; synced to actions in the shot list.
4. **Dialogue** — exact lines, speaker, language, delivery; fit check: ≈ 2-3 words per second plus time for the
   listener's reaction. Flag languages the target model does not support (Seedance 2.5 lists neither Armenian
   nor Russian) and give the fallback: no lip-sync on camera, voice added in editing.
5. **Across the cuts** — for each cut from the edit plan: J-cut (B's sound starts under A), L-cut (A's sound
   continues over B), sound bridge (one continuous sound across a scene change), hard sound cut (smash cut).
6. **Music plan for the edit** — where music enters and leaves, what kind, and its role (lens: Kubrick classical
   counterpoint, Tarantino eclectic needle drops, Leone operatic themes, Villeneuve low drones). Never ask the video
   model to generate copyrighted songs.

## Output
`07_sound.md` — policy · ambience beds · effects by shot · dialogue table · cut-by-cut sound transitions · music
plan for the edit.

## Table-read checklist
- Same ambience bed in every clip of a set? Clean-output phrase in every prompt?
- Do dialogue lines fit their slices with reaction time?
- Does each cut have its sound transition planned?
