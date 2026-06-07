import time
from pathlib import Path

from google import genai
from google.genai import types

from lib.config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL, GEMINI_IMAGE_SIZE


def _client() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def _is_imagen_model(model: str) -> bool:
    return "imagen" in model.lower()


def _image_size_or_none() -> str | None:
    value = (GEMINI_IMAGE_SIZE or "").strip()
    return value or None


def generate_image(prompt: str, output_path: Path, max_retries: int = 6) -> Path:
    output_path = Path(output_path)
    client = _client()

    last_exc = None
    for attempt in range(max_retries):
        try:
            if _is_imagen_model(GEMINI_IMAGE_MODEL):
                # Imagen 4 API — native 16:9 support
                response = client.models.generate_images(
                    model=GEMINI_IMAGE_MODEL,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio="16:9",
                        image_size=_image_size_or_none(),
                        output_mime_type="image/png",
                    ),
                )
                image_bytes = response.generated_images[0].image.image_bytes
                output_path.write_bytes(image_bytes)
                return output_path
            else:
                # Gemini generate_content API — output_mime_type not supported on direct API (Vertex AI only)
                response = client.models.generate_content(
                    model=GEMINI_IMAGE_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio="16:9",
                            image_size=_image_size_or_none(),
                        ),
                    ),
                )
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        output_path.write_bytes(part.inline_data.data)
                        return output_path
                raise ValueError("Gemini returned no image part in response")

        except Exception as e:
            last_exc = e
            if attempt < max_retries - 1:
                wait = 15 * (attempt + 1)
                print(f"    Retry {attempt + 1}/{max_retries} in {wait}s: {e}")
                time.sleep(wait)

    raise last_exc


def generate_images_batch(prompts: list, output_dir: Path) -> list:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for i, p in enumerate(prompts):
        out = output_dir / p["filename"]
        if out.exists() and out.stat().st_size > 0:
            print(f"  [{i + 1}/{len(prompts)}] Skip (exists): {p['filename']}")
            results.append(out)
            continue

        print(f"  [{i + 1}/{len(prompts)}] Generating: {p['filename']}")
        generate_image(p["prompt"], out)
        results.append(out)

        if i < len(prompts) - 1:
            time.sleep(3)  # rate limit buffer between requests

    return results
