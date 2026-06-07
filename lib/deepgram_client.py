import json
import os
import shutil
import subprocess
from pathlib import Path

import requests

from lib.config import DEEPGRAM_API_KEY, DEEPGRAM_BASE_URL, DEEPGRAM_MODEL, BASE_DIR, FFMPEG_PATH

_FFMPEG_CANDIDATE_DIRS = [d for d in [
    str(BASE_DIR / "remotion" / "node_modules" / "@remotion" / "compositor-win32-x64-msvc"),
    FFMPEG_PATH,
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/usr/bin",
] if d]


def _find_exe(name: str) -> str:
    # Try system PATH first
    found = shutil.which(name)
    if found:
        return found
    # Try candidate dirs with and without .exe extension
    for d in _FFMPEG_CANDIDATE_DIRS:
        for suffix in ("", ".exe"):
            p = Path(d) / (name + suffix)
            if p.exists():
                return str(p)
    return name  # fall back to bare name and let OS raise the error


_FFMPEG = _find_exe("ffmpeg")
_FFPROBE = _find_exe("ffprobe")


def extract_audio(input_path: Path, output_path: Path, sample_rate: int = 16000) -> Path:
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        return output_path
    subprocess.run(
        [
            _FFPROBE, "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(input_path),
        ],
        capture_output=True, check=True,
    )
    subprocess.run(
        [
            _FFMPEG, "-y", "-i", str(input_path),
            "-ar", str(sample_rate), "-ac", "1", "-f", "wav",
            str(output_path),
        ],
        capture_output=True, check=True,
    )
    return output_path


def get_word_timestamps(audio_path: Path) -> list[dict]:
    audio_path = Path(audio_path)
    wav_path = audio_path.with_suffix(".16k.wav")
    extract_audio(audio_path, wav_path)

    with open(wav_path, "rb") as f:
        audio_data = f.read()

    resp = requests.post(
        f"{DEEPGRAM_BASE_URL}/listen",
        headers={
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav",
        },
        params={
            "model": DEEPGRAM_MODEL,
            "punctuate": "true",
            "words": "true",
        },
        data=audio_data,
        timeout=120,
    )
    resp.raise_for_status()
    result = resp.json()

    channels = result.get("results", {}).get("channels", [])
    if not channels:
        raise ValueError("No channels in Deepgram response")

    alternatives = channels[0].get("alternatives", [])
    if not alternatives:
        raise ValueError("No alternatives in Deepgram response")

    dg_words = alternatives[0].get("words", [])

    words = []
    for w in dg_words:
        words.append({
            "word": w["word"],
            "startMs": int(w["start"] * 1000),
            "endMs": int(w["end"] * 1000),
        })

    wav_path.unlink(missing_ok=True)
    return words


def save_word_timestamps(audio_path: Path, output_path: Path) -> Path:
    output_path = Path(output_path)
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping (exists): {output_path.name}")
        return output_path
    words = get_word_timestamps(audio_path)
    output_path.write_text(json.dumps(words, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"  Saved {len(words)} words to {output_path.name}")
    return output_path
