import json
import sys
from pathlib import Path

from lib.config import OUTPUTS_DIR
from lib.state import create_run, load_run, update_stage
from lib.gathos_client import generate_tts
from lib.gemini_client import generate_images_batch
from lib.deepgram_client import save_word_timestamps
from lib.transcript import download_youtube, transcribe_video


def stage_tts(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    script_path = output_dir / "script.md"

    if not script_path.exists():
        print("ERROR: script.md not found. Run script stage first.")
        sys.exit(1)

    narration = script_path.read_text(encoding='utf-8').strip()
    voice = run["voice"]
    audio_path = output_dir / "narration.mp3"

    print(f"[TTS] Generating narration with voice '{voice}'...")
    update_stage(run_id, "tts", "in_progress")
    generate_tts(narration, voice, audio_path)
    update_stage(run_id, "tts", "complete", str(audio_path))
    print(f"[TTS] Done: {audio_path}")


def stage_timestamps(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    audio_path = output_dir / "narration.mp3"
    words_path = output_dir / "words.json"

    if not audio_path.exists():
        print("ERROR: narration.mp3 not found. Run TTS stage first.")
        sys.exit(1)

    print("[TIMESTAMPS] Extracting word-level timing...")
    update_stage(run_id, "timestamps", "in_progress")
    save_word_timestamps(audio_path, words_path)
    update_stage(run_id, "timestamps", "complete", str(words_path))
    print(f"[TIMESTAMPS] Done: {words_path}")


def stage_images(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    scenes_path = output_dir / "scenes.json"
    images_dir = output_dir / "images"

    if not scenes_path.exists():
        print("ERROR: scenes.json not found. Run scenes stage first.")
        sys.exit(1)

    scenes = json.loads(scenes_path.read_text(encoding='utf-8'))
    prompts = []
    for i, scene in enumerate(scenes["scenes"]):
        prompts.append({
            "prompt": scene["image_prompt"],
            "filename": f"scene_{i+1:03d}.png",
        })

    print(f"[IMAGES] Generating {len(prompts)} B-roll images...")
    update_stage(run_id, "images", "in_progress")
    generate_images_batch(prompts, images_dir)
    update_stage(run_id, "images", "complete", str(images_dir))
    print(f"[IMAGES] Done: {images_dir}")


def stage_render(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    import subprocess

    props = {
        "outputDir": str(output_dir),
        "filmPreset": run["film_preset"],
    }
    props_json = json.dumps(props)

    remotion_dir = Path(__file__).parent.parent / "remotion"
    final_path = output_dir / "final.mp4"

    print("[RENDER] Rendering video with Remotion...")
    update_stage(run_id, "render", "in_progress")
    subprocess.run(
        [
            "npx", "remotion", "render",
            "ViralBrollVideo",
            str(final_path),
            "--props", props_json,
        ],
        cwd=str(remotion_dir),
        check=True,
        timeout=1800,
    )
    update_stage(run_id, "render", "complete", str(final_path))
    print(f"[RENDER] Done: {final_path}")


def stage_viral_dna(run_id: str, youtube_url: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])

    print(f"[VIRAL DNA] Downloading: {youtube_url}")
    video_path = download_youtube(youtube_url, output_dir)

    print("[VIRAL DNA] Transcribing...")
    result = transcribe_video(video_path, output_dir)
    print(f"[VIRAL DNA] Transcript saved. Agent will now run 3-level dissection.")
    return result


STAGE_MAP = {
    "tts": stage_tts,
    "timestamps": stage_timestamps,
    "images": stage_images,
    "render": stage_render,
}


def run_stage(run_id: str, stage: str, **kwargs):
    if stage in STAGE_MAP:
        STAGE_MAP[stage](run_id, **kwargs)
    else:
        print(f"Stage '{stage}' is agent-driven (script/style_card/characters/scenes).")
        print("The AI agent handles these stages using skills/.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Viral B-Roll Pipeline")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    parser.add_argument("--stage", type=str, help="Run a specific stage")
    parser.add_argument("--run-id", type=str, help="Run ID to operate on")
    parser.add_argument("--youtube-url", type=str, help="YouTube URL for viral DNA")
    args = parser.parse_args()

    if args.check:
        print("Checking dependencies...")
        import shutil
        from lib.config import GATHOS_TTS_API_KEY, DEEPGRAM_API_KEY, GEMINI_API_KEY, GEMINI_IMAGE_MODEL
        for tool in ["ffmpeg", "ffprobe"]:
            path = shutil.which(tool) or shutil.which(tool, path="/opt/homebrew/bin")
            print(f"  {tool}: {'OK' if path else 'MISSING'} ({path})")
        print(f"  Gemini API key: {'SET' if GEMINI_API_KEY else 'MISSING'}")
        print(f"  Gemini image model: {GEMINI_IMAGE_MODEL}")
        print(f"  Gathos TTS key: {'SET' if GATHOS_TTS_API_KEY else 'MISSING'}")
        print(f"  Deepgram API key: {'SET' if DEEPGRAM_API_KEY else 'MISSING'}")
        print("Done.")
    elif args.stage and args.run_id:
        if args.stage == "viral_dna" and args.youtube_url:
            stage_viral_dna(args.run_id, args.youtube_url)
        else:
            run_stage(args.run_id, args.stage)
    else:
        parser.print_help()
