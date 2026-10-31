# Seedance 2.5 — limits, inputs and UI modes

Source: `official-guide-lark.md` → "1. Parameter setting" and "2. Function interaction" (Dreamina web). If the live
UI shows different numbers, the UI wins — tell the user.

## Output

| Item | Seedance 2.0 | Seedance 2.5 |
| --- | --- | --- |
| Duration (Omni / frames) | -1 or 4-15 s (97-361 frames) | **-1 or 4-30 s (97-721 frames)** |
| Long Video | — | **30-180 s in one pass** |
| Extension | — | source < 30 s, +4-30 s per step, nested up to **60 s** total |
| Resolution | — | **480p, 720p** |

`-1` = let the model choose the length.

## Reference inputs

| Type | Seedance 2.0 | Seedance 2.5 |
| --- | --- | --- |
| Images | 0-9 per request | **up to 30** (up to 4K) |
| Videos | ≤ 3, each 2-15 s, total ≤ 15 s | **≤ 10, each 2-30 s, total ≤ 30 s** (tolerance 1.8-30.2 s) |
| Audio | ≤ 3, each 2-15 s, total ≤ 15 s | **≤ 10, each 2-30 s, total ≤ 30 s** (tolerance 1.8-30.2 s) |
| Audio-only input | not supported | **supported** |

File specs (same for 2.0 and 2.5):

- **Image:** jpeg, png, webp, bmp, tiff, gif, heic, heif · aspect (w/h) 0.4-2.5 · 300-6000 px per side · < 30 MB each ·
  request body ≤ 64 MB (no Base64 for large files).
- **Video:** mp4, mov · 480p-4K · aspect 0.4-2.5 · 300-6000 px per side · total pixels 409,600-8,295,044 ·
  ≤ 200 MB · 24-60 fps.
- **Audio:** wav, mp3 · ≤ 15 MB each · request body ≤ 64 MB.

## Stability sweet spots (official recommendations)

| Situation | Stable | Possible, less stable ("may need re-rolls") |
| --- | --- | --- |
| Subjects in a reference video/audio | 1-5 | 6-10 |
| Length of a subject's reference video/audio | 5-10 s | longer |
| Subjects across reference images | 1-8 | 9-12 |
| Views per subject | ≤ 5 subjects: single or multi-view both fine | > 5 subjects: single view per image |
| Multi-view input | several images, one view each | one collage with many views (worst) |
| Video to edit | ≤ 20 s | longer |
| Reference images for a video edit | 1-5 | 6-8 |

## UI modes (Dreamina → AI Video → Dreamina Seedance 2.5)

- Pick ratio, resolution and duration in the toolbar, then the mode: **Omni Reference**, **Smart Edit**, **Long
  Video**, **First and Last Frames**.
- **Long Video:** mode menu → Long Video → clock icon → slide or type 30-180 s → confirm ratio/resolution →
  Generate. One pass, no stitching.
- **Extend Video:** under a generated clip click *Extend Video* (only for sources < 30 s) → clock icon → set the
  added seconds (4-30) → write a prompt for **the new part only** → Generate. Result = original + added seconds.
  While the result is still ≤ 30 s you can extend again ("nesting"); the extreme case is 30 s + 30 s = 60 s.
  The extend button appends after the last frame.
- **Smart Edit:** choose the Smart Edit mode, upload a video, describe the change in text.
- **Edit with marks:** after uploading a local video, mark the frame with box, brush, arrow, anchor point, line or
  text (eraser available), write the change, press *Add to Input Box*; a time label such as "⏱️00:00 Video Frame
  Labeling" appears; Generate.
- **Edit Video:** the same marking tools, but on a clip you already generated (icon under the clip).
- **Clay Renderer plugin:** Blender/Maya plugin exports the white-model camera/action video straight to Dreamina
  web as a reference video. Install steps: `official-clay-plugin-lark.md`. Coarse white models currently give
  better results than fine ones.

## Auto-behaviour worth knowing (secondary source — not in the Lark guide)

Reported in smixs/visual-skills `seedance-25.md` (ByteDance Prompt Guide + launch-week tests). Treat as likely,
verify in the UI:

- Edits keep the source's ratio and length (±0.3 s); extension keeps the source's ratio.
- In First and Last Frames the ratio follows the first image — a last frame with another ratio gets stretched.
