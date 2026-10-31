---
name: jackvsai-fashion-campaign-prompt-framework
description: "Generate high-energy multi-shot AI video prompts for streetwear or editorial fashion campaigns built around a garment, outfit, styled look, or fashion reference image. Do not use for non-fashion video prompts."
metadata:
  version: 1.1.0
---

# JACKVSAI Fashion Campaign Prompt Framework

This skill generates high-energy multi-shot video prompts for streetwear and editorial fashion campaigns — structured as timed shot sequences built around garment-led storytelling, fast cuts, handheld camera energy, constant model movement, bold direct-to-camera attitude, and heavy use of negative space.

Use this for: streetwear prompts, fashion campaign prompts, editorial prompts, shot sequences for an outfit, cinematic direction from a fashion reference image, garment-led ads, negative space fashion videos, attitude beats, macro fabric detail, and urban editorial energy.

Route elsewhere for: general video prompts (`cinema-worldbuilder-pro-2.0`), 5-stage narrative shorts (`shortfilm-prompt`), or Higgsfield platform/model/credit questions (`higgsfield`).

**Hard rule: the final prompt must be 1,000 characters or fewer.** Non-negotiable. This is a compressed format designed for AI video generators with strict prompt-length limits.

---

## Workflow

### Step 1 — Analyze the reference image

The garment is the hero. Extract a compact visual description prioritising the clothes, not the person wearing them. Cover:

- **Garment details** — silhouette, cut, fabric type, colorway, construction details (seams, hardware, logo placement, texture, fit)
- **Styling** — layering, accessories, footwear if visible, how pieces are worn (oversized, cropped, open, belted, tucked)
- **Model energy** — build, skin tone, hair, any distinctive features; their vibe in the reference (slouched cool, upright, candid, relaxed)

If no image has been uploaded, ask for one. The reference is the visual anchor for everything that follows.

If the reference is a flat lay or product shot with no model, note it and proceed — the model will be implied or generic.

---

### Step 2 — Gather the brief

Ask for all of the following in a single message, unless the user has already provided them:

1. **Subject** — who is the model? (default: infer from reference or use a generic descriptor like "a young woman")
2. **Action** — what are they doing? Every shot must contain model movement — even minimal. Defaults: slow body turn, weight shift between feet, casual walk, leaning push-off. (Required but low bar — "standing" becomes a subtle sway or shift.)
3. **Location** — where? Urban default. Street, rooftop, car park, underpass, empty lot, stairwell, studio void — all valid.
4. **Expression / attitude** — bold/confident, sassy, confrontational, unbothered (default: bold direct eye contact into lens)
5. **Lighting mood** — harsh midday, overcast flat light, golden hour, fluorescent interior, night with practicals (default: overcast urban)

If the user provides these inline with their request, skip the questions and proceed directly.

---

### Step 3 — Design the shot sequence

Build a sequence totalling **exactly 15 seconds**. Streetwear editorial is fast and punchy by default:

- **Default to 6–7 shots** at **2–3 seconds each** (maximum 4 seconds per shot — tighter ceiling than standard cinematic work)
- **Mandatory: every shot must include model movement** — name it explicitly in the copy. Range from subtle (shifting weight, slow chin raise, fingers brushing fabric) to full-body (turn, stride, lean push-off). No shot where the model is completely static.
- **Mandatory: at least one negative space wide** — subject occupying ≤30% of frame, architecture, sky, or empty ground dominant
- **Mandatory: at least one bold attitude beat** — model staring directly and confidently into the lens; name this explicitly ("locks eyes with camera, chin lifted, expression charged", "direct eye contact, jaw set, unflinching")
- **Handheld or shaky handheld is the default camera movement** — static camera is allowed only when the model's own movement carries the shot
- **Cut to.** between every shot

For each shot, specify all four technical parameters:

1. **Shot size** — ultra-wide / wide / medium / close-up / extreme close-up / macro
2. **Lens** — 16mm, 24mm, 35mm, 50mm, 85mm (or macro equivalent)
3. **Camera angle** — worm's eye, low angle, eye-level, high angle, bird's eye, dutch angle
4. **Camera movement** — shaky handheld, handheld, snap pan, whip pan, push in, pull out, tracking, orbit, static

Vary all four across the sequence. Consecutive shots must shift perspective — the edit should feel driven, not drifting.

---

### Step 4 — Write the prompt

Output the entire sequence as **one flowing paragraph**. No line breaks, no lists, no markdown, no numbered shots.

Distribute garment references across the sequence — mention silhouette in wides, hardware or texture in close-ups, colorway against environment in establishing shots. After the first shot, use "she", "he", "they", or "the model" for subject references to save characters.

**Always end with this exact line:**
`Gritty realism, natural framing. Audio: diegetic sound only — urban ambience, footsteps, fabric movement, environmental foley.`

This line is non-negotiable (~108 chars). Plan for it in the budget.

---

### Step 5 — Count and deliver

Count the final prompt characters. If over 1,000, trim in this order:

1. **Compress atmospheric padding** — "warm golden light spills softly across" → "warm rim light across"
2. **Merge shared location elements** — state environment once, reference it after
3. **Shorten subject references** — "she" / "the model" after first mention
4. **Shorten garment references** — "the jacket" after the first full description
5. **Drop lens mm last resort only** — it informs the render; cut adjectives before cutting specs
6. **Never cut:** shot size / angle / movement specs, the model movement descriptor in each shot, the negative space wide, the attitude eye-contact beat, or the closing audio line

Output the prompt in a **single fenced code block** — no commentary inside it.

Below the code block, add 2–3 sentences max: the shot structure logic, and one suggested tweak if the first generation doesn't land.

---

## Shot vocabulary for streetwear editorial

These are the primary building blocks. Mix freely:

- **Negative space wide** — ultra-wide or wide, subject ≤30% of frame, urban environment dominant, model small and deliberate against scale; model still moving — a slow turn, a shift, a step
- **Attitude lock** — medium or close-up, slow push in or static camera, model in direct bold eye contact with lens; movement is in the body — weight shift, chin raise, shoulder roll
- **Candid mid-motion** — medium or medium-wide, handheld, model mid-step or mid-turn, energy in the movement, clothes reacting to the body
- **Environmental anchor** — medium-wide, model moving within the space — pushing off a wall, stepping away from a surface, turning through the environment rather than posing in front of it
- **Silhouette wide** — wide or ultra-wide, strong backlight or side light, model in full-body motion against sky or open space, garment silhouette reading in movement

---

## Expression palette

Use these directly in prompt copy:

| Attitude | Prompt language |
|---|---|
| Bold / confident *(default)* | direct eye contact into lens, chin level or lifted, expression charged and present |
| Sassy | chin lifted, slight smirk, eye contact held with casual superiority |
| Confrontational | unblinking direct eye contact, body still within movement, charged stillness |
| Unbothered | gaze drifting past camera, posture relaxed, expression doing nothing — movement carries it |

---

## Lighting language

Name the light setup, not just the time of day:

| Mood | Prompt language |
|---|---|
| Harsh midday | hard directional sun, graphic shadow, high contrast |
| Overcast urban | even diffuse grey light, no shadow, clean fabric read |
| Golden hour | warm rim light, long ground shadow, deep colorway saturation |
| Fluorescent interior | cool flat top light, slight overexposure on pale fabric |
| Night / practicals | pools of warm streetlight, deep shadow fill, neon bleed |

---

## Example

**User uploads image of a model in an oversized olive cargo jacket, black wide-leg trousers, and chunky white sneakers. Brief: "standing outside a multi-storey car park, overcast, bold."**

```
Ultra-wide shot, 16mm, worm's eye, shaky handheld — a figure in an oversized olive cargo jacket and black wide-leg trousers stands beneath the raw concrete lip of a multi-storey car park, even grey light killing all shadow, subject small against the structure, slowly turning to face camera, 3 seconds. Cut to. Medium shot, 35mm, eye-level, handheld — she steps forward, jacket shifting at the shoulder, direct eye contact into lens, chin level, expression charged, 2 seconds. Cut to. Wide shot, 24mm, dutch angle, tracking — she moves parallel to the concrete wall, wide-leg trousers breaking over a chunky white sole, full silhouette against raw grey, glancing back at camera over her shoulder, 3 seconds. Cut to. Close-up, 50mm, low angle, slow push in — she shifts her weight forward, locks eyes with camera, jaw set, chin lifted, unflinching, 3 seconds. Cut to. Medium-wide shot, 35mm, high angle, shaky handheld — she turns a slow full rotation in the open concourse, jacket hem lifting, gaze finding the lens mid-turn, 2 seconds. Cut to. Wide shot, 16mm, eye-level, pull out — she steps toward camera, growing in frame, expression bold and direct, architecture receding behind her, 2 seconds. Gritty realism, natural framing. Audio: diegetic sound only — urban ambience, footsteps, fabric movement, environmental foley.
```

6 shots — opens small in the space, builds through attitude close-ups, closes on a direct advance toward camera. If the tracking shot in shot 3 loses the silhouette read, change the background to "pale overcast sky at the open end of the level."

---

## Handling variations

**Minimal action brief.** Default to slow turn, weight shift, or lean push-off. The model is always moving — even the quietest shot has a breath, a shift, a glance. Don't describe stillness.

**Multiple garment pieces to feature.** Distribute shots so each hero piece appears in at least one mid-shot or close-up while the model is in motion — jacket reacting to a turn, trousers breaking over a step, accessories catching light as the head moves.

**Studio void.** Negative space becomes the entire environment. The model's movement is everything — a slow turn in deep white space, a step toward camera from black. Garment colorway and silhouette-in-motion are the only visual anchors.

**Two models.** Use over-shoulder and side-by-side framing in the wides, both moving. Each model gets their own attitude beat — direct eye contact, their own charged moment. Let their movements have relationship: one turning as the other steps forward.

**Night / artificial light.** Slow the handheld on wide shots — let practical lights (streetlamps, shop windows, neon) create pools the model moves through. Movement through light and shadow hits harder than any static pose.

**Monochrome or tonal looks.** When the garment has minimal colorway contrast, let the model's movement do the work — fabric in motion, silhouette shifting, clothes reacting to the body. Strong environmental contrast (pale sky, dark ground) keeps the silhouette readable through the movement.
