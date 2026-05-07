import sys
sys.path.insert(0, r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent")

import json
from pathlib import Path
from lib.gemini_client import generate_images_batch

RUN_ID = "2026-05-07_051644_emergency-fund-savings-vs-invested"
scenes_path = Path(r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent\outputs") / RUN_ID / "scenes.json"
images_dir = scenes_path.parent / "images"

scenes = json.loads(scenes_path.read_text(encoding="utf-8"))
prompts = [
    {"prompt": s["image_prompt"], "filename": f"scene_{i+1:03d}.png"}
    for i, s in enumerate(scenes["scenes"])
]

print(f"Generating {len(prompts)} images with Gemini...")
generate_images_batch(prompts, images_dir)
print("All images done.")
