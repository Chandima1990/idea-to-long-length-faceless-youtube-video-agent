"""One-off: regenerate the timing-the-market scenes via local ComfyUI/Flux
into a separate test folder, leaving the original run untouched."""
import os
os.environ["IMAGE_PROVIDER"] = "comfyui"

import json
import time
from pathlib import Path
from lib import comfyui_client as c

DST = Path(r"outputs/2026-06-06_060936_timing-the-market_COMFYUI")
scenes = json.loads((DST / "scenes.json").read_text(encoding="utf-8"))["scenes"]

prompts = [
    {"prompt": s["image_prompt"], "filename": f"scene_{i+1:03d}.png"}
    for i, s in enumerate(scenes)
]

print(f"Generating {len(prompts)} images via ComfyUI/Flux into {DST/'images'}")
t0 = time.time()
c.generate_images_batch(prompts, DST / "images")
print(f"ALL DONE: {len(prompts)} images in {(time.time()-t0)/60:.1f} min")
