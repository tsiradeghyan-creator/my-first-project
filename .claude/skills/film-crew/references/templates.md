# Output templates

Use these headings. Department documents may be in the user's language; prompts are English.

## 00_brief.md
```
Project · Brand/client · Goal · Logline · Deliverable · Duration · Ratio · Platform · Resolution · Target model
Client brief (TZ) when there is a client:
  Content pack: | # | type (video / still) | scene description | mood | reference | channel |
  Aesthetics: style · palette · light key · characters (faces shown or not; focus on silhouette, hands, product)
  Product rules: what must be visible, logo/packaging, what never appears
Style lens: <director> — why
Shot budget: <duration> ÷ ASL <n s> = <N> shots (rounded)
Assumptions: …
Open questions: … (only if they change the plan)
```

## 01_director.md
```
Dramatic core · Subtext · Visual thesis
Direction rules from the lens (4-6)
Beat map: | # | scene | beat | function | state in → out | audience must see | shot family | target s |
Performance notes per character
Edit intent
```

## 02_world.md
```
Per set: name · INT/EXT · time · period
  Floor plan (compass) · Master side
  [SET: name] locked description (60-120 words)
  Hero props + state timeline
  Light sources in set
Palette: dominant · secondary · accent · danger
```

## 03_costume.md
```
Per character: [LOOK: name] locked card (80-140 words)
Wardrobe state table: | character | beat 1 | beat 2 | … |
Separation notes
```

## 04_camera_light.md
```
Lens plan (2-4 focal lengths + meaning) · Format & texture · Depth of field
Per scene: [LIGHT: scene] locked light block · axis map (line, side kept, planned crossings)
Camera grammar (when it moves, rigs) · Coverage strategy · Grade
```

## 05_edit_plan.md
```
Shot order: | shot | scene | beat | function | size (step 1-6) | angle | s |
Size line per scene: e.g. `2 → 4 → 5 → 6 → 6 → 2` with every cut marked clean / allowed / accent
Cuts: one handoff contract per cut (format in references/editing-grammar.md)
Rhythm map per scene · Scene transitions · Generation units
```

## 06_shot_list.md
```
| shot | rig/height | lens | start frame | move: path · speed · motivation | end frame | subject action | focus | risk |
```

## 07_sound.md
```
Policy + clean-output phrase · [SOUND BED: set] per set · effects by shot
Dialogue: | shot | speaker | line | language | delivery | seconds |
Cut-by-cut sound transitions · Music plan for the edit
```

## 08_storyboard.md — one card per shot
```
### SHOT <n> — <scene> · <duration> s · <size> · <angle> · <lens> · <move>
Purpose: <from the beat map>
Handoff in: <contract from previous cut>
Start keyframe (image prompt):
  <SET block> <LOOK blocks> <composition, lens, light block, palette — no motion>
End keyframe (only if the cut needs an exact landing):
  <…>
Video prompt (<target model>):
  <asset declaration>
  <one-line summary>
  [0-Xs] <picture + camera move + action + dialogue + sound> ➖ <local bans>
  <global supplement: locked blocks + clean-output phrase + bans>
Sound: <bed + effects + dialogue + across-cut transition>
Handoff out: <contract to next cut>
```

## 09_generation_plan.md
```
| unit | shots | method (same call / first-frame chain / first+last / extension / bridge / independent) | duration | references to upload (in order) | depends on |
Generation order · QC checklist per unit · Edit assembly notes (where score and titles go)
```

## 10_review.md
```
Per department: checklist results (pass / fixed: what changed)
Virtual cut: one line per cut — pass / fixed
Remaining risks
```
