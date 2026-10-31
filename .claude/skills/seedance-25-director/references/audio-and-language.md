# Seedance 2.5 — audio, dialogue and language

## Languages (official, Lark guide → "Breaking language boundaries")

- Prompts can be written in many languages; dialogue in the prompt is spoken in that language.
- **Optimisation priority:** Chinese, English, Spanish, Indonesian, Malay.
- **Fully covered:** Thai, Arabic, Portuguese, Vietnamese, Japanese, Korean.
- **Armenian and Russian are not on the list.** Before any project with Armenian or Russian dialogue, run a short
  test. Fallbacks if lip-sync or pronunciation fails:
  1. generate the scene with no dialogue ("no dialogue, no BGM, natural ambience only") and add voice in editing;
  2. keep the speaker off-screen, from behind, or in a wide shot so lip-sync does not matter;
  3. use a clean voice reference as @Audio (tone reference) and test whether the lines hold.

Dialogue reinforcement formula (ByteDance Prompt Guide via smixs — secondary):
`dialogue language + accent/regional variety + delivery + speaker + {line}`
e.g. `The young man says in natural Los Angeles English, half-laughing: {No way, you actually made it.}`

## Audio markers (ByteDance Prompt Guide via smixs — secondary, not in the Lark user guide)

| Content | Marker | Example |
| --- | --- | --- |
| Music | `( )` | `(soft rhythmic piano in the background)` |
| Sound effect | `< >` | `<a bell rings in the distance>` |
| Dialogue | `{ }` | `{Hello, welcome back.}` |
| On-screen text / title | `【 】` | `【Chapter One: Departure】` |

The Lark guide's own examples write audio in plain sentences ("Sound: No background music (No BGM). Real urban
ambient sounds…"). Both work; plain explicit sentences are the safe default, markers add precision.

## Sound policy — say it every time

Each prompt should state, explicitly and without contradiction:
- dialogue: who says what, in which language, or "no dialogue";
- ambience and sound effects tied to visible causes;
- music: what kind, or "no background music";
- subtitles/text: what appears, or "no subtitles".

For clean footage to finish in editing: **"pure video, no subtitles, no background music"** (official wording).

## Voice (tone) reference

- Upload a **clean, noise-free** voice as @Audio N.
- "Reference @Audio 1 and say {I found you}, keeping a low, suspenseful tone." Add the emotion and delivery.
- Use for a recurring character voice, brand voice, or strong dramatic delivery.

## Audio-only driving

Seedance 2.5 accepts audio as the only reference (2.0 did not). Use @Audio for rhythm ("cut on the beats of
@Audio 1"), voice, or ambience. Up to 10 clips, total ≤ 30 s.

## Removing music from an existing video

"Remove the background music in @Video 1, keep only <speaker>'s voice and natural ambient sound. Keep the original
footage completely unchanged." Subtitles already in the picture are preserved.
