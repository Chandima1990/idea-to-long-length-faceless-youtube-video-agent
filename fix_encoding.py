import json
import re
from pathlib import Path

scenes_path = Path(r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent\outputs\2026-05-06_164719_paying-off-debt-vs-investing\scenes.json")

# Read raw bytes and decode as utf-8
data = json.loads(scenes_path.read_text(encoding='utf-8'))

# The mojibake: â€" (U+00E2 U+20AC U+201D) is the cp1252 mis-read of UTF-8 em dash bytes
# Replace with a clean em dash or comma
MOJIBAKE = 'â€”'
REPLACEMENT = ' — '

def fix_str(s):
    if isinstance(s, str):
        return s.replace(MOJIBAKE, REPLACEMENT)
    return s

def fix_obj(obj):
    if isinstance(obj, dict):
        return {k: fix_obj(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fix_obj(i) for i in obj]
    elif isinstance(obj, str):
        return fix_str(obj)
    return obj

fixed = fix_obj(data)

scenes_path.write_text(json.dumps(fixed, indent=2, ensure_ascii=False), encoding='utf-8')
print("Done. Fixed scenes.json encoding.")

# Verify
content = scenes_path.read_text(encoding='utf-8')
count = content.count(MOJIBAKE)
em_count = content.count('—')
print(f"Remaining mojibake instances: {count}")
print(f"Em dash instances: {em_count}")
