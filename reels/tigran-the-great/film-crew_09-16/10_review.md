# 10 · Review — block 09–16

## 1. Self table read
- Director: every shot traces to a beat; thesis visible — the king still in 1, 2, 6 (until the hand), 7; the world moves around him. Pass.
- Production design: Set A / Set B locked text; after review Set B text is pasted verbatim into shots 3, 5, 7, 8 (plus a shot-specific clause). Fixed.
- Costume: King LOOK verbatim in 1, 2, 7; insert 6 uses the hand/vambrace/cloak/cuirass part only (a full face description in an insert invites a face into the frame — deliberate). Archer LOOK corrected to the still (quiver at the hip, no blaze). Cavalry horses "bay, brown and grey" everywhere. Fixed.
- DP: LIGHT A rim side now "frame-right side of his face and crown"; LIGHT B verbatim in 3–8; fire only in 1–2; axis kept (Armenians L→R, Romans frame-right). Fixed.
- Sound: clean-output phrase in all 8 prompts; beds A/B repeated; no dialogue. Pass.

## 2. Validator
`validate_package.py` → PASS, 8 shots, 7 cuts, 8 prompts. Warnings: slices shorter than 3 s in prompts 2, 4, 5, 6, 7. Judged acceptable: each short slice holds one single action (a breath, a lift, a draw, a curl, the chop) inside 4–5 s clips; merging them would put two actions in one slice.

## 3. Independent verifier (film-continuity-verifier) — verdict FAIL, all items checked against the files and stills
| # | finding | checked | action |
|---|---|---|---|
| F1 | 14_signal.jpg: the raised arm is not clearly the right arm (brooch beside it) — clash with "right hand" in 6/7 | confirmed by viewing the still | removed left/right everywhere; 7 says "raises the arm on the frame-right side of his body, exactly as in @Image 1"; 6 is "his hand" |
| F2 | shot 1: soldiers in the still walk away from camera, prompt had them coming toward it; self-contradiction | confirmed | soldiers now walk away into the city; the king walks against the stream (stronger image); 02/05/06 updated |
| F3 | King LOOK incomplete in 2, 6, 7; "armour" vs "cuirass" | confirmed | full LOOK in 2 and 7; 6 kept partial on purpose (see above), wording → "cuirass" |
| F4 | archer LOOK vs still (quiver, blaze) | confirmed | LOOK changed to the still; action "reaches down to the quiver at his hip" |
| R1 | shot 4 lacks the R→L legion vector | accepted | "march … from right to left of frame", ban on L→R |
| R2 | shot 7 riders face camera/left in the still | accepted | "wheel their horses to frame-right and ride off left to right", ban on riding toward camera |
| R3 | horse colours differ | accepted | "bay, brown and grey" |
| R4 | shot 8 river geography | accepted | "splashes across the shallow flooded edge of the river toward the shield wall on the east bank" |
| R5/R6 | LIGHT B / SET B not verbatim | accepted | pasted verbatim |
| R7 | rim side ambiguous | accepted | frame-right side |
| R8 | eyeline height in 7 | accepted | "slightly down toward the river" |
| R9 | shot 8 "low" vs "eye level" | accepted | "camera about one metre above the ground" |
| R10 | splash peak timing in 4 | accepted | "the splash peaks at about two seconds" |
| R11 | 12a next to 12 | accepted | moved to stills_09-16/rejected/ |

## Remaining risks
- Shot 7 still asks for two events (chop, then riders wheeling away) in 5 s; fallback in 09 (drop the surge).
- Style card is researched-unreviewed; two spot-checks could not run (network). Nothing in the prompts depends on an unverified fact beyond general look phrases.
