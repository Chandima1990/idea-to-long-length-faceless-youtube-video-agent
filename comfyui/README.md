# Local image generation via ComfyUI

This lets the pipeline generate B-roll/thumbnail images on your own machine
(Flux.2 Klein or any workflow) instead of paying Gathos/Gemini. Gathos and
Gemini stay available — this is just a third option you flip on per run.

## One-time setup

1. **Start ComfyUI** with your Flux workflow loaded and confirm it renders a test
   image. Note the server address (default `http://127.0.0.1:8188`).

2. **Export the workflow in API format:**
   - ComfyUI → Settings (gear) → enable **Dev mode**.
   - Menu → **Save (API Format)**.
   - Save the file here as `comfyui/workflow_api.json`
     (or anywhere, and point `COMFYUI_WORKFLOW_PATH` at it in `.env`).

3. **Insert tokens** into that JSON (open it in a text editor). The client does a
   plain find-and-replace before each render, so you do NOT need to know node IDs:

   | Token          | Put it in...                                   | Required |
   |----------------|------------------------------------------------|----------|
   | `__PROMPT__`   | the **positive** CLIP-text node's `text` field | **Yes**  |
   | `__NEGATIVE__` | the negative CLIP-text node's `text` field     | No       |
   | `__SEED__`     | the sampler's `seed` field (gets a fresh value)| No       |
   | `__WIDTH__`    | EmptyLatentImage `width`                        | No       |
   | `__HEIGHT__`   | EmptyLatentImage `height`                       | No       |

   Example — a positive prompt node becomes:
   ```json
   "inputs": { "text": "__PROMPT__", "clip": ["4", 1] }
   ```
   `__SEED__`, `__WIDTH__`, `__HEIGHT__` are numbers, so write them unquoted:
   ```json
   "inputs": { "seed": __SEED__, "width": __WIDTH__, "height": __HEIGHT__, ... }
   ```
   Leave any token out and the pipeline just uses whatever your workflow already
   has baked in (fixed seed, fixed size, etc.).

4. **Switch the provider on** in `.env`:
   ```
   IMAGE_PROVIDER=comfyui
   COMFYUI_BASE_URL=http://127.0.0.1:8188
   COMFYUI_WORKFLOW_PATH=comfyui/workflow_api.json
   # optional:
   COMFYUI_NEGATIVE_PROMPT=text, watermark, blurry, extra fingers, deformed
   ```

To go back to cloud, set `IMAGE_PROVIDER=gathos` (or `gemini`). That's the only
switch — no code changes.

## How prompts are written for Flux

When `IMAGE_PROVIDER=comfyui`, image prompts must respect Flux's quirks (number
and table hallucination, layout). See
[`skills/flux-image-prompting.md`](../skills/flux-image-prompting.md). Those are
technical limits layered ON TOP of the active channel's art style — they don't
replace it.

## Notes

- Images generate one at a time (ComfyUI queues internally; sequential keeps VRAM
  predictable and ordering stable for `scene_001.png` … `scene_NNN.png`).
- Output is fetched via ComfyUI's `/view` endpoint, so your SaveImage node can
  write wherever — the pipeline pulls the bytes and writes them into
  `outputs/<run>/images/` itself.
