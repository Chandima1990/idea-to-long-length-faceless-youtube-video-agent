import shutil
import subprocess
import sys
from pathlib import Path

from lib.deepgram_client import extract_audio, get_word_timestamps


def _find_ffmpeg() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    candidates = [
        r"C:\Users\emcc1\Downloads\Repos\remotion videos\YashAiGuy\idea-to-long-length-faceless-youtube-video-agent\remotion\node_modules\@remotion\compositor-win32-x64-msvc\ffmpeg.exe",
        r"C:\Users\emcc1\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe",
        "/opt/homebrew/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/usr/bin/ffmpeg",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return "ffmpeg"


def download_youtube(url: str, output_dir: Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "reference_video.mp4"

    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skipping download (exists): {output_path.name}")
        return output_path

    subprocess.run(
        [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", _find_ffmpeg(),
            "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "--merge-output-format", "mp4",
            "-o", str(output_path),
            url,
        ],
        check=True,
        timeout=300,
    )
    return output_path


def transcribe_video(video_path: Path, output_dir: Path) -> dict:
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    audio_path = output_dir / "reference_audio.wav"

    extract_audio(video_path, audio_path)
    words = get_word_timestamps(audio_path)

    transcript = " ".join(w["word"] for w in words)
    transcript_path = output_dir / "transcript.txt"
    transcript_path.write_text(transcript, encoding='utf-8')

    print(f"  Transcribed: {len(words)} words, {len(transcript)} chars")
    return {"transcript": transcript, "words": words, "path": str(transcript_path)}
