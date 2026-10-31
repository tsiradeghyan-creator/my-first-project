# Seedance 2.5 — transitions

Source: `official-guide-lark.md` → "How to write a video extension?" (transition table). Use at any cut — inside a
30 s / Long Video prompt or in a cutting extension. Every transition uses the same three lines:

```
1. Use a "<transition>" transition at the cut point (no rigid cut, no objects appearing out of thin air).
2. <What happens: picture A → mechanism → picture B, with the concrete content of A and B.>
3. Switch scenes naturally. <optional: and the shot size changes from X to Y>
```

Give the model a broad description and let it improvise, or a specific A/B description and it follows you. You can
also offer a list and let it choose: "Choose the transition that suits this film best from: natural shot switch /
mask transition / ink transition / similar-object transition."

## Foundation transitions

| Transition | What it is | Use for | Line 2 template |
| --- | --- | --- | --- |
| Natural shot switch | A becomes B directly, but the shot must "breathe" — enough duration before the switch, not a hard cut | most ordinary narrative | Keep the camera's breathing and duration coordinated; leave enough time; shot A <…> then naturally becomes shot B <…>. |
| Fade in / fade out | Picture darkens to full black (or white), next one rises from it | openings, endings, time passing | Picture A darkens until fully black (or white), then picture B slowly emerges and brightens. |
| Dissolve (stacking) | A turns transparent while B appears; 1-2 s overlap | memory, dream, slow time, lyrical moments | As picture A slowly becomes transparent, picture B appears, overlapping and blending for 1-2 s. |
| White / black flash | Frame flashes white or black for an instant, then cuts | impact on a beat — drum, gunshot, shutter; tense edits | The screen bursts into white light (or plunges into black) for an instant, then cuts fast to the next scene. |
| Wipe | B pushes A off like a sliding door from one side | retro feel, clear change of location | Picture B advances from the left (right/top/bottom) like a sliding door, fully covering picture A. |

## Creative transitions

| Transition | What it is | Use for | Line 2 template |
| --- | --- | --- | --- |
| Mask transition | Camera pushes into an object (wall, back, palm, pillar) until the frame is black; pulls out in a new scene | crossing space — through a mirror, behind a passing object | The camera pushes forward until <object> fully blocks the lens and the frame goes black, then it pulls out of the darkness into <scene B>. |
| Similar-object (match) cut | Last frame of A matches first frame of B in shape, outline or colour | montage | Shape match: <round moon in A> seamlessly becomes <round latte art in B> as the camera advances. |
| Action / whip transition | Hard swing in A with motion blur; B enters with the same direction and force, then settles | action, parkour, travel vlogs — "instant transfer" | In A the camera swings hard to the left with strong motion blur; B enters from the blur in the same direction and force and freezes. |
| Motion relay | A character's movement carries across — jumps out of frame in A, falls into frame in B | outfit changes ("kick-shoe / finger-snap change"), jumps between places | In A <character> jumps up and out of frame; in B they fall into frame from above, now <in the new place/outfit>. |
| Zoom in / zoom out | Zoom into a detail of A (pupil, keyhole) until it becomes all of B, or the reverse | grand ↔ micro scale, "world within a world" | The camera zooms into <detail> in A until it fills the screen and unfolds into the panorama of B. |
| Ink transition | A spreads like ink dropped into water and dissolves; B emerges from the ink | oriental, poetic, historical, memories | Picture A spreads like thick ink in clear water and fades; picture B emerges from the scattered ink. |

## Bridge-only triggers (seamless transition between two existing videos)

Pushing into a reflection, an object wiping across the lens (umbrella, hand, paper plane), particles filling the
frame, focal-length transitions, rotating outfit-change transitions, dive transitions. See `prompt-formulas.md` §8.
