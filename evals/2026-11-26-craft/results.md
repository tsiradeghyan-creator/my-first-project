# A/B: skills before vs after the prompt-craft guide (2026-11-26)

**Arms:**
- OLD is the skills at `d89e0da`, before the guide.
- NEW is the skills at `c205849`, the guide wired in.
- NEW′ is `2900412`, two fixes after round 1.

Both arms get the same CLAUDE.md, business.md and memory, with no web and no MCP. A blind model judge uses the same 4-criterion rubric as the first eval, so it is not primed with the guide's vocabulary.

## Round 1: 8 tasks × 2 runs (`out/`)

| Task | NEW wins | OLD wins | Mean total NEW / OLD (max 20) |
|---|---|---|---|
| S2 Seedance, Narine, the floor shakes | 2 | 0 | 17.5 / 14.5 |
| F2 film-crew, Villeneuve scene | 2 | 0 | 17.0 / 13.5 |
| N3 hunter's patience (one physical channel) | 2 | 0 | 17.5 / 15.0 |
| F1 studio teaser | 1 | 1 | 15.0 / 13.5 |
| C1 Kling, Gyumri | 1 | 1 | 18.0 / 17.5 |
| N2 reference roles and costume delta | 1 | 1 | 17.0 / 17.0 |
| N1 voice-over-led promo | 0 | 2 | 16.0 / 17.5 |
| B3 compositing plate | 1 | 1 | 15.0 / 17.0 |
| **Total** | **10** | **6** | 16.6 / 15.7 |

The cost and time were the same: $0.44 and 72 s per run on both arms. The guide adds no overhead.

**The losses explained (judge notes):**
- N1: the new plan made the voice-over symbolic and lost key information ("ages zero to sixteen", "in Armenian", the logo timing).
- B3: one new run baked grain and a grade into a compositing plate, and named the model "Banana Pro" instead of Nano Banana Pro.

**Fixes (`2900412`):**
- Voice-over lines must carry their information, landing on their timestamps.
- Compositing plates stay neutral.
- Official model names in the settings lines.

## Round 2: the two lost tasks × 3 runs, NEW′ vs OLD (`out-retest/`)

| Task | NEW′ wins | OLD wins | Mean NEW′ / OLD |
|---|---|---|---|
| B3 compositing plate | 3 | 0 | 18.7 / 14.3 |
| N1 voice-over-led promo | 2 | 1 | 17.7 / 17.0 |

## Reading

- **Overall:** with the fixes, the six untouched tasks give 8–4 and the retest gives 5–1, so **13 of 18 comparisons go to the new skills**. That is a modest but consistent gain, at no extra cost.
- **Strongest gains:** performance-heavy video (S2, F2, N3, +2.5 to +3.5 points), which is where the guide's acting, camera and audio rules apply.
- **Limits:**
  - one model judge, from the same model family;
  - text prompts only, with no generated video;
  - 2–3 runs per task.
  
  Tigran's blind read or real generations would settle it.
