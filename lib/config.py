import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# Video output
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# Pacing
WORDS_PER_SECOND = 2.5
MIN_SCENE_DURATION = 3
MAX_SCENE_DURATION = 6
DEFAULT_SCENE_DURATION = 4
DEFAULT_DURATION_MINUTES = 1.5

# Gathos API
GATHOS_BASE_URL = "https://gathos.com/api/v1"
GATHOS_IMAGE_API_KEY = os.getenv("GATHOS_API_KEY", os.getenv("GATHOS_IMAGE_API_KEY", ""))
GATHOS_TTS_API_KEY = os.getenv("GATHOS_TTS_API_KEY", "")
GATHOS_IMAGE_WIDTH = 768
GATHOS_IMAGE_HEIGHT = 1344
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

# YouTube upload (optional — leave blank to skip)
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

# TTS voices
PRESET_VOICES = ["josh", "koko", "pixxy", "prof", "rochie", "spraky"]
DEFAULT_VOICE = "pixxy"

# Channel style
CHANNEL_VISUAL_STYLE_SUFFIX = (
    "Cinematic macro photography of a 3D rendered plastic building block minifigure "
    "(LEGO style). The character has painted-on facial features, molded plastic hair, "
    "and wears an olive-green military jacket with a red beret. The figure is standing "
    "in a miniature diorama on cracked, arid desert ground. Ground-level camera, very "
    "shallow depth of field with heavy bokeh, figure in razor-sharp focus and background "
    "heavily blurred. Twilight background with a soft glowing moon. Dramatic cinematic "
    "lighting with a soft bright backlight creating rim light on the character's left "
    "side, high-contrast soft fill light in front. Realistic glossy plastic materials "
    "with subtle subsurface scattering, tangible miniature scale, vertical 9:16 frame."
)

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
