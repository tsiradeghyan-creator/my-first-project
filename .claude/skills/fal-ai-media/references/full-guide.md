---
name: fal-ai-media
description: Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance 2.5, Kling v3, Veo 3.1), text-to-speech, and video-to-audio. Use when the user wants to generate images, videos, or audio with AI.
origin: ECC
---

# fal.ai Media Generation

Generate images, videos, and audio using fal.ai models via MCP.

Model ids and parameters below were checked on fal.ai model pages (`https://fal.ai/models/<id>/llms.txt`) on 2026-11-26. They drift: confirm with `get_model_schema` before a paid run.

## When to Activate

- User wants to generate images from text prompts
- Creating videos from text or images
- Generating speech, music, or sound effects
- Any media generation task
- User says "generate image", "create video", "text to speech", "make a thumbnail", or similar

## Before Any Image or Video Prompt

Before writing a prompt, run `film-crew` (single-shot mode for one shot, full mode for several) per CLAUDE.md, and take its plan as input. If a film-crew plan already exists, use it. The model skill (`seedance-25-director`, `banana-pro-director-2.0`, `cinema-worldbuilder-pro-2.0`…) then writes the final prompt text; this skill only sends it to fal.

## MCP Requirement

### Official hosted fal MCP (recommended)

fal runs its own hosted MCP server (docs: https://fal.ai/docs/documentation/setting-up/mcp):

- URL: `https://mcp.fal.ai/mcp-relay`, transport Streamable HTTP, auth OAuth (browser sign-in). No API key or Authorization header is needed for this connection.
- Claude Code: `claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay`, then run `/mcp`, select `fal`, choose **Authenticate**.
- On claude.ai, add fal as a connector and sign in through the browser.
- Generations bill the **Active MCP account** chosen at https://fal.ai/dashboard/ai-tools.
- A separate documentation-only server, `https://fal.ai/docs/mcp`, searches fal docs without running models.

Official tools:

| Tool | What it does |
|------|--------------|
| `search_models` | Search the model catalog by keyword or category |
| `get_model_schema` | A model's input and output parameters (call before `run_model`) |
| `get_pricing` | Model pricing before generation |
| `search_docs` | Search fal documentation |
| `recommend_model` | Find models for a task |
| `run_model` | Run a model with a bounded wait (about 45 s); returns the result or a request ID |
| `submit_job` | Submit a long job (video, 3D) and return its request ID |
| `check_job` | Check an existing job |
| `get_job_result` | Retrieve a completed job's output |
| `cancel_job` | Cancel a queued or running job |
| `upload_file` | Prepare a signed upload, or upload a public URL or base64 data |

`run_model` and `submit_job` take `endpoint_id` and `input`. For video, use `submit_job` → `check_job` → `get_job_result` from the start. Do not resubmit to check progress: each new `run_model` / `submit_job` call is a new billable job. fal notes that tool availability can change; the client's tool list is the source of truth.

### Third-party server (legacy, only if installed)

The laptop's `~/.claude.json` has used the third-party npm package `fal-ai-mcp-server` (`npx -y fal-ai-mcp-server` with `FAL_KEY` in env; see `skills/zavod-craft/fal-setup.md` in the zavod-om repo). It is not fal's official server. Its tool names apply only when that package is the one installed:

| Third-party tool | Official equivalent |
|------------------|---------------------|
| `search` | `search_models` |
| `find` | `get_model_schema` |
| `models` | `search_models` / `recommend_model` |
| `generate` (`app_id`, `input_data`) | `run_model` / `submit_job` (`endpoint_id`, `input`) |
| `status`, `result` | `check_job`, `get_job_result` |
| `cancel` | `cancel_job` |
| `upload` | `upload_file` |
| `estimate_cost`, `pricing` | `get_pricing` |

Check which server is connected (tool list) before calling. Examples below use the official names.

---

## Image Generation

### Nano Banana 2 (Fast)
Best for: quick iterations, drafts, text-to-image.

```
run_model(
  endpoint_id: "fal-ai/nano-banana-2",
  input: {
    "prompt": "a futuristic cityscape at sunset, cyberpunk style",
    "aspect_ratio": "16:9",
    "resolution": "1K",
    "num_images": 1,
    "seed": 42
  }
)
```

### Nano Banana Pro (High Fidelity)
Best for: production images, realism, typography, detailed prompts.

```
run_model(
  endpoint_id: "fal-ai/nano-banana-pro",
  input: {
    "prompt": "professional product photo of wireless headphones on marble surface, studio lighting",
    "aspect_ratio": "1:1",
    "resolution": "2K",
    "num_images": 1
  }
)
```

### Common Image Parameters (Nano Banana 2 / Pro)

| Param | Type | Options | Notes |
|-------|------|---------|-------|
| `prompt` | string | required | Describe what you want |
| `aspect_ratio` | string | `auto`, `21:9`, `16:9`, `3:2`, `4:3`, `5:4`, `1:1`, `4:5`, `3:4`, `2:3`, `9:16`, `4:1`, `1:4`, `8:1`, `1:8` | Pro defaults to `1:1`, Nano Banana 2 to `auto` |
| `resolution` | string | `1K`, `2K`, `4K` (Nano Banana 2 also `0.5K`) | Default `1K` |
| `num_images` | number | default 1 | How many to generate |
| `seed` | number | any integer | Reproducibility |
| `output_format` | string | `png`, `jpeg`, `webp` | Default `png` |

There is no `image_size` or `guidance_scale` on these models.

### Image Editing
Use the `/edit` endpoint with one or more input images:

```
# First upload the source image. The hosted server cannot read a local path:
# for a local file up to 90 MB, call upload_file(prepare_upload: true, file_name: "image.png", file_size: <bytes>),
# PUT the bytes to the returned upload_url, then use file_url.
# For a public URL: upload_file(url: "https://...") returns a cdn_url.

# Then edit with the image input
run_model(
  endpoint_id: "fal-ai/nano-banana-2/edit",
  input: {
    "prompt": "same scene but in watercolor style",
    "image_urls": ["<uploaded_url>"],
    "aspect_ratio": "auto"
  }
)
```

`fal-ai/nano-banana-pro/edit` takes the same `image_urls` list for higher-fidelity edits.

---

## Video Generation

For video prompt wording, limits and Seedance syntax, use the `seedance-25-director` skill (after film-crew); the blocks below only show the fal call.

### Seedance 2.5 (ByteDance), default
Best for: text-to-video and image-to-video, native synced audio, up to 30 s, up to 4K.

Text-to-video:

```
submit_job(
  endpoint_id: "bytedance/seedance-2.5/text-to-video",
  input: {
    "prompt": "a drone flyover of a mountain lake at golden hour, cinematic",
    "duration": "8",
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "generate_audio": true
  }
)
```

Image-to-video:

```
submit_job(
  endpoint_id: "bytedance/seedance-2.5/image-to-video",
  input: {
    "prompt": "camera slowly zooms out, gentle wind moves the trees",
    "image_url": "<uploaded_image_url>",
    "duration": "5",
    "resolution": "720p"
  }
)
```

Seedance 2.5 on fal:
- `duration`: `"auto"` (default) or `"4"` … `"30"` (a number as a string, no `s`).
- `resolution`: `480p`, `720p` (default), `1080p`, `4k`. `draft: true` makes a cheap 480p preview with a `draft_id` that can be finished at 1080p/4K within 14 days.
- `aspect_ratio` (text-to-video): `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`. Image-to-video always uses `auto`.
- Image-to-video also takes `end_image_url` for a last frame.
- No `seed` input; the seed comes back in the output.
- Other endpoints listed by fal: `bytedance/seedance-2.5/reference-to-video`, plus `flash/` and `us/` variants (check with `get_model_schema` before use).

### Kling Video v3 Pro
Best for: text/image-to-video with native audio, multi-shot.

```
submit_job(
  endpoint_id: "fal-ai/kling-video/v3/pro/text-to-video",
  input: {
    "prompt": "ocean waves crashing on a rocky coast, dramatic clouds",
    "duration": "5",
    "aspect_ratio": "16:9"
  }
)
```

Image-to-video uses `fal-ai/kling-video/v3/pro/image-to-video` with `start_image_url` (required) and optional `end_image_url`; it has no `aspect_ratio`. Kling v3 `duration` is `"3"` … `"15"` (default `"5"`); `aspect_ratio` is `16:9`, `9:16` or `1:1`. Kling 4.0 exists in the Kling app, but no API was announced as of 2026-11-26.

### Veo 3.1 (Google DeepMind)
Best for: video with generated sound, high visual quality.

```
submit_job(
  endpoint_id: "fal-ai/veo3.1",
  input: {
    "prompt": "a bustling Tokyo street market at night, neon signs, crowd noise",
    "aspect_ratio": "16:9",
    "duration": "8s",
    "resolution": "1080p"
  }
)
```

Veo 3.1 `duration` keeps the `s`: `"4s"`, `"6s"`, `"8s"` (default). `aspect_ratio`: `16:9` or `9:16`. `resolution`: `720p`, `1080p`, `4k`. Image-to-video: `fal-ai/veo3.1/image-to-video` with `image_url`.

### Video Parameters at a Glance

| Model | `duration` format | `aspect_ratio` | Image input |
|-------|-------------------|----------------|-------------|
| Seedance 2.5 | `"auto"`, `"4"`–`"30"` | `auto`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` | `image_url` (+ `end_image_url`) |
| Kling v3 Pro | `"3"`–`"15"` | `16:9`, `9:16`, `1:1` | `start_image_url` (+ `end_image_url`) |
| Veo 3.1 | `"4s"`, `"6s"`, `"8s"` | `16:9`, `9:16` | `image_url` |

---

## Audio Generation

### CSM-1B (Conversational Speech) (verify live)
Text-to-speech with natural, conversational quality. `fal-ai/csm-1b` was not found in the fal catalog on 2026-11-26; search with `search_models(category: "text-to-speech")` first.

```
run_model(
  endpoint_id: "fal-ai/csm-1b",
  input: {
    "text": "Hello, welcome to the demo. Let me show you how this works.",
    "speaker_id": 0
  }
)
```

### ThinkSound (Video-to-Audio) (verify live)
Generate matching audio from video content. `fal-ai/thinksound` was not found in the fal catalog on 2026-11-26; search for a current video-to-audio model first.

```
run_model(
  endpoint_id: "fal-ai/thinksound",
  input: {
    "video_url": "<video_url>",
    "prompt": "ambient forest sounds with birds chirping"
  }
)
```

### ElevenLabs (via API, no MCP)
For professional voice synthesis, use ElevenLabs directly:

```python
import os
import requests

resp = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>",
    headers={
        "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
        "Content-Type": "application/json"
    },
    json={
        "text": "Your text here",
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
)
with open("output.mp3", "wb") as f:
    f.write(resp.content)
```

### VideoDB Generative Audio
If VideoDB is configured, use its generative audio:

```python
# Voice generation
audio = coll.generate_voice(text="Your narration here", voice="alloy")

# Music generation
music = coll.generate_music(prompt="upbeat electronic background music", duration=30)

# Sound effects
sfx = coll.generate_sound_effect(prompt="thunder crack followed by rain")
```

---

## Cost Estimation

Before generating, check pricing:

```
get_pricing(endpoint_id: "fal-ai/nano-banana-pro,bytedance/seedance-2.5/text-to-video")
```

On the third-party server the equivalent is `estimate_cost(estimate_type: "unit_price", endpoints: {"fal-ai/nano-banana-pro": {"unit_quantity": 1}})`.

Reference point (fal page, 2026-11-26): Seedance 2.5 costs roughly $0.22/s at 480p, $0.47/s at 720p, $1.16/s at 1080p and $1.84/s at 4K. Prices change; check before each paid run.

## Model Discovery

Find models for specific tasks:

```
search_models(query: "text to video")
search_models(category: "text-to-video")
get_model_schema(endpoint_id: "bytedance/seedance-2.5/text-to-video")
recommend_model(task: "create a 10s cinematic video")
```

## Tips

- Use `seed` for reproducible results when iterating on prompts (where the model accepts it; Seedance 2.5 does not)
- Start with lower-cost settings (Nano Banana 2, Seedance `draft: true` or 480p) for prompt iteration, then switch to Pro / higher resolution for finals
- For video, keep prompts descriptive but concise — focus on motion and scene
- Image-to-video produces more controlled results than pure text-to-video
- Check pricing before running expensive video generations

## Related Skills

- `film-crew` — runs first for every image or video prompt
- `seedance-25-director`, `banana-pro-director-2.0`, `cinema-worldbuilder-pro-2.0` — write the final prompt text
- `videodb` — Video processing, editing, and streaming
- `video-editing` — AI-powered video editing workflows
- `content-engine` — Content creation for social platforms
