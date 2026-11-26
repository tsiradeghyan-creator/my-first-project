# Prompt craft: what the studio's best prompts do

This guide is distilled on 2026-11-26 from 24 example prompts Tigran shared, plus one system prompt (`tigran-examples/01–25`). Each rule names the examples it comes from. Read it when you write a final image or video prompt, or a plan that feeds one. It adds to film-crew's departments; it does not replace them.

The two schools in the examples:
- **John series (01–18).** Grounded survival drama, physical detail, artefact locks, no music, no slow motion.
- **Mira series (19–24).** Comedy and fantasy, dialogue, voice references, named camera packages, slow motion when it serves.

Rules marked *default* are broken on purpose when the meaning asks for it (15, 16, 22, 24); say so in the prompt when you break one.

## 1. Plan before you prompt

- **Project type first (25).** Decide what kind of piece it is: narrative, ad, explainer, music video, documentary, reel, or a plate. Don't invent conflict, characters or a twist the piece doesn't need.
- **Audio-first when audio exists (25).** If there is a script, voice-over, dialogue or music, map its phrases, pauses and accents before designing pictures. Use given timestamps as the clock. Label estimated timing as approximate. Keep the script word for word unless asked.
  Every key phrase gets a picture that carries its *information* (names, numbers, the language, the brand), landing
  on that phrase's timestamp: "ages zero to sixteen" shows the range; "in Armenian" shows Armenian; the brand or logo
  lands on the brand line. Symbolic imagery can sit on top of that information, never replace it. (Eval 2026-11-26:
  a symbolic-only voice-over plan lost to a literal one twice.)
- **Units are not interchangeable (25).** Sequence, scene, shot, generation task and editing task are different things. Keep a separate list of editing tasks: things done in post (speed ramps, glitches, text, the wipe between worlds).
- **Split dense work (03, 08, 12, 17, 19, 23).** One generation holds about one clear event per 2–3 seconds.
  - Split at the cut where the world, lens family or cast changes.
  - Split when a shot packs more than 3 cuts, a sub-second insert, or 5+ separate events.
  - Speed ramps and image glitches are safer in post (22, 24).
- **Speed against distance (15).** Check that the distance an object covers fits the time and the stated speed. "From the horizon to the gate in 3 s" breaks a "slow and steady" motion lock.
- **Honesty (25).** Say "expected", never "tested", unless a generation was actually run.

## 2. References: the asset map

- **Every reference has a role (01, 06, 07).** Say what it governs (identity / costume / place / light and grade / prop) and what it does **not** govern ("location reference, not a starting frame"; "governs the look only, not the camera, framing or action").
- **Declare deltas (06, 13, 18).** When the shot must differ from the reference, say so: "the grass is much taller than in the reference", "the bus is much further away than in the reference", "use only the grass and land, not its sky or sun". Never claim "matches exactly" while asking for something the reference lacks (the 04/05 conflict).
- **Ban the reference's own viewpoint by description (04, 05, 13).** Write "no three-quarter view from the left corner", not just "don't copy the framing". Plates are made first so that every shot can find a new angle in the same world.
- **Describe a video reference's content so it isn't copied (07, 08).** "In video_1 the camera is a distant wide with five men; here it is a tight shot of one man."
- **Take only part of a multi-object reference (14).** "Only the cans; the white bottle is never seen."
- **Reverse angles from one reference (15).** "Same gate, seen in reverse: from inside, looking out." Say what is now behind the camera.
- **Absent characters.** Don't attach the reference of someone who is off-screen. If you must, add "NEVER APPEARS" (06, 16).
- **One face reference per character (19–24).** Other references for that character are costume-only. Several face references cause identity drift.
- **Fixed text per id across a series (07, 14, 18).** Write one description per reference and reuse it word for word. Watch for drift: the rifle was "lever-action" in 01–04 and "bolt-action" in 18; the hunter's marks changed between 06 and 07.
- **Identity from the reference, costume from the text (19, 22).** "ONLY a cowboy hat is added."
- **Minimum set (25).** Attach only the references this generation needs. No reference guarantees identity.

## 3. Performance (director)

- **One physical channel (01, 02, 03, 12).** The emotion lives in one body part doing a task: feet and eyes backing away, a finger on a trigger, hands on controls. It is not acted on the face.
- **Acting task (01–04, 12, 14, 17, 18).** Give a GOAL, an OBSTACLE, a TACTIC, and **moment-to-moment beats** that become visible behaviour. Motive and "the event" are director's notes; keep them short.
- **Name the clichés to avoid (01, 07, 14).** "Fear is never acted: no wide eyes, no gasp"; "not the staring madman, no savouring"; "a man listening, not a man posing".
- **Performance by contrast (07).** "The madness is in the hands; the face is almost empty."
- **Gaze safety (01+).** The gaze is always on a task, never glassy; natural blinks. Count blinks when it matters ("blinks once", 14).
- **Turn the obstacle into a physical beat (03, 14).** The engine coughs twice; the empty can booms.
- **Animal acting (16, 21).** State the animal's state of mind ("calm, curious, unbothered"), then list concrete behaviours (steps shortening, an ear flick, two breaths). Behaviour transfer can be the gag (a dragon doing puppy moves).
- **Overlapping action (07).** "The hand is already going down as the knee is still dropping; no plateau." This works against the AI habit of moving in separate steps.
- **Anti-sync by cause (08, 06, 20).** Crowds and groups arrive or act at different moments, so they can't move in unison. "Never perfectly synchronised" alone is weaker.
- **Comic timing is written out (19, 22, 23).** Line finishes, 1–2 s of silence, an interruption mid-line. Seriousness is played straight for the laugh.
- **Weapons and violence (02, 18, 23).** The finger rests along the guard; the muzzle points past the lens; the shot is suggested off-screen; no wound or blood. It is truthful craft and keeps moderation clear.

## 4. Camera (DP and operator)

- **The camera is a person with a reason (06, 08, 14, 18, 20, 24).**
  - prey running backwards;
  - a watcher braced on the ground, breathing;
  - a startled reporter;
  - an operator running beside a fighter.
  
  Write its behaviour and its mistakes (over-corrects, stumbles, loses focus), plus "if the shot looks operated, it is wrong" where that applies.
- **Physical operator motion, not digital shake (24).** Describe the causes (steps, reframing) and ban "artificial shake, gimbal, digital floating".
- **POV from named physical signals (08).** Obstruction, breathing, bracing, and "there is no fourth". Ban the clichés by name (scope reticle, binocular mask, HUD).
- **The camera touches the world (18, 24).** Stalks bend and spring back; mud hits the lens. "Never passes through like a ghost."
- **Scale by what can be read (08).** "You can read arms rising and falling, and nothing else; more is too close."
- **Reveals.** By foreground wipe (04), by approach (18), by crane (13), by rack focus as a punchline (19), and by imperfect acquisition: overshoot, focus hunt, settle (24).
- **Geography lock (04, 22).** Fix the positions of vehicles and parties, which way they face, and which side the camera sees. Work out reverse angles in advance. Repeat the screen direction (16).
- **Lens facts are real (14).** Lens, field of view and distance must agree (85 mm ≈ 29° diagonal). Check that the distance fits the framing (16).
- **Motion lock (13, 15–18).** MOTION SPEED AND QUALITY: real time, never fast-forward; smooth, never jerky or robotic; no frame skipping. Slow motion is used only on purpose, with a percentage (24).
- **Symmetry and centring are defaults to break for meaning (15).** The padlock on the centre line is the theme. Otherwise keep dramatic objects off-axis and partly hidden (11).

## 5. Editing

- **A CUT POLICY with the cut times pinned (17).** "Hard cuts only at 4.5 s, 9 s, 15.5 s; no extra cuts." Cuts fall on the action, and sound runs across them (03).
- **Start late (17).** Open with the action already happening (the petrol already pouring).
- **Decimal seconds or mm:ss.** Never seconds:frames like "3:12", which reads as minutes (06–08). Use 0.0–3.5 s or 00:03.
- **Size jumps as punctuation (03).** Extreme close-up inserts, then an extreme wide.
- **Transitions between worlds (23).** A practical foreground wipe, a visual rhyme between the first and last shots; generate each side separately.
- **A defined last frame (02, 04, 12).** "Hold to the final frame" plus what is in it, not a state like "still walking".

## 6. Sound

- **Whitelist first (06–08, 14).** "ONLY THE FOLLOWING SOUNDS EXIST", numbered, then one no-music line. A long list of "no X" can prime the thing it bans.
- **No-music wording without "drone" (03).** A drone camera and a "no drone" music ban collide. Write "no drone note" or call the camera "an aerial shot from high above". "MUSIC: FALSE" reads like code; write "no music; diegetic sound only".
- **Mapped per shot, with perspective (03, 04, 08).** Every click in the cab; the engine small and distant from the air. Sound arrives late over distance (08).
- **Acoustics match the space (06, 13, 14).** Dead in fog, an echo off shopfronts, reverb only inside the empty cans.
- **Signature sounds (12, 14, 17).** The pill rattle, the hollow boom, the glug turning to gurgle. Processes go in phases, with the sound matching the picture.
- **The world off screen (07, 15).** The others still working; the fence energiser ticking. Impacts are "never in a beat", so they never become music.
- **Dialogue (19, 22, 23).** A delivery note per line, an accent, the stressed word, a voice reference.

## 7. Light, grade, stock

- **Name the sources, the brightest value and the darkest value (05, 09, 11).** Shadows keep their detail; nothing crushed to black.
- **Overcast still has contact shadows (11).** "No visible shadows" looks CGI. Write "only soft contact shadows under cars and in doorways".
- **Freeze the state (06, 07, 14).** "Identical exposure and grade from first frame to last; nothing emits light; eyes do not glow."
- **Fit the stock to the light (04).** Daylight 250 fine grain for overcast daylight. Tungsten in daylight goes cool on purpose, so say "cool".
- **A palette in proportions (05, 09–11)**, with drift rules under the grade ("teals going grey-green").
- **Ban the default looks by name (09, 11, 24).** No teal-and-orange, no video-game styling, no post-apocalyptic stylisation, no glossy fantasy.
- **Avoid contradictions.** "THE GRADE" against "no colour grade"; deep focus against bokeh (09–11).

## 8. Plates and set dressing (production design)

- **Plates for compositing stay neutral.** If a plate will be keyed or layered, it has no film grain, no grade, no
  vignette, no flare or bloom, even exposure, the key-light direction stated, and clean space where people go. The look
  is added after the composite. Plates used only as a world reference (05, 09–11) may carry the look. (Eval 2026-11-26:
  a graded compositing plate lost.)
- **Plate-first world building (05, 09–11, 13).** Make still plates, then shots that reference them with the viewpoint banned and the deltas declared.
- **Forensic set dressing with a timeline (09, 10, 11).** The only fresh scratch against a year of dust; footprints under dust; a gouge with weeds in it. The objects say who, what and when.
- **Causal backstory for any dramatic object (11).** The bus left the road at speed, rolled, slid; the lamp post is pinned under it. "Read as an accident, not a placement."
- **Scarcity logic (10).** What is left and what is gone, and why.
- **One humane detail per zone (09, 11).** Uncollected prescriptions; chairs stacked at closing.
- **De-emphasise the spectacle (11).** Half hidden, off-axis, a small share of the palette.
- **Restrained decay with a stated elapsed time (11).** Keep one figure for the whole series.
- **Variety against cloning (10, 16, 19).** Different containers, animals and figures.
- **Design for the next shot (09).** The foreground gap is the route in.
- **Text (12, 13, 22).**
  - Readable text comes from a reference or is spelled exactly in quotes.
  - Everything else is "faded and unreadable at this distance".
  - Keep text out of face close-ups.

## 9. The prompt's shape

- **Default to the compact template (15, 17, 18): about 400–900 words, one line per block.**
  1. Header: duration, shots, cuts, aspect ratio, fps.
  2. CUT POLICY.
  3. NO BGM.
  4. MOTION SPEED AND QUALITY.
  5. REFERENCES, with roles and deltas.
  6. SETTING (plus the geography lock if needed).
  7. REALISM.
  8. SHOTS, timed in decimal seconds.
  9. CAMERA.
  10. PERFORMANCE: channel, task, beats, gaze safety.
  11. PHYSICS: artefact locks by name.
  12. LIGHTING.
  13. AUDIO: whitelist.
  14. Stock, plus the text policy.
- **The long template (06–08, 14, about 2,000–2,700 words)** adds a recap block at the end. Use it only when the target engine's field is long enough; text past the limit is cut silently. Keep capitals for real priorities.
- **Positive phrasing pulls harder** than strings of negatives. Keep negatives for named artefacts that actually appeared, and lock a repeated failure by name (the hat, the sun, the tongues).
- **Camera brand names (19–24)** are untested with our engines. The look described in plain words is the safe default.

## 10. The check before delivery

Before delivering a prompt, check these:
- Does every reference have a role?
- Are the deltas declared, and the reference viewpoint banned?
- Is there one face reference per character, and no off-screen character attached?
- Is the per-id text the same as last time?
- Do the events fit the duration?
- Do distance, speed and lens agree?
- Are the times in decimal seconds or mm:ss?
- Is the last frame defined?
- Is the audio a whitelist?
- Is there no "drone" ambiguity?
- Are the light sources named, and are the contact shadows kept?
- Are there no contradictions (grade vs no grade, deep focus vs bokeh, "matches exactly" vs a delta)?
- Is text either from a reference or unreadable?
- Is post work listed separately (ramps, glitches, overlays)?
