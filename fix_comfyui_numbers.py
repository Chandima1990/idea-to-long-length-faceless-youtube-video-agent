"""Round 2: the spelled-out number-words garbled on Flux.2 Klein, but short
'$186K' tokens rendered fine. Re-do scenes 1,8,9,17 with short tokens only."""
import os
os.environ["IMAGE_PROVIDER"] = "comfyui"

import json
from pathlib import Path
from lib import comfyui_client as c

DST = Path(r"outputs/2026-06-06_060936_timing-the-market_COMFYUI")

JOSH = ("Josh: 32-year-old man, short dark brown hair, short dark beard, average build, "
        "light skin, light sky-blue casual short-sleeve shirt, dark navy pants, no glasses. "
        "Flat vector cartoon illustration style, clean bold black outlines, simple flat color "
        "fills, no gradients, no shading. ")

STYLE = (" Flat 2D vector illustration, infographic style, bold clean outlines, solid color "
         "fills, no gradients, no shadows, no photorealism, white background, modern minimal "
         "design, geometric shapes, clean finance icons, red and green accents, 16:9 aspect ratio.")

# Only short $ tokens as labels; explicitly forbid any other words.
REWRITES = {
    1: JOSH + (
        "Josh stands on the LEFT in a presenter pose, one hand raised toward a chart on the "
        "RIGHT. The chart is a vertical stack of horizontal bars: four long green bars of similar "
        "length grouped at the top, and one short red bar at the bottom about one quarter as long, "
        "clearly separated below the rest. Put the short label '$186K' beside the top green bar and "
        "'$47K' beside the short red bar. Show ONLY those two short dollar labels — no spelled-out "
        "words, no sentences, no other text or numbers anywhere. Keep Josh large on the left, the "
        "bar chart as the visual anchor on the right." ) + STYLE,

    8: (
        "A finance comparison as a vertical stack of horizontal bars: four long green bars of "
        "similar length grouped together, and one short red bar about one quarter as long isolated "
        "at the bottom. Put the short label '$186K' beside the top green bar and '$47K' beside the "
        "short red bar. Show ONLY those two short dollar labels — no spelled-out words, no "
        "sentences, no other text or numbers anywhere. Strong red-green contrast, centered on a "
        "white background, bold black outlines." ) + STYLE,

    9: (
        "A finance comparison as a vertical stack of horizontal bars: four long green bars of "
        "similar length at the top, and one short red bar about one quarter as long isolated at the "
        "bottom with a clear gap above it. Put the short label '$186K' beside the top green bar and "
        "'$47K' beside the short red bar. Show ONLY those two short dollar labels — no spelled-out "
        "words, no sentences, no other text or numbers anywhere. Strong red-green contrast, "
        "centered on a white background, bold black outlines." ) + STYLE,

    17: JOSH + (
        "Josh stands on the LEFT in a presenter pose, one hand raised toward a comparison on the "
        "RIGHT. The right side shows two green staircase climbs side by side: a tall full staircase "
        "rising the entire height, and beside it a clearly shorter staircase that starts late and "
        "ends well below, with a small red block on top of the short one marking the missing early "
        "years. Put the short label '$745K' under the tall staircase and '$295K' under the short "
        "one. Show ONLY those two short dollar labels — no names, no spelled-out words, no other "
        "text or numbers anywhere. Keep Josh large on the left, the two-staircase comparison as the "
        "anchor on the right." ) + STYLE,
}

scenes_path = DST / "scenes.json"
data = json.loads(scenes_path.read_text(encoding="utf-8"))
for n, prompt in REWRITES.items():
    data["scenes"][n - 1]["image_prompt"] = prompt
scenes_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated {len(REWRITES)} prompts")

for n in REWRITES:
    f = DST / "images" / f"scene_{n:03d}.png"
    if f.exists():
        f.unlink()
        print(f"  deleted {f.name}")

prompts = [
    {"prompt": s["image_prompt"], "filename": f"scene_{i+1:03d}.png"}
    for i, s in enumerate(data["scenes"])
]
c.generate_images_batch(prompts, DST / "images")
print("DONE round 2:", sorted(REWRITES))
