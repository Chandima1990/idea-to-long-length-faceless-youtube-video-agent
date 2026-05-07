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

# Gathos API
GATHOS_BASE_URL = "https://gathos.com/api/v1"
GATHOS_IMAGE_API_KEY = os.getenv("GATHOS_API_KEY", os.getenv("GATHOS_IMAGE_API_KEY", ""))
GATHOS_TTS_API_KEY = os.getenv("GATHOS_TTS_API_KEY", "")
GATHOS_IMAGE_WIDTH = 1344
GATHOS_IMAGE_HEIGHT = 768
GATHOS_POLL_INTERVAL = 5
GATHOS_TTS_POLL_INTERVAL = 3
GATHOS_TIMEOUT = 600
GATHOS_MAX_RETRIES = 5

# Gemini API (image generation)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

# Deepgram API
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
DEEPGRAM_MODEL = "nova-3"

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

# Paths
OUTPUTS_DIR = BASE_DIR / "outputs"
STATE_DIR = BASE_DIR / "state"
SKILLS_DIR = BASE_DIR / "skills"
