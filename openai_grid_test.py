"""Quick experiment: ask gpt-image-2 for a single 3x3 collage and see if the grid
is even enough to split into 9 clean cells. Usage: python openai_grid_test.py [rows] [cols]"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from lib import openai_client
from openai_collages import condense_panel, default_style_line
from collage_to_scenes import split_grid

ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 3
N = ROWS * COLS

RUN = Path(r"outputs/2026-06-06_060936_timing_OPENAI_test")
OUT = RUN / "grid_test"
OUT.mkdir(parents=True, exist_ok=True)

scenes = json.loads((RUN / "scenes.json").read_text(encoding="utf-8"))["scenes"][:N]
panels = [condense_panel(s["image_prompt"]) for s in scenes]
style = default_style_line(RUN)

rules = (
    f"Create ONE single image: a {ROWS}x{COLS} grid of {N} separate panels for a video. "
    "I will crop this into separate images, so the grid must be mechanically perfect.\n"
    "- Whole-image aspect ratio: 16:9 widescreen.\n"
    f"- A strict {ROWS}x{COLS} grid: {COLS} EQUAL columns and {ROWS} EQUAL rows = {N} identical cells.\n"
    f"- CRITICAL: every column must be exactly the same width and every row exactly the same height. "
    "Do NOT make the middle column or middle row narrower or wider than the others.\n"
    f"- Cell boundaries fall exactly at each 1/{COLS} of the width and each 1/{ROWS} of the height.\n"
    "- The grid fills the ENTIRE image edge to edge: no outer margin, no frame, no rounded corners, "
    "no overall title, no caption strip, no watermark.\n"
    "- Separate cells with thin, straight, uniform lines of equal thickness, or no lines.\n"
    "- Reading order left-to-right then top-to-bottom (cell 1 = top-left ... last = bottom-right).\n"
    "- Each panel self-contained; nothing crosses into a neighbor. Keep content centered in each cell.\n"
    "- Text large, bold, high-contrast, minimal; money as short tokens like $186K.\n"
    f"STYLE (identical across all panels): {style}\nTHE {N} PANELS:\n"
)
for i, p in enumerate(panels):
    rules += f"{i + 1}. {p}\n"
rules += f"Render exactly one image - the {ROWS}x{COLS} grid. No text or graphics outside the {N} panels."

collage = OUT / f"grid_{ROWS}x{COLS}.png"
print(f"Generating {ROWS}x{COLS} collage ({N} panels)...")
openai_client.generate_image(rules, collage)

img = Image.open(collage).convert("RGB")
print(f"Collage size: {img.size}  aspect {img.width / img.height:.3f}")
print(f"Even split -> each cell {img.width // COLS} x {img.height // ROWS}")

cells = split_grid(img, ROWS, COLS)
for i, cell in enumerate(cells):
    cell.save(OUT / f"cell_{i + 1:02d}.png")

# contact sheet with grid lines drawn at the exact thirds so misalignment is visible
tw, th = 360, 202
sheet = Image.new("RGB", (COLS * tw + (COLS + 1) * 8, ROWS * th + (ROWS + 1) * 8), (25, 25, 28))
d = ImageDraw.Draw(sheet)
for i, cell in enumerate(cells):
    r, cc = divmod(i, COLS)
    x, y = 8 + cc * (tw + 8), 8 + r * (th + 8)
    sheet.paste(cell.resize((tw, th)), (x, y))
    d.text((x + 6, y + 4), f"#{i + 1}", fill=(255, 255, 0))
sheet.save(OUT / "_contact_sheet.png")
print(f"Saved {len(cells)} cells + contact sheet in {OUT}")
