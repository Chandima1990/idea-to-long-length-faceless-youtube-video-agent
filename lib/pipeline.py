import json
import subprocess
import sys
from pathlib import Path

from lib.config import (
    OUTPUTS_DIR, YOUTUBE_CLIENT_ID, CHANNEL_STYLE_PATH,
    GATHOS_IMAGE_WIDTH, GATHOS_IMAGE_HEIGHT,
    GATHOS_SHORTS_IMAGE_WIDTH, GATHOS_SHORTS_IMAGE_HEIGHT,
)
from lib.state import create_run, load_run, update_stage
from lib.gathos_client import generate_tts
from lib.image_provider import generate_image, generate_images_batch, active_provider
from lib.deepgram_client import save_word_timestamps
from lib.transcript import download_youtube, transcribe_video


def _get_audio_duration(audio_path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(audio_path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def _rescale_scenes_to_audio(run_id: str, output_dir: Path):
    scenes_path = output_dir / "scenes.json"
    audio_path = output_dir / "narration.mp3"

    if not scenes_path.exists() or not audio_path.exists():
        return

    audio_sec = _get_audio_duration(audio_path)
    data = json.loads(scenes_path.read_text(encoding='utf-8'))
    old_total = sum(s["duration"] for s in data["scenes"])
    drift = abs(audio_sec - old_total)

    if drift < 0.5:
        print(f"[RESCALE] Scene durations match audio ({old_total:.2f}s). No adjustment needed.")
        return

    scale = audio_sec / old_total
    print(f"[RESCALE] Audio: {audio_sec:.2f}s | Scenes total: {old_total:.2f}s | drift: {drift:+.2f}s — rescaling x{scale:.4f}")

    for s in data["scenes"]:
        s["duration"] = round(s["duration"] * scale, 2)

    residual = round(audio_sec - sum(s["duration"] for s in data["scenes"]), 2)
    data["scenes"][-1]["duration"] = round(data["scenes"][-1]["duration"] + residual, 2)
    data["total_duration_seconds"] = round(sum(s["duration"] for s in data["scenes"]), 2)

    scenes_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[RESCALE] Done — {len(data['scenes'])} scenes rescaled to {data['total_duration_seconds']}s")


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

    channel_style = json.loads(CHANNEL_STYLE_PATH.read_text(encoding='utf-8'))
    captions_enabled = channel_style.get("channel", {}).get("captions_enabled", True)

    if not captions_enabled:
        print("[TIMESTAMPS] Captions disabled for this channel — skipping Deepgram.")
        words_path.write_text("[]", encoding='utf-8')
        update_stage(run_id, "timestamps", "skipped", str(words_path))
        _rescale_scenes_to_audio(run_id, output_dir)
        return

    if not audio_path.exists():
        print("ERROR: narration.mp3 not found. Run TTS stage first.")
        sys.exit(1)

    print("[TIMESTAMPS] Extracting word-level timing...")
    update_stage(run_id, "timestamps", "in_progress")
    save_word_timestamps(audio_path, words_path)
    update_stage(run_id, "timestamps", "complete", str(words_path))
    print(f"[TIMESTAMPS] Done: {words_path}")

    _rescale_scenes_to_audio(run_id, output_dir)


def stage_images(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    scenes_path = output_dir / "scenes.json"
    images_dir = output_dir / "images"

    if not scenes_path.exists():
        print("ERROR: scenes.json not found. Run scenes stage first.")
        sys.exit(1)

    is_shorts = run.get("shorts", False)
    img_width = GATHOS_SHORTS_IMAGE_WIDTH if is_shorts else GATHOS_IMAGE_WIDTH
    img_height = GATHOS_SHORTS_IMAGE_HEIGHT if is_shorts else GATHOS_IMAGE_HEIGHT

    scenes = json.loads(scenes_path.read_text(encoding='utf-8'))
    prompts = []
    for i, scene in enumerate(scenes["scenes"]):
        prompts.append({
            "prompt": scene["image_prompt"],
            "filename": f"scene_{i+1:03d}.png",
            "width": img_width,
            "height": img_height,
        })

    print(f"[IMAGES] Provider: {active_provider()} | Generating {len(prompts)} B-roll images ({img_width}x{img_height})...")
    update_stage(run_id, "images", "in_progress")
    generate_images_batch(prompts, images_dir)
    update_stage(run_id, "images", "complete", str(images_dir))
    update_stage(run_id, "image_review", "pending_review", str(images_dir))
    print(f"[IMAGES] Done: {images_dir}")
    print("[IMAGE REVIEW] Guardrail active. Review the generated B-roll images before rendering.")
    print(f"[IMAGE REVIEW] Images directory: {images_dir}")
    print(f"[IMAGE REVIEW] To approve rendering, run: python -m lib.pipeline --stage approve_images --run-id {run_id}")


def stage_approve_images(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    images_dir = output_dir / "images"

    if not images_dir.exists():
        print("ERROR: images directory not found. Run images stage first.")
        sys.exit(1)

    scenes_path = output_dir / "scenes.json"
    if scenes_path.exists():
        scenes = json.loads(scenes_path.read_text(encoding='utf-8')).get("scenes", [])
        expected = len(scenes)
        existing = len(list(images_dir.glob("scene_*.png")))
        if existing < expected:
            print(f"ERROR: image review cannot be approved yet. Found {existing}/{expected} scene images.")
            sys.exit(1)

    update_stage(run_id, "image_review", "approved", str(images_dir))
    print(f"[IMAGE REVIEW] Approved for render: {images_dir}")


def stage_render(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    import subprocess

    is_shorts = run.get("shorts", False)
    composition = "ShortsVideo" if is_shorts else "ViralBrollVideo"
    remotion_dir = Path(__file__).parent.parent / "remotion"
    final_path = output_dir / "final.mp4"

    image_review = run.get("stages", {}).get("image_review", {})
    if image_review.get("status") != "approved":
        images_dir = output_dir / "images"
        print("ERROR: image review approval required before rendering.")
        print(f"Review the generated B-roll images here: {images_dir}")
        print(f"After user approval, run: python -m lib.pipeline --stage approve_images --run-id {run_id}")
        sys.exit(1)

    _rescale_scenes_to_audio(run_id, output_dir)

    print(f"[RENDER] Rendering {composition} with Remotion...")
    update_stage(run_id, "render", "in_progress")
    subprocess.run(
        [
            "node", "render.mjs",
            str(output_dir),
            run["film_preset"],
            str(final_path),
            composition,
        ],
        cwd=str(remotion_dir),
        check=True,
        timeout=1800,
    )
    update_stage(run_id, "render", "complete", str(final_path))
    print(f"[RENDER] Done: {final_path}")


def stage_thumbnail(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    scenes_path = output_dir / "scenes.json"
    style_path = output_dir / "style.json"
    thumbnail_path = output_dir / "thumbnail.png"

    if not scenes_path.exists():
        print("ERROR: scenes.json not found. Run scenes stage first.")
        sys.exit(1)

    scenes_data = json.loads(scenes_path.read_text(encoding='utf-8'))
    raw_prompt = scenes_data.get("thumbnail_prompt", "")

    style_suffix = ""
    if style_path.exists():
        style_suffix = json.loads(style_path.read_text(encoding='utf-8')).get("style_suffix", "")

    prompt = f"{raw_prompt} {style_suffix}".strip()

    if active_provider() == "openai":
        print("[THUMBNAIL] Skipped — IMAGE_PROVIDER=openai. Generate the thumbnail manually in ChatGPT.")
        update_stage(run_id, "thumbnail", "skipped")
        return

    print("[THUMBNAIL] Generating thumbnail image...")
    update_stage(run_id, "thumbnail", "in_progress")
    generate_image(prompt, thumbnail_path)
    update_stage(run_id, "thumbnail", "complete", str(thumbnail_path))
    print(f"[THUMBNAIL] Done: {thumbnail_path}")


def stage_metadata(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    scenes_path = output_dir / "scenes.json"

    if not scenes_path.exists():
        print("ERROR: scenes.json not found. Run scenes stage first.")
        sys.exit(1)

    scenes_data = json.loads(scenes_path.read_text(encoding='utf-8'))
    title = scenes_data.get("title", "")
    description = scenes_data.get("description", "")
    tags = scenes_data.get("tags", [])
    tags_str = ", ".join(tags)

    metadata_txt = output_dir / "metadata.txt"
    metadata_json = output_dir / "metadata.json"

    metadata_txt.write_text(
        f"TITLE:\n{title}\n\nDESCRIPTION:\n{description}\n\nTAGS:\n{tags_str}\n",
        encoding='utf-8'
    )
    metadata_json.write_text(
        json.dumps({"title": title, "description": description, "tags": tags}, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )

    update_stage(run_id, "metadata", "complete", str(metadata_txt))
    print(f"[METADATA] Done: {metadata_txt}")
    print(f"  Title:       {title}")
    print(f"  Description: {description[:80]}...")
    print(f"  Tags:        {tags_str[:80]}...")


def stage_upload(run_id: str):
    if not YOUTUBE_CLIENT_ID:
        print("[UPLOAD] Skipped — YOUTUBE_CLIENT_ID not set in .env")
        update_stage(run_id, "upload", "skipped")
        return

    from lib.youtube_client import upload_video

    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    final_path = output_dir / "final.mp4"
    scenes_path = output_dir / "scenes.json"

    if not final_path.exists():
        print("ERROR: final.mp4 not found. Run render stage first.")
        sys.exit(1)

    scenes_data = json.loads(scenes_path.read_text(encoding='utf-8'))
    title = scenes_data.get("title", run_id)
    description = scenes_data.get("description", "")
    tags = scenes_data.get("tags", [])

    channel_style = json.loads(CHANNEL_STYLE_PATH.read_text(encoding='utf-8'))
    category_id = channel_style.get("youtube_metadata", {}).get("category_id", "22")

    print(f"[UPLOAD] Uploading to YouTube as private draft...")
    print(f"  Title: {title}")
    update_stage(run_id, "upload", "in_progress")
    video_id = upload_video(final_path, title, description, tags, category_id=category_id, privacy="private")
    url = f"https://youtu.be/{video_id}"
    update_stage(run_id, "upload", "complete", url)
    print(f"[UPLOAD] Done: {url}")


def stage_article_images(run_id: str):
    run = load_run(run_id)
    output_dir = Path(run["output_dir"])
    article_images_json = output_dir / "article_images.json"
    article_images_dir = output_dir / "article_images"

    if not article_images_json.exists():
        print("ERROR: article_images.json not found. Run article stage first.")
        sys.exit(1)

    data = json.loads(article_images_json.read_text(encoding='utf-8'))
    style_path = output_dir / "style.json"
    style_suffix = ""
    if style_path.exists():
        style_suffix = json.loads(style_path.read_text(encoding='utf-8')).get("style_suffix", "")

    article_images_dir.mkdir(parents=True, exist_ok=True)
    prompts = []

    cover = data.get("cover")
    if cover:
        prompts.append({"prompt": f"{cover['prompt']} {style_suffix}".strip(), "filename": cover["filename"]})

    for img in data.get("inline", []):
        prompts.append({"prompt": f"{img['prompt']} {style_suffix}".strip(), "filename": img["filename"]})

    total = len(prompts)
    print(f"[ARTICLE IMAGES] Generating {total} images (1 cover + {total - 1} inline)...")
    update_stage(run_id, "article_images", "in_progress")
    generate_images_batch(prompts, article_images_dir)
    update_stage(run_id, "article_images", "complete", str(article_images_dir))
    print(f"[ARTICLE IMAGES] Done: {article_images_dir}")


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
    "approve_images": stage_approve_images,
    "render": stage_render,
    "thumbnail": stage_thumbnail,
    "metadata": stage_metadata,
    "article_images": stage_article_images,
    "upload": stage_upload,
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
        from lib.config import GATHOS_TTS_API_KEY, GATHOS_IMAGE_API_KEY, DEEPGRAM_API_KEY
        for tool in ["ffmpeg", "ffprobe"]:
            path = shutil.which(tool) or shutil.which(tool, path="/opt/homebrew/bin")
            print(f"  {tool}: {'OK' if path else 'MISSING'} ({path})")
        print(f"  Gathos image key: {'SET' if GATHOS_IMAGE_API_KEY else 'MISSING'}")
        print(f"  Gathos TTS key:   {'SET' if GATHOS_TTS_API_KEY else 'MISSING'}")
        print(f"  Deepgram API key: {'SET' if DEEPGRAM_API_KEY else 'MISSING'}")
        print("Done.")
    elif args.stage and args.run_id:
        if args.stage == "viral_dna" and args.youtube_url:
            stage_viral_dna(args.run_id, args.youtube_url)
        else:
            run_stage(args.run_id, args.stage)
    else:
        parser.print_help()
