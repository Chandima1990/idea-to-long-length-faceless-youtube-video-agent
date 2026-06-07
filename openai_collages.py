"""Automated 2x2 collage pipeline for text-heavy channels.

    scenes.json  ->  group scenes in 4s  ->  OpenAI gpt-image-1 2x2 collage
                 ->  split into 4 cells   ->  local UltraSharp upscale
                 ->  outputs/<run>/images/scene_NNN.png

Each gpt-image-1 call renders 4 scenes at once (~4x cheaper than 1-per-image), with
perfect text; the local upscale enlarges each cell to 1920x1080 for free. Any leftover
scenes that don't fill a final group of 4 are generated individually (full-res, even
better quality).

Usage:
    python openai_collages.py <run_dir> [quality] [size]
        quality : low | medium | high          (default: medium)
        size    : 1536x1024 | 1024x1024 | 1024x1536  (default: 1536x1024)

Requires OPENAI_API_KEY in .env and a running ComfyUI (for the upscale step).
"""
import json
import sys
import tempfile
from pathlib import Path

from PIL import Image

from lib import openai_client, comfyui_client
from lib.config import OPENAI_IMAGE_QUALITY, OPENAI_IMAGE_SIZE
from collage_to_scenes import split_grid

# Boilerplate chunks to strip from per-scene prompts so the collage prompt stays clean.
_STYLE_MARKER = "Flat 2D vector illustration, infographic style"
_JOSH_END = "no gradients, no shading."
_FILLER = [
    "Use one main idea only, with large readable finance icons and strong red-green contrast.",
    "Keep the layout centered and uncluttered on a white or very light background.",
    "Add bold black outlines around every important object and avoid tiny text.",
    "Use a centered white-background composition with bold black outlines and large readable icons.",
    "Keep Josh large enough to recognize but leave the finance infographic as the visual anchor.",
]


def condense_panel(prompt: str) -> str:
    """Reduce a full scene prompt to its essential scene description for a collage cell."""
    p = prompt.strip()
    if p.lower().startswith("josh:") and _JOSH_END in p:
        p = p.split(_JOSH_END, 1)[1].strip()  # tail already names Josh; style line describes him
    idx = p.find(_STYLE_MARKER)
    if idx != -1:
        p = p[:idx].strip()
    for f in _FILLER:
        p = p.replace(f, "")
    return " ".join(p.split())


def build_2x2_prompt(panels: list[str], style_line: str) -> str:
    rules = (
        "Create ONE single image: a 2x2 grid of 4 separate panels for a video. "
        "I will crop this into 4 images, so the grid must be mechanically precise.\n"
        "- Whole-image aspect ratio: 16:9 widescreen.\n"
        "- A strict 2x2 grid: 2 equal columns and 2 equal rows = 4 identically sized cells. "
        "Each cell is itself 16:9; compose each panel as a complete 16:9 scene.\n"
        "- The grid fills the ENTIRE image edge to edge: no outer margin, no frame or border, "
        "no rounded corners, no overall title, no caption strip, no watermark.\n"
        "- Cell boundaries sit exactly at the horizontal and vertical midlines; all 4 cells equal.\n"
        "- Reading order: cell 1 = top-left, 2 = top-right, 3 = bottom-left, 4 = bottom-right.\n"
        "- Each panel is self-contained; nothing crosses into a neighboring cell. Keep important "
        "content within the central area of each cell so cropping is clean.\n"
        "- Text large, bold, high-contrast, minimal; money as short tokens like $186K, never spelled out.\n"
        f"STYLE (identical across all panels): {style_line}\n"
        "THE 4 PANELS:\n"
    )
    for i, p in enumerate(panels):
        rules += f"{i + 1}. {p}\n"
    rules += "Render exactly one image - the 2x2 grid. No text or graphics outside the 4 panels."
    return rules


def default_style_line(run_dir: Path) -> str:
    style_path = run_dir / "style.json"
    suffix = ""
    if style_path.exists():
        suffix = json.loads(style_path.read_text(encoding="utf-8")).get("style_suffix", "")
    if not suffix:
        suffix = ("flat 2D vector infographic, bold black outlines, solid color fills, white "
                  "background, red and green finance accents, no gradients, no shadows.")

    # Pin the recurring host's exact appearance so it stays consistent across every collage.
    chars_path = run_dir / "characters.json"
    if chars_path.exists():
        data = json.loads(chars_path.read_text(encoding="utf-8"))
        chars = data if isinstance(data, list) else data.get("characters", [])
        if chars:
            host = chars[0]
            suffix += (f" The recurring host '{host.get('name','the host')}' always looks exactly the "
                       f"same: {host.get('description','').strip()}")
    return suffix


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    run_dir = Path(pos[0])
    quality = pos[1] if len(pos) > 1 else OPENAI_IMAGE_QUALITY
    size = pos[2] if len(pos) > 2 else OPENAI_IMAGE_SIZE

    limit = None
    for a in sys.argv:
        if a.startswith("--limit"):
            limit = int(a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1])

    scenes = json.loads((run_dir / "scenes.json").read_text(encoding="utf-8"))["scenes"]
    if limit:
        scenes = scenes[:limit]

    n_check = len(scenes) if not limit else limit
    if n_check % 4 != 0:
        print(f"WARNING: {n_check} scenes is not divisible by 4 — {n_check % 4} scene(s) will be "
              f"generated individually (different style/cost). Fix scene count in scenes.json.")
    collages_dir = run_dir / "collages"
    images_dir = run_dir / "images"
    collages_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="oai_collage_"))
    style_line = default_style_line(run_dir)

    n = len(scenes)
    full_count = (n // 4) * 4
    print(f"{n} scenes -> {full_count // 4} collage(s) of 4 + {n - full_count} individual\n"
          f"quality={quality} size={size}")

    # --- full groups of 4 -> 2x2 collages ---
    for gi in range(full_count // 4):
        group = scenes[gi * 4:gi * 4 + 4]
        start, end = gi * 4 + 1, gi * 4 + 4
        panels = [condense_panel(s["image_prompt"]) for s in group]
        prompt = build_2x2_prompt(panels, style_line)
        collage = collages_dir / f"scene_{start}to{end}.png"
        print(f"\n[COLLAGE] scenes {start}-{end} -> {collage.name}")
        openai_client.generate_image(prompt, collage, size=size, quality=quality)

        img = Image.open(collage).convert("RGB")
        cells = split_grid(img, 2, 2)  # TL, TR, BL, BR
        for i, s in enumerate(group):
            cell_path = tmp / f"{collage.stem}_cell{i + 1}.png"
            cells[i].save(cell_path)
            comfyui_client.upscale_image(cell_path, images_dir / f"scene_{start + i:03d}.png", 1920, 1080)

    # --- leftover scenes -> individual full-res images, then upscale ---
    for j in range(full_count, n):
        s = scenes[j]
        prompt = condense_panel(s["image_prompt"]) + f"  STYLE: {style_line}  16:9 widescreen, full frame."
        raw = tmp / f"scene_{j + 1:03d}_raw.png"
        print(f"\n[SINGLE] scene {j + 1} -> {raw.name}")
        openai_client.generate_image(prompt, raw, size=size, quality=quality)
        comfyui_client.upscale_image(raw, images_dir / f"scene_{j + 1:03d}.png", 1920, 1080)

    print(f"\nDONE: {n} scene images in {images_dir}")


if __name__ == "__main__":
    main()
