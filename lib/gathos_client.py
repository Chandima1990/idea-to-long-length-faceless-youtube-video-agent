import base64
import time
from pathlib import Path

import requests

from lib.config import (
    GATHOS_BASE_URL,
    GATHOS_IMAGE_API_KEY,
    GATHOS_TTS_API_KEY,
    GATHOS_IMAGE_HEIGHT,
    GATHOS_IMAGE_WIDTH,
    GATHOS_MAX_RETRIES,
    GATHOS_IMAGE_MAX_RETRIES,
    GATHOS_POLL_INTERVAL,
    GATHOS_TIMEOUT,
    GATHOS_TTS_POLL_INTERVAL,
)


def _image_headers():
    return {"Authorization": f"Bearer {GATHOS_IMAGE_API_KEY}", "Content-Type": "application/json"}


def _tts_headers():
    return {"Authorization": f"Bearer {GATHOS_TTS_API_KEY}", "Content-Type": "application/json"}


def submit_image_job(prompt: str, width: int = GATHOS_IMAGE_WIDTH, height: int = GATHOS_IMAGE_HEIGHT) -> str:
    last_exc = None
    for attempt in range(GATHOS_IMAGE_MAX_RETRIES):
        try:
            resp = requests.post(
                f"{GATHOS_BASE_URL}/image-generation",
                headers=_image_headers(),
                json={"prompt": prompt, "width": width, "height": height},
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json()["job_id"]
        except Exception as e:
            last_exc = e
            status = getattr(getattr(e, "response", None), "status_code", None)
            wait = 90 * (attempt + 1) if status == 429 else 15 * (attempt + 1)
            if attempt < GATHOS_IMAGE_MAX_RETRIES - 1:
                print(f"    Retry {attempt+1}/{GATHOS_IMAGE_MAX_RETRIES} after error: {e} (waiting {wait}s)")
                time.sleep(wait)
    raise last_exc


def poll_image_job(job_id: str) -> str:
    start = time.time()
    while time.time() - start < GATHOS_TIMEOUT:
        try:
            resp = requests.get(
                f"{GATHOS_BASE_URL}/image-generation/jobs/{job_id}",
                headers=_image_headers(),
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "completed":
                result = data.get("result", {})
                return result.get("image_base64", result.get("image", ""))
            if data.get("status") == "failed":
                raise RuntimeError(f"Image job {job_id} failed: {data}")
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"    Poll network error (will retry): {e}")
        time.sleep(GATHOS_POLL_INTERVAL)
    raise TimeoutError(f"Image job {job_id} timed out after {GATHOS_TIMEOUT}s")


def generate_image(prompt: str, output_path: Path, width: int = GATHOS_IMAGE_WIDTH, height: int = GATHOS_IMAGE_HEIGHT) -> Path:
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping (exists): {output_path.name}")
        return output_path
    job_id = submit_image_job(prompt, width, height)
    print(f"  Image job submitted: {job_id}")
    b64 = poll_image_job(job_id)
    output_path.write_bytes(base64.b64decode(b64))
    print(f"  Saved: {output_path.name}")
    return output_path


def generate_images_batch(prompts: list[dict], output_dir: Path) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process one at a time to stay within the 2-concurrent API limit
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


def submit_tts_job(text: str, voice: str) -> str:
    for attempt in range(GATHOS_MAX_RETRIES):
        try:
            resp = requests.post(
                f"{GATHOS_BASE_URL}/tts",
                headers=_tts_headers(),
                json={"text": text, "voice": voice},
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["job_id"]
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as e:
            if attempt < GATHOS_MAX_RETRIES - 1:
                wait = 15 * (attempt + 1)
                print(f"    Retry {attempt+1}/{GATHOS_MAX_RETRIES} after error: {e} (waiting {wait}s)")
                time.sleep(wait)
            else:
                raise


def poll_tts_job(job_id: str) -> str:
    start = time.time()
    while time.time() - start < GATHOS_TIMEOUT:
        resp = requests.get(
            f"{GATHOS_BASE_URL}/tts/jobs/{job_id}",
            headers=_tts_headers(),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "completed":
            result = data.get("result", {})
            return result.get("audio_base64", result.get("audio_wav", result.get("audio", "")))
        if data.get("status") == "failed":
            raise RuntimeError(f"TTS job {job_id} failed: {data}")
        time.sleep(GATHOS_TTS_POLL_INTERVAL)
    raise TimeoutError(f"TTS job {job_id} timed out after {GATHOS_TIMEOUT}s")


def generate_tts(text: str, voice: str, output_path: Path) -> Path:
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping (exists): {output_path.name}")
        return output_path
    job_id = submit_tts_job(text, voice)
    print(f"  TTS job submitted: {job_id}")
    b64 = poll_tts_job(job_id)
    output_path.write_bytes(base64.b64decode(b64))
    print(f"  Saved: {output_path.name}")
    return output_path
