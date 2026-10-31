# Seedance 2.5 — failures and fixes

Diagnose before rewriting: name the symptom, the likely cause in the prompt or inputs, then the smallest fix.
Fix order — cheapest first: (1) change wording, (2) change references/inputs, (3) change mode or duration,
(4) split the shot, (5) after 3 failed tries on the same shot, redesign the shot instead of re-rolling.
(The cost ladder and the 3-tries rule are directing practice, as in DirectorSKILL; the fixes below cite the
official guide where it speaks.)

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Characters look like twins / faces swap | identities bound loosely ("@Images 1-4 are the four people"), too many subjects in one reference, multi-view collage | bind each person by name to one image; one view per image; ≤ 5 subjects per reference video, ≤ 8 across images (official sweet spots) |
| Plastic "AI" skin, Jimeng look | no texture language | realistic-human formula; add "retaining real fine pores and skin texture", "native skin texture", "hair roots distinct" (official) |
| Random subtitles or music appear | no explicit ban | "pure video, no subtitles, no background music" in the plot and again in the global supplement (official) |
| Action happens too early / plot "fast-forwards" | no timestamps, or too much in one slice | timestamp every slice; ≥ 3 s per slice; one main action per slice (official timestamp control) |
| A slice gets chopped into many cuts or loses events | content exceeds its time budget | remove events or give the slice more seconds |
| Nothing happens / the model improvises | too little content in a slice | add the action and its end state |
| Emotion reads fake or over-acted | emotion words, too many facial cues | 2-4 visible cues, motivated by a trigger; add the "why" line under the slice (official three-module method) |
| Tears, laughter, falls before their cause | effect written before the trigger | write cause → reaction in order; ban premature reactions explicitly ("no tears before 20 s") |
| Extension resets, jumps or objects pop in | prompt re-describes the whole video, or no continuity clause | describe only the new part; add "natural extension, smooth action connection, no rigid cuts, no objects appearing out of thin air" (official) |
| Edit changes things it should not | target, area or time not specified | full edit formula: marks + target + change + time, then list what stays unchanged (official) |
| Clay render looks stiff / limbs wrong | coarse model with limbs or wings | write the complete limb action sequence, or remove limbed/winged models (official) |
| Fine clay render shows lines or cones | trajectory lines, axes, camera cones left in the export | clean the reference video before upload (official) |
| Bridge alters the source clips | missing protection clause | "do not modify @Video 1 or @Video 2" (official) |
| Wrong language spoken / bad lip-sync | language outside the supported list (e.g. Armenian, Russian) | test first; fallbacks in `audio-and-language.md` |
| Reference ignored or misused | file not mentioned, or role vague | mention every file with role and what not to take; re-@ it where it matters |
| Ratio stretched in First/Last Frames | last frame has another ratio | match both frames to the same ratio (secondary source) |
| Generation blocked by moderation | real celebrity, copyrighted character, graphic violence | remove names/brands, soften violence wording (from the user's Seedance 2.0 rules) |
| Long video drifts in style or identity | globals stated once | restate duration/ratio at the top and repeat identity, outfit and look in the global supplement |
