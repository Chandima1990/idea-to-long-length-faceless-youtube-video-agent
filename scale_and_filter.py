import json
import re
from pathlib import Path

run_dir = Path(r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent\outputs\2026-05-07_051644_emergency-fund-savings-vs-invested")

# Get actual audio duration from last word timestamp
words = json.loads((run_dir / "words.json").read_text(encoding="utf-8"))
audio_seconds = words[-1]["endMs"] / 1000
print(f"Audio duration: {audio_seconds:.2f}s")

# Scale scene durations to match actual audio
scenes_data = json.loads((run_dir / "scenes.json").read_text(encoding="utf-8"))
total_scene_dur = sum(s["duration"] for s in scenes_data["scenes"])
scale = audio_seconds / total_scene_dur
print(f"Scene total: {total_scene_dur}s  |  scale: {scale:.4f}")

for s in scenes_data["scenes"]:
    s["duration"] = round(s["duration"] * scale, 3)

scenes_data["total_duration_seconds"] = round(audio_seconds)
(run_dir / "scenes.json").write_text(json.dumps(scenes_data, indent=2, ensure_ascii=False), encoding="utf-8")
new_total = sum(s["duration"] for s in scenes_data["scenes"])
print(f"Scaled scenes saved. New total: {new_total:.2f}s")

# Build script vocabulary for artifact filtering
script = (run_dir / "script.md").read_text(encoding="utf-8").lower()
vocab = set(re.findall(r"[a-z']+", script))

# Filter artifact words
before = len(words)
words_clean = [w for w in words if w["word"].lower().strip(".,!?'") in vocab]
after = len(words_clean)
(run_dir / "words.json").write_text(json.dumps(words_clean, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Words filtered: {before} -> {after} (removed {before - after} artifacts)")
