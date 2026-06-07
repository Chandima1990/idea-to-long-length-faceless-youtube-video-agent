"""Local image generation through a running ComfyUI server.

Mirrors the interface of gathos_client / gemini_client so it can be selected
transparently via IMAGE_PROVIDER=comfyui (see lib/image_provider.py).

How prompt injection works
--------------------------
ComfyUI's HTTP API takes a workflow JSON (the "API format" export). Rather than
hard-coding node IDs, this client does string-level token replacement on that
JSON before submitting. Export your workflow once (Save (API Format)), then edit
the text fields so they contain the tokens below:

    __PROMPT__    -> replaced with the scene's image prompt (REQUIRED, positive node)
    __NEGATIVE__  -> replaced with COMFYUI_NEGATIVE_PROMPT (optional)
    __SEED__      -> replaced with a fresh random seed each image (optional)
    __WIDTH__     -> replaced with the requested width  (optional)
    __HEIGHT__    -> replaced with the requested height (optional)

Token names are configurable in lib/config.py / .env.
"""

import json
import random
import time
from pathlib import Path

import requests

from lib.config import (
    COMFYUI_BASE_URL,
    COMFYUI_WORKFLOW_PATH,
    COMFYUI_UPSCALE_WORKFLOW_PATH,
    COMFYUI_PROMPT_TOKEN,
    COMFYUI_NEG_TOKEN,
    COMFYUI_SEED_TOKEN,
    COMFYUI_WIDTH_TOKEN,
    COMFYUI_HEIGHT_TOKEN,
    COMFYUI_NEGATIVE_PROMPT,
    COMFYUI_POLL_INTERVAL,
    COMFYUI_TIMEOUT,
    GATHOS_IMAGE_WIDTH,
    GATHOS_IMAGE_HEIGHT,
)


def _load_workflow_text() -> str:
    path = Path(COMFYUI_WORKFLOW_PATH)
    if not path.exists():
        raise FileNotFoundError(
            f"ComfyUI workflow not found at {path}. Export your workflow from "
            f"ComfyUI as 'Save (API Format)', add the {COMFYUI_PROMPT_TOKEN} token "
            f"to your positive prompt node, and set COMFYUI_WORKFLOW_PATH in .env."
        )
    return path.read_text(encoding="utf-8")


def _json_escape(text: str) -> str:
    # Escape so the value can be dropped inside an existing JSON string literal
    # (json.dumps wraps in quotes; strip them off).
    return json.dumps(text, ensure_ascii=False)[1:-1]


def _build_workflow(prompt: str, width: int, height: int) -> dict:
    raw = _load_workflow_text()
    if COMFYUI_PROMPT_TOKEN not in raw:
        raise ValueError(
            f"Token {COMFYUI_PROMPT_TOKEN!r} not found in workflow "
            f"{COMFYUI_WORKFLOW_PATH}. Add it to your positive prompt node's text."
        )
    raw = raw.replace(COMFYUI_PROMPT_TOKEN, _json_escape(prompt))
    raw = raw.replace(COMFYUI_NEG_TOKEN, _json_escape(COMFYUI_NEGATIVE_PROMPT))
    raw = raw.replace(COMFYUI_SEED_TOKEN, str(random.randint(1, 2_147_483_646)))
    raw = raw.replace(COMFYUI_WIDTH_TOKEN, str(width))
    raw = raw.replace(COMFYUI_HEIGHT_TOKEN, str(height))
    return json.loads(raw)


def _submit(workflow: dict) -> str:
    resp = requests.post(
        f"{COMFYUI_BASE_URL}/prompt",
        json={"prompt": workflow},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    prompt_id = data.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI rejected the workflow: {data}")
    return prompt_id


def _poll_for_image(prompt_id: str) -> bytes:
    start = time.time()
    while time.time() - start < COMFYUI_TIMEOUT:
        try:
            resp = requests.get(f"{COMFYUI_BASE_URL}/history/{prompt_id}", timeout=30)
            resp.raise_for_status()
            history = resp.json()
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"    Poll network error (will retry): {e}")
            time.sleep(COMFYUI_POLL_INTERVAL)
            continue

        entry = history.get(prompt_id)
        if entry:
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI job {prompt_id} failed: {status}")
            for node_output in entry.get("outputs", {}).values():
                images = node_output.get("images", [])
                if images:
                    img = images[0]
                    return _download_image(
                        img["filename"], img.get("subfolder", ""), img.get("type", "output")
                    )
        time.sleep(COMFYUI_POLL_INTERVAL)
    raise TimeoutError(f"ComfyUI job {prompt_id} timed out after {COMFYUI_TIMEOUT}s")


def _download_image(filename: str, subfolder: str, folder_type: str) -> bytes:
    resp = requests.get(
        f"{COMFYUI_BASE_URL}/view",
        params={"filename": filename, "subfolder": subfolder, "type": folder_type},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.content


def generate_image(
    prompt: str,
    output_path: Path,
    width: int = GATHOS_IMAGE_WIDTH,
    height: int = GATHOS_IMAGE_HEIGHT,
) -> Path:
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping (exists): {output_path.name}")
        return output_path
    workflow = _build_workflow(prompt, width, height)
    prompt_id = _submit(workflow)
    print(f"  ComfyUI job submitted: {prompt_id}")
    image_bytes = _poll_for_image(prompt_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)
    print(f"  Saved: {output_path.name}")
    return output_path


def _upload_image(path: Path) -> str:
    """Upload a local image into ComfyUI's input folder; return its reference name."""
    path = Path(path)
    with open(path, "rb") as fh:
        resp = requests.post(
            f"{COMFYUI_BASE_URL}/upload/image",
            files={"image": (path.name, fh, "image/png")},
            data={"type": "input", "overwrite": "true"},
            timeout=120,
        )
    resp.raise_for_status()
    info = resp.json()
    name = info["name"]
    if info.get("subfolder"):
        name = f"{info['subfolder']}/{name}"
    return name


def upscale_image(input_path: Path, output_path: Path, width: int = 1920, height: int = 1080) -> Path:
    """Enlarge an existing image with 4x-UltraSharp (no diffusion — content is preserved),
    then resize to width x height. Used for the ChatGPT-2x2-collage -> split -> upscale path."""
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping (exists): {output_path.name}")
        return output_path

    wf_path = Path(COMFYUI_UPSCALE_WORKFLOW_PATH)
    if not wf_path.exists():
        raise FileNotFoundError(f"Upscale workflow not found at {wf_path}")

    uploaded = _upload_image(input_path)
    raw = wf_path.read_text(encoding="utf-8")
    raw = raw.replace("__IMAGE__", _json_escape(uploaded))
    raw = raw.replace("__WIDTH__", str(width)).replace("__HEIGHT__", str(height))
    workflow = json.loads(raw)

    prompt_id = _submit(workflow)
    print(f"  Upscale job submitted: {prompt_id}")
    image_bytes = _poll_for_image(prompt_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)
    print(f"  Saved: {output_path.name} ({width}x{height})")
    return output_path


def generate_images_batch(prompts: list[dict], output_dir: Path) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    total = len(prompts)
    for i, p in enumerate(prompts):
        out = output_dir / p["filename"]
        w = p.get("width", GATHOS_IMAGE_WIDTH)
        h = p.get("height", GATHOS_IMAGE_HEIGHT)
        print(f"  [{i+1}/{total}] Generating: {out.name}")
        generate_image(p["prompt"], out, w, h)
        results.append(out)
    return results
