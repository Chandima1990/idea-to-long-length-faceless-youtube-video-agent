"""Image generation through OpenAI gpt-image-1 (the same engine as ChatGPT's image
tool — best-in-class text/layout). Mirrors the gathos/gemini/comfyui interface so it
can be used as IMAGE_PROVIDER=openai (1 scene per image), and also exposes generate_image
directly for the 2x2-collage workflow (see openai_collages.py)."""

import base64
import time
from pathlib import Path

from lib.config import (
    OPENAI_API_KEY,
    OPENAI_IMAGE_MODEL,
    OPENAI_IMAGE_SIZE,
    OPENAI_IMAGE_QUALITY,
)


def _client():
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY)


def generate_image(prompt: str, output_path: Path, size: str = None, quality: str = None,
                   max_retries: int = 4) -> Path:
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping (exists): {output_path.name}")
        return output_path

    client = _client()
    size = size or OPENAI_IMAGE_SIZE
    quality = quality or OPENAI_IMAGE_QUALITY

    last_exc = None
    for attempt in range(max_retries):
        try:
            resp = client.images.generate(
                model=OPENAI_IMAGE_MODEL,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )
            b64 = resp.data[0].b64_json  # gpt-image-1 always returns base64
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(base64.b64decode(b64))
            print(f"  Saved: {output_path.name} ({size}, {quality})")
            return output_path
        except Exception as e:
            last_exc = e
            # Only retry transient errors (rate limit / network / 5xx). Fail fast on
            # permanent 400s like billing-limit, content-policy, or invalid request.
            status = getattr(e, "status_code", None)
            permanent = status is not None and 400 <= status < 500 and status != 429
            if permanent or attempt >= max_retries - 1:
                raise last_exc
            wait = 10 * (attempt + 1)
            print(f"    Retry {attempt + 1}/{max_retries} in {wait}s: {e}")
            time.sleep(wait)
    raise last_exc


def generate_images_batch(prompts: list, output_dir: Path) -> list:
    """1-scene-per-image provider interface (IMAGE_PROVIDER=openai)."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for i, p in enumerate(prompts):
        out = output_dir / p["filename"]
        print(f"  [{i + 1}/{len(prompts)}] Generating: {out.name}")
        generate_image(p["prompt"], out)
        results.append(out)
    return results
