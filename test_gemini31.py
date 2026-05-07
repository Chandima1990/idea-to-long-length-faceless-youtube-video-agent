import sys
sys.path.insert(0, r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent")

from pathlib import Path
from lib.gemini_client import generate_image
from PIL import Image

out = Path(r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent\test_gemini31_out.png")
try:
    generate_image("A flat 2D vector illustration of a blue savings jar and a green investment jar side by side on a white background, infographic style, bold outlines", out)
    img = Image.open(out)
    print(f"SUCCESS: {img.size[0]}x{img.size[1]}  ratio: {img.size[0]/img.size[1]:.3f}  (16:9 = 1.778)")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
