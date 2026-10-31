# Generation strategy — turning the plan into clips that cut

## Principle: keyframe first

For every shot, the start frame (and, when the cut needs it, the end frame) is designed as a still image first.
The video model mostly animates what the still already fixed: identity, wardrobe, set, light and composition.
Fix the still before spending video generations. Keyframe prompts are plain English stills: set description +
character look card + composition + lens + light + palette, no motion verbs.

## Chaining methods (chosen per cut by the Editor)

| Method | Use when | How |
|---|---|---|
| **Same call, multi-shot** | Short continuous action with a cut inside, same set, same light, ≤ model max duration | One video prompt with timed slices and the cut written in the slice ("[4-8s] cut to a close-up of…"). Safest for continuity. |
| **First-frame chain** | Continuous action across separate generations | Take the last frame of clip A (export it) and use it as the first frame of clip B (First/Last Frames mode or image-to-video). |
| **First + last frame** | B must land exactly on a designed frame | Provide both keyframes; the model fills the motion. |
| **Extension** | The same shot simply continues | Extend clip A; the prompt describes only the new part. |
| **Bridge / seamless transition** | Two finished clips need a designed transition between them | Seedance 2.5 seamless transition: "connect @Video 1 and @Video 2 without modifying them" + the bridge action. |
| **Independent + hard cut** | Different set or deliberate contrast | Generate separately; continuity comes from locked text blocks and sound. |

## Locked text blocks

Write each block once and paste it verbatim into every prompt that needs it:
`[SET: <name>]` from the Production Designer · `[LOOK: <character>]` from the Costume Designer ·
`[LIGHT: <scene>]` from the DP · `[SOUND BED: <set>]` from the Sound Designer. Changing one word changes the shot.

## Model adapters

### Seedance 2.5 (default) — follow `seedance-25-director` if available
- Per call: 4-30 s (Long Video 30-180 s; extension to 60 s total). Output 480p/720p.
- References: up to 30 images, 10 videos (≤ 30 s total), 10 audio; declare each `@Image N` with its role, in
  upload order; bind each character to one image by name.
- Prompt order: asset declaration → one-line summary → timed plot `[0-4s] …` (➕ picture, camera, action,
  dialogue, sound; ➖ local bans) → global supplement (globals + bans).
- Time slices ≥ 3 s; plain seconds; one main action + one camera move per slice.
- Clean output: "pure video, no subtitles, no background music". Score in the edit.
- Dialogue languages: Chinese, English, Spanish, Indonesian, Malay, Thai, Arabic, Portuguese, Vietnamese,
  Japanese, Korean. Armenian/Russian not listed → test or add voice in post.
- Transitions inside a call: use the official 3-line transition template (natural shot switch, fade, dissolve,
  flash, wipe, mask, similar-object, motion, motion relay, zoom, ink).

### Other models (when the user names one)
- Kling, Veo, Wan, Hailuo, Runway, Sora-class: keep the same plan; adapt length per call to the model's limit,
  move references into that model's reference slots, and write one shot per call when the model handles cuts
  poorly. Use `cinema-worldbuilder-pro-2.0` for model-specific syntax. Verify current limits before promising them.

## QC per generation unit (before moving on)

1. Identity and wardrobe match the look cards. 2. Set geography matches the floor plan. 3. Light side and colour
match the light plan. 4. The last frame matches the outgoing handoff contract. 5. Sound: ambience bed present, no
music/subtitles if banned. If a unit fails three times, change the shot design (simplify the move, split the
action, use an insert), not just the wording.
