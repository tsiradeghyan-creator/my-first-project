# Seedance 2.5 — prompt formulas by mode

Everything here is from `official-guide-lark.md` ("3. Prompt word suggestions" and the Highlights) unless marked.
Official example prompts for each section: `examples-index.md`.

## Contents
1. Universal backbone
2. Realistic human formula
3. `timeline-30` — the three-module 30-second structure
4. `long` — 30-180 s
5. `extend`
6. `edit` — Smart Edit / Edit with marks / Edit Video
7. `clay` — Clay Renderer (coarse / fine)
8. `bridge` — seamless transition between two videos
9. `grid` — multi-grid storyboard
10. Capabilities: BGM/subtitle removal, voice reference, multi-person, green screen, creative transfer,
    perspective change, object removal, realism boosters

---

## 1. Universal backbone

```
Complete prompt = [asset declaration] + [one-line summary] + [plot] + [global supplement]
```

- **Asset declaration** — every file by upload order + its job (character / voice / motion / scene / prop).
  No uploaded image, video or audio may be left unmentioned.
- **One-line summary** — subject + location + event + theme/style + special camera treatment.
- **Plot** — by timeline or storyline. Per slice:
  ➕ positive: picture content + camera movement + action + dialogue + sound effects;
  ➖ reverse: what must not appear in this slice ("no subtitles", "no BGM").
- **Global supplement (end)** — restate what must hold for the whole video (camera position, environment features,
  overall sound/atmosphere, lighting) and the global bans (subtitles, background music…).

Re-@ the same asset where it matters again later — the guide says repeated mentions raise accuracy.

Timestamps: put the interval in front of the line it governs — `[0-5s]`, `[5-12s]` (the guide also shows
`[00.0-05]` and `0-3s`). Use one convention per prompt. A slice is a time budget, not an edit point.

Minimal prompt shape for small requests (ByteDance Prompt Guide, via smixs — secondary):

```
<Subject> performs <primary action> in <scene>. The visuals feature <style>.
Use <shot size / angle / camera move>. Audio includes <dialogue, ambience, effects or music>.
```

## 2. Realistic human formula (also works for animated characters)

```
Character = [age/ethnicity] + [skin tone/skin texture] + [facial details] + [eyes/soul]
          + [hairstyle/hair colour] + [clothing/fabric] + [build/emotion/temperament] + [other, if any]
```

| Part | Sub-formula | Purpose |
| --- | --- | --- |
| Age/ethnicity | exact age + nationality/ethnicity + style adjective + face-shape noun | sets the character tone |
| Skin | warm/cool tone + skin-tone noun + texture adjective + **"retaining real fine pores and skin texture"** (optionally freckles, blemishes) | kills plastic AI skin |
| Facial details | at least 3-4 of: eye shape, brow bone, nose bridge, lips, jaw/bone structure | recognisability |
| Eyes/soul | eye adjective + what the gaze conveys (metaphor) + underlying emotion | emotion |
| Hair | exact colour + condition/texture + hairstyle noun + interaction with environment (wind, mess) | life, atmosphere |
| Clothing | cut/pattern + colour + garment noun + fabric and wear state + how it is worn | style, backstory |
| Build/temperament | frame/shoulders + composition/shot + action/gaze + atmosphere word (drop shot/action if the plot already gives them) | composition, story |

Realism boosters from the guide: "native skin texture", "hair roots distinct". For animated characters keep the
structure and switch the texture register.

## 3. `timeline-30` — three modules (official structure for dramatic 30 s work)

```
<One sentence that states the tone of the whole video, e.g. "29-second one-take: a farewell by the river">

[Module 1 — Reference layer]            (skip if nothing is uploaded)
Based on the uploaded <type>, strictly keep <face/features> of @Image 1 consistent,
keep the <composition / white model / spatial relations> of @Image 2, strictly lock character positions.

[Module 2 — Global settings: worldview + anti-collapse]
Base environment & texture: <time> + <place> + <atmosphere> + emphasise extreme real physical texture.
Visual style: <cinematic / realistic / 2D…> + <depth of field> + <lighting method>.
Camera language: <shot size / viewpoint> + <details>.
Character styling: <section 2 formula, or "@Image N" + what it shows>.
  (for objects: quantity + colour + shape/design + item noun + material/wear + signature feature)
Performance core: <what the finished film must get right>.
Prohibited: <sound> + <subtitles> + <behaviour> + <the exact places this scene collapses>.

[Module 3 — Timestamped storyboard]
[start-end s] <phase name>
  Physical directives: scene + composition + precise actions/expressions.
  Emotion / camera intent: one line telling the model WHY (the subtext) or how the camera schedules it.
…
```

- Prohibition lists are specific: the official farewell example bans exaggerated crying, fast cuts, large body
  movements, extra dialogue, BGM, runny nose, tears dropping too early.
- For a 30 s piece with cuts instead of a one-take, add the cut/transition wording from `transitions.md` at each cut.

## 4. `long` — 30-180 s in one pass

```
Complete prompt = [global parameters] + [asset declaration] + [one-line summary] + [plot] + [global supplement]
```

- **Global parameters:** restate the total duration and the ratio at the top ("Video duration 1 minute, aspect
  ratio 16:9, cinematic realistic picture quality…") even though they are set in the UI.
- Write the plot as a timeline (`0-6 seconds: …`) or as a story. For long pieces, split the story into stages,
  each with one main change and a visible end state that the next stage starts from (practitioner method —
  smixs; matches the guide's examples).
- Slow continuous camera work (long push-ins, orbits, fly-throughs) is a stated strength of Long Video.

## 5. `extend`

Rules:
- Source must be < 30 s. Per step +4-30 s; repeat while the result is ≤ 30 s; maximum total 60 s.
- The prompt describes **only the new part**; the original seconds stay untouched.
- State placement explicitly: "after the last frame" (the Extend button's behaviour) or "before the first frame".
  The guide lists both forward and backward extension; if the user's wording is ambiguous, ask once.
- Extra images/video/audio may be attached to an extension.

Templates:

```
Reference the content of @Video 1 and extend it by <N> s <after its last frame>.
Require a natural extension: smooth, natural action continuity, no rigid cuts, no objects appearing out of thin air.
<What happens in the new N seconds — action, camera, sound — continuing from the last frame.>
```

For an extension that **cuts or transitions** to something new, add a cut setting:

```
Cut setting = [transition type guide] + [basic constraints] + [cut logic]
[Transition type] Use a "<transition name>" at the cut point (no rigid cut, no objects appearing out of thin air).
[Basic constraints] Keep the camera's breathing and duration coordinated. Shot A shows <…>, then naturally
  transitions to Shot B, <…>.
[Cut logic] Switch scenes naturally<, and the shot size changes from close-up to medium shot>.
```

Or let the model choose: "Choose the transition that best fits this film from: natural shot switch / mask
transition / ink transition / similar-object transition."

## 6. `edit` — Smart Edit, Edit with marks, Edit Video

Write the change as A → B, with time:

```
[Annotation tool & orientation] + [target object] + [action/change] + [effective time]
```

- **Annotation tool & orientation** (Edit with marks / Edit Video only): name the tool and whether the change is
  inside or outside it — "inside the red box", "where the red arrow points", "at the anchor point", "to the left of
  the red line". Omit for Smart Edit.
- **Target:** what exactly changes — "the boy's jeans", "the dead tree in the background".
- **Change verbs:** edit / add / delete-remove / modify-replace-change to.
- **Effective time:** whole clip ("throughout the 15 s, keep consistent"), a window ("only between 5 s and 8 s"), or
  a ramp ("gradually appears from 3 s"). Match the time label Dreamina adds after *Add to Input Box*.
- Always list what must stay unchanged (people, motion, camera, background, audio).
- Extra reference images: 1-5 best. Source video ≤ 20 s for stability.

Official patterns: "Modify everything from 0 to 8 seconds of the whole video. Change the whale to a white dragon.
Remove the BGM." · "Change all the white backgrounds into a green screen background from 0 to 5 s. Remove the sound,
keep it muted." · "Remove the black sunglasses from the girl's face in @Video 1, add a white baseball cap, add a light
pink water bottle to her right hand; otherwise keep the video the same as the original."

## 7. `clay` — Clay Renderer

Coarse models (simple spheres/cylinders/boxes standing in for people and objects) currently work better than fine.

**Coarse white model — the clay video is only the motion skeleton:**

```
[Reference statement] Refer to the {camera movement | action | movement line | light changes | positions |
  music and sound | rhythm} of @Video 1.
[Mapping] Replace the {colour/shape} model in @Video 1 with {character} from @Image X, the {colour/shape} model
  with {character} from @Image Y, the {colour/shape} model with {prop/scene} from @Image Z.
[Plot details] chronological actions, expressions, lines, light changes.
[Scene] text, or "use the {scene} in @Image W as the background".
[Wrap-up] overall style, image quality, consistency constraints, audio handling.
```
If a model has limbs or wings, write the full limb action sequence, or better, do not upload limbed/winged models.

**Fine white model — the scene is fully modelled; only materials, light and style change:**

```
[Render command] Render the white-model animation of @Video 1 into the final film.
[Segmented render] 0-{N} s: {environment, tone, character materials, light and shadow}.
  At {N} s {transition trigger and method}: {render description of the new scene}.
[Scene] text or @Image W.
[Wrap-up] whether environment and character rendering stay the same after the transition; audio handling.
```
Before uploading a fine model, remove trajectory lines, axes and camera cones from the video.

## 8. `bridge` — seamless transition between two videos

```
Seamlessly connect @Video 1 and @Video 2, but do not modify @Video 1 or @Video 2.
<How @Video 1's last moment drives into the bridge — camera move, object, motion direction and speed.>
<The bridge itself — what covers/transforms the frame.>
<How the bridge resolves into @Video 2's first frame — matching position, scale and motion.>
```
Official bridge triggers: pushing into a circular neon reflection, an umbrella wiping across the lens, a paper
plane flying into the lens, glowing particles filling the frame. Also supported: focal-length, rotating
outfit-change and dive transitions.

## 9. `grid` — multi-grid storyboard

Draw the storyboard as simple line drawings or stick figures; use the prompt for everything the drawing lacks.

```
@Image 1 is the complete storyboard of the film, made of <N> consecutive shots read <left-to-right, top-to-bottom>.
Each panel is one complete shot, not a separate character sheet.
<Character> refers to @Image 2, <prop> refers to @Image 3, …
<Global setting: style, world, light, sound.>
<Story summary in one or two sentences.>
Shot 1 (<seconds>): composition, shot size, camera move, action. Shot 2: …
<Continuity: identity, outfit, positions, screen direction stay consistent between panels.>
```

## 10. Capabilities on top of a mode

- **Clean footage (no random subtitles / music):** "pure video, no subtitles, no background music". Use it for
  B-roll, ads you will finish in editing, music videos, loop backgrounds.
- **Remove BGM from a video, keep voices:** "Remove the background music in @Video 1, keep only <whose> voice and
  natural ambient sound. Keep the original footage completely unchanged."
- **Voice (tone) reference:** upload a clean, noise-free voice as @Audio N; "Reference @Audio 1 and say {I found
  you}, keeping a low, suspenseful tone." Add the emotion.
- **Multi-person:** one reference per person, each bound by name; state actions and relationships ("A and B sit
  by the campfire talking; A hands B a glass of water"). Never "@Images 1-4 are the four characters" — bind each.
- **Green screen:** upload the green-screen video and describe or reference the new scene: "Replace the background
  with a medieval magic forest with mysterious light." / "Refer to the classroom picture and naturally integrate
  the characters from the green screen into it." Compositing several videos: "Composite @Video 1 and @Video 2 into
  @Video 3. As the camera pushes in…"
- **Creative transfer:** "Reference the <expressions / camera language / creative format / rhythm> of @Video 1 to
  make <new subject from @Image 1>." Say which dimensions to inherit and which not (identity, clothing, scene).
- **Perspective change:** "Replace the multi-camera switching in @Video 1 with a fixed frontal shot; keep people and
  background unchanged." / "Film @Video 1 from an over-the-shoulder view behind the person on the left; keep
  identities, clothing, postures, rhythm and object positions unchanged." The model fills in unseen space.
- **Remove / replace objects:** "Remove the woman on the left and the man on the right in @Video 1, keep only the
  woman in the middle, actions unchanged."
- **Complex motion:** 2.5 handles long-tail actions — describe them physically and in order ("performs a backflip
  in the rain, draws a long sword after landing, rain slides down the blade").
