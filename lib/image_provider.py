"""Image-provider dispatcher.

Selects the active image-generation backend from IMAGE_PROVIDER (.env):

    gathos  -> lib.gathos_client   (cloud, default)
    gemini  -> lib.gemini_client   (cloud)
    comfyui -> lib.comfyui_client  (local Flux, no cost)
    openai  -> lib.openai_client   (gpt-image-1; best text — 1 scene per image)

All three expose the same generate_image / generate_images_batch interface, so
the rest of the pipeline imports from here and never needs to know which is live.
TTS always stays on Gathos (handled directly in pipeline.py).
"""

from lib.config import IMAGE_PROVIDER

_PROVIDERS = {"gathos", "gemini", "comfyui", "openai"}


def _backend():
    if IMAGE_PROVIDER == "gemini":
        from lib import gemini_client as backend
    elif IMAGE_PROVIDER == "comfyui":
        from lib import comfyui_client as backend
    elif IMAGE_PROVIDER == "openai":
        from lib import openai_client as backend
    elif IMAGE_PROVIDER == "gathos":
        from lib import gathos_client as backend
    else:
        raise ValueError(
            f"Unknown IMAGE_PROVIDER={IMAGE_PROVIDER!r}. "
            f"Choose one of: {', '.join(sorted(_PROVIDERS))}."
        )
    return backend


def active_provider() -> str:
    return IMAGE_PROVIDER


def generate_image(*args, **kwargs):
    return _backend().generate_image(*args, **kwargs)


def generate_images_batch(prompts, output_dir):
    return _backend().generate_images_batch(prompts, output_dir)
