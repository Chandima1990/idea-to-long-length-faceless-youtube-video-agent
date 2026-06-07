"""ChatGPT N×N collage  ->  split into cells  ->  UltraSharp upscale  ->  scene_NNN.png

You make grid collages in ChatGPT (gpt-image-1) — several scenes per image, perfect text —
and name each file with the scene range it covers, e.g. "scene_1to4.png" (2x2),
"scene_1to9.png" (3x3), "scene_25to27.png" (partial last grid). This tool splits each
collage in reading order (left-to-right, top-to-bottom), upscales every cell to 1920x1080
locally with 4x-UltraSharp (no quality loss, text preserved), and writes scene_001.png ...
into the run's images/ folder.

The grid is inferred from the scene count (4 -> 2x2, 9 -> 3x3, 6 -> 3x2 ...), or set it
explicitly in the filename as RxC, e.g. "scene_1to9_3x3.png" or just pass --grid 3x3.

Usage:
    python collage_to_scenes.py "<collages_dir>" "<output_images_dir>" [W] [H] [--grid RxC]

Example:
    python collage_to_scenes.py ^
      "outputs/2026-06-06_060936_..._COMFYUI/collages" ^
      "outputs/2026-06-06_060936_..._COMFYUI/images"
"""
import math
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image

from lib import comfyui_client as c


def parse_scene_range(name: str):
    """'scene_13to16.png' -> (13, 16). Ignores any trailing RxC grid hint. None if no match."""
    cleaned = re.sub(r"\d+\s*[xX]\s*\d+", "", name)  # drop a grid hint like 3x3 first
    nums = re.findall(r"\d+", cleaned)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    return None


def parse_grid_hint(name: str):
    """'scene_1to9_3x3.png' -> (3, 3) as (rows, cols). None if absent."""
    m = re.search(r"(\d+)\s*[xX]\s*(\d+)", name)
    return (int(m.group(1)), int(m.group(2))) if m else None


def infer_grid(count: int):
    """4 -> (2,2), 9 -> (3,3), 6 -> (2,3) ... rows x cols, cols-heavy for non-squares."""
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)
    return rows, cols


def split_grid(img: Image.Image, rows: int, cols: int):
    """Return cells in reading order (row-major: left->right, top->bottom)."""
    cw, ch = img.width // cols, img.height // rows
    cells = []
    for r in range(rows):
        for cc in range(cols):
            cells.append(img.crop((cc * cw, r * ch, (cc + 1) * cw, (r + 1) * ch)))
    return cells


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    collages_dir = Path(args[0])
    images_dir = Path(args[1])
    W = int(args[2]) if len(args) > 2 else 1920
    H = int(args[3]) if len(args) > 3 else 1080

    cli_grid = None
    for a in sys.argv:
        if a.startswith("--grid"):
            g = a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1]
            cli_grid = parse_grid_hint(g)
    images_dir.mkdir(parents=True, exist_ok=True)

    collages = sorted(collages_dir.glob("*.png")) + sorted(collages_dir.glob("*.jpg"))
    if not collages:
        print(f"No collages found in {collages_dir}")
        sys.exit(1)

    # Order collages by their starting scene number when the name encodes it.
    def sort_key(p):
        rng = parse_scene_range(p.name)
        return rng[0] if rng else 10**6
    collages.sort(key=sort_key)

    tmp = Path(tempfile.mkdtemp(prefix="collage_split_"))
    next_seq = 1
    total = 0
    for col in collages:
        rng = parse_scene_range(col.name)
        img = Image.open(col).convert("RGB")

        if rng:
            start, end = rng
            count = end - start + 1
            scene_nums = list(range(start, end + 1))
        else:
            count = 4
            scene_nums = list(range(next_seq, next_seq + 4))

        rows, cols = cli_grid or parse_grid_hint(col.name) or infer_grid(count)
        cells = split_grid(img, rows, cols)  # row-major reading order

        print(f"\n{col.name}  ->  scenes {scene_nums}  (grid {rows}x{cols}, {len(cells)} cells)")
        for i, n in enumerate(scene_nums):
            cell_img = cells[i]
            cell_path = tmp / f"{col.stem}_cell{i+1:02d}.png"
            cell_img.save(cell_path)
            out = images_dir / f"scene_{n:03d}.png"
            c.upscale_image(cell_path, out, W, H)
            total += 1
        next_seq = scene_nums[-1] + 1

    print(f"\nDONE: {total} scene images upscaled to {W}x{H} in {images_dir}")


if __name__ == "__main__":
    main()
