"""Rewrite the text-heavy scene prompts per skills/flux-image-prompting.md and
regenerate ONLY those scenes via ComfyUI/Flux, in the _COMFYUI test folder."""
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

# scene number (1-based) -> rewritten prompt body (Flux-safe)
REWRITES = {
    1: JOSH + (
        "Josh stands on the LEFT in a presenter pose, one hand raised toward a chart on the "
        "RIGHT. The chart is a vertical ranked list of horizontal bars, one bar per row only: "
        "four tall green bars of roughly equal length grouped at the top, and a single short red "
        "bar at the bottom about one quarter as long, clearly separated below the rest. Label "
        "ONLY the top green bar 'one hundred eighty-six thousand dollars ($186K)' and the bottom "
        "red bar 'forty-seven thousand dollars ($47K)'. No other numbers or words anywhere. The "
        "short red bar is money left sitting in cash. Keep Josh large and recognizable on the "
        "left, the bar chart as the visual anchor on the right." ) + STYLE,

    7: (
        "A clean race-track infographic: five simple investor avatars on separate lanes running "
        "left to right. Four avatars in green lanes are far ahead near the finish on the right; "
        "one avatar in the red lane is stalled at the start on the left behind a single large red "
        "octagonal stop sign. Big green forward arrows fill the leading lanes. NO text, no words, "
        "no letters anywhere — tell the story only with position, arrows and the stop sign. One "
        "main idea only, large readable icons, strong red-green contrast, centered on a white "
        "background, bold black outlines." ) + STYLE,

    8: (
        "A finance comparison shown as a vertical ranked list of horizontal bars, one bar per row "
        "only: four tall green bars of roughly equal length grouped together, and a single short "
        "red bar about one quarter as long isolated at the bottom. Label ONLY the longest green "
        "bar 'one hundred eighty-six thousand dollars ($186K)' and the short red bar 'forty-seven "
        "thousand dollars ($47K)'. No other numbers or words. The short red bar is money kept in "
        "cash on the sidelines. One main idea only, large readable icons, strong red-green "
        "contrast, centered on a white background, bold black outlines, no tiny text." ) + STYLE,

    9: (
        "A finance comparison shown as a vertical ranked list of horizontal bars, one bar per row "
        "only: four tall green bars of roughly equal length at the top, and one short red bar "
        "about one quarter as long isolated at the bottom with a clear gap above it. Label ONLY "
        "the top green bar 'one hundred eighty-six thousand dollars ($186K)' and the short red bar "
        "'forty-seven thousand dollars ($47K)'. No other numbers or words. The red bar is the "
        "cash investor falling far behind. One main idea only, strong red-green contrast, centered "
        "on a white background, bold black outlines, no tiny text." ) + STYLE,

    13: (
        "A large pie chart with most slices in green emerging out of a dark red bear-market zone, "
        "and one small blue slice set just beside the green. The idea: the best green days are "
        "hidden inside the scary red market period. NO text, no words, no letters or labels "
        "anywhere — communicate only through the red zone, the green slices and the small blue "
        "slice. One main idea only, strong red-green contrast, centered on a white background, "
        "bold black outlines, no tiny text." ) + STYLE,

    17: JOSH + (
        "Josh stands on the LEFT in a presenter pose, one hand raised toward a comparison on the "
        "RIGHT. The right side shows two green staircase climbs side by side: a tall full "
        "staircase rising the entire height, and beside it a clearly shorter staircase that starts "
        "late and ends well below, with a small red block marking the missing early years. Label "
        "ONLY the tall staircase 'seven hundred forty-five thousand dollars ($745K)' and the short "
        "one 'two hundred ninety-five thousand dollars ($295K)'. No names, no other numbers or "
        "words. Keep Josh large on the left, the two-staircase comparison as the anchor on the "
        "right." ) + STYLE,

    24: (
        "A large magnifying glass hovers over a clean investment line chart, magnifying a smooth "
        "green compounding curve that rises to the right. Inside the magnified circle a red "
        "downward arrow and a small red dripping-coin icon highlight money lost by waiting. NO "
        "text, no words, no letters anywhere — show the cost of waiting only through the red "
        "downward arrow and dripping coins against the rising green curve. One main idea only, "
        "strong red-green contrast, centered on a white background, bold black outlines." ) + STYLE,
}

# 1) update the test scenes.json (original run untouched)
scenes_path = DST / "scenes.json"
data = json.loads(scenes_path.read_text(encoding="utf-8"))
for n, prompt in REWRITES.items():
    data["scenes"][n - 1]["image_prompt"] = prompt
scenes_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated {len(REWRITES)} prompts in {scenes_path}")

# 2) delete the old images so the batch regenerates exactly these
for n in REWRITES:
    f = DST / "images" / f"scene_{n:03d}.png"
    if f.exists():
        f.unlink()
        print(f"  deleted {f.name}")

# 3) regenerate (batch skips the 20 that still exist, makes only the deleted 7)
prompts = [
    {"prompt": s["image_prompt"], "filename": f"scene_{i+1:03d}.png"}
    for i, s in enumerate(data["scenes"])
]
c.generate_images_batch(prompts, DST / "images")
print("DONE regenerating text-heavy scenes:", sorted(REWRITES))
