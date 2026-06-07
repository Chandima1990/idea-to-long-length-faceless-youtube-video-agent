import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# Video output
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30

# Pacing
WORDS_PER_SECOND = 2.5
MIN_SCENE_DURATION = 7
MAX_SCENE_DURATION = 15
DEFAULT_SCENE_DURATION = 10

# Active channel
CHANNEL = os.getenv("CHANNEL", "rich_mantra")
CHANNEL_STYLE_PATH = BASE_DIR / "channels" / f"{CHANNEL}.json"

# Gathos API
GATHOS_BASE_URL = "https://gathos.com/api/v1"
GATHOS_IMAGE_API_KEY = os.getenv("GATHOS_API_KEY", os.getenv("GATHOS_IMAGE_API_KEY", ""))
GATHOS_TTS_API_KEY = os.getenv("GATHOS_TTS_API_KEY", "")
GATHOS_IMAGE_WIDTH = 1344
GATHOS_IMAGE_HEIGHT = 768
GATHOS_SHORTS_IMAGE_WIDTH = 768
GATHOS_SHORTS_IMAGE_HEIGHT = 1344
GATHOS_POLL_INTERVAL = 5
GATHOS_TTS_POLL_INTERVAL = 3
GATHOS_TIMEOUT = 3600
GATHOS_MAX_RETRIES = 5
GATHOS_IMAGE_MAX_RETRIES = int(os.getenv("GATHOS_IMAGE_MAX_RETRIES", "10"))

# Gemini API (image generation)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")
GEMINI_IMAGE_SIZE = os.getenv("GEMINI_IMAGE_SIZE", "")  # Gemini 3 image models: 1K | 2K | 4K

# OpenAI gpt-image-1 (image generation — used for 2x2 collages, best text quality)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2-2026-04-21")
OPENAI_IMAGE_SIZE = os.getenv("OPENAI_IMAGE_SIZE", "auto")        # auto -> true 16:9 for collages | 1536x1024 | 1024x1024 | 1024x1536
OPENAI_IMAGE_QUALITY = os.getenv("OPENAI_IMAGE_QUALITY", "auto")  # auto | low | medium | high

# Image provider selection: gathos | gemini | comfyui | openai
# Flip this in .env to switch where B-roll / thumbnail images come from.
# gathos and gemini are cloud; comfyui is your local Flux setup (no cost).
IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "gathos").strip().lower()

# ComfyUI (local image generation via Flux.2 Klein or any workflow)
COMFYUI_BASE_URL = os.getenv("COMFYUI_BASE_URL", "http://127.0.0.1:8188").rstrip("/")
# Path to a workflow exported in *API format* (ComfyUI: Settings > Enable Dev mode,
# then "Save (API Format)"). Edit it once to insert the placeholder tokens below.
COMFYUI_WORKFLOW_PATH = os.getenv(
    "COMFYUI_WORKFLOW_PATH", str(BASE_DIR / "comfyui" / "workflow_api.json")
)
# Tokens replaced inside the workflow JSON at submit time. Put COMFYUI_PROMPT_TOKEN
# in your positive CLIP-text node; the others are optional.
COMFYUI_PROMPT_TOKEN = os.getenv("COMFYUI_PROMPT_TOKEN", "__PROMPT__")
COMFYUI_NEG_TOKEN = os.getenv("COMFYUI_NEG_TOKEN", "__NEGATIVE__")
COMFYUI_SEED_TOKEN = os.getenv("COMFYUI_SEED_TOKEN", "__SEED__")
COMFYUI_WIDTH_TOKEN = os.getenv("COMFYUI_WIDTH_TOKEN", "__WIDTH__")
COMFYUI_HEIGHT_TOKEN = os.getenv("COMFYUI_HEIGHT_TOKEN", "__HEIGHT__")
COMFYUI_NEGATIVE_PROMPT = os.getenv("COMFYUI_NEGATIVE_PROMPT", "")
COMFYUI_POLL_INTERVAL = int(os.getenv("COMFYUI_POLL_INTERVAL", "2"))
COMFYUI_TIMEOUT = int(os.getenv("COMFYUI_TIMEOUT", "600"))
# Upscale-only workflow (enlarges an existing image with 4x-UltraSharp, no diffusion).
# Used for the "ChatGPT 2x2 collage -> split -> upscale" path. Tokens: __IMAGE__, __WIDTH__, __HEIGHT__.
COMFYUI_UPSCALE_WORKFLOW_PATH = os.getenv(
    "COMFYUI_UPSCALE_WORKFLOW_PATH", str(BASE_DIR / "comfyui" / "upscale_api.json")
)

# Deepgram API
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEEPGRAM_BASE_URL = os.getenv("DEEPGRAM_BASE_URL", "https://api.deepgram.com/v1")
DEEPGRAM_MODEL = os.getenv("DEEPGRAM_MODEL", "nova-3")

# YouTube upload (optional — leave blank to skip)
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

# TTS voices
PRESET_VOICES = ["josh", "koko", "pixxy", "prof", "rochie", "spraky"]
DEFAULT_VOICE = "josh"

# Ken Burns presets
KEN_BURNS_PRESETS = {
    "pan_right": {"startX": 0, "endX": -3, "startY": 0, "endY": 0, "startScale": 1.05, "endScale": 1.05},
    "pan_left": {"startX": 0, "endX": 3, "startY": 0, "endY": 0, "startScale": 1.05, "endScale": 1.05},
    "zoom_in": {"startX": 0, "endX": 0, "startY": 0, "endY": 0, "startScale": 1.0, "endScale": 1.08},
    "zoom_out": {"startX": 0, "endX": 0, "startY": 0, "endY": 0, "startScale": 1.08, "endScale": 1.0},
    "pan_up": {"startX": 0, "endX": 0, "startY": 0, "endY": 3, "startScale": 1.05, "endScale": 1.05},
    "zoom_in_pan_right": {"startX": 0, "endX": -2, "startY": 0, "endY": 0, "startScale": 1.0, "endScale": 1.06},
}

# Film effect presets
FILM_PRESETS = {
    "clean_modern": {"filter": "contrast(1.04) saturate(1.05)", "grain": 0, "vignette": 0},
    "vintage_film": {"filter": "contrast(1.08) saturate(0.85) brightness(0.95) sepia(0.15)", "grain": 0.12, "vignette": 0.5},
    "bw_documentary": {"filter": "grayscale(1) contrast(1.15) brightness(0.92)", "grain": 0.18, "vignette": 0.6},
    "dark_cinematic": {"filter": "contrast(1.12) saturate(0.7) brightness(0.88)", "grain": 0.08, "vignette": 0.4},
    "sepia_archival": {"filter": "sepia(0.6) contrast(1.05) brightness(0.9)", "grain": 0.22, "vignette": 0.7},
    "none": {"filter": "none", "grain": 0, "vignette": 0},
    "vector_infographic": {"filter": "contrast(1.06) saturate(1.1) brightness(1.02)", "grain": 0, "vignette": 0},
}

# ffmpeg location (optional — set FFMPEG_PATH in .env to the directory containing ffmpeg/ffprobe)
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "")

# Paths
OUTPUTS_DIR = BASE_DIR / "outputs"
STATE_DIR = BASE_DIR / "state"
SKILLS_DIR = BASE_DIR / "skills"
