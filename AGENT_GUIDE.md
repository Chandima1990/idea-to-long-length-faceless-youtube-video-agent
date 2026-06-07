# Idea-to-Long-Viral-Static-BRoll — Agent Guide

## Overview
This pipeline takes an idea (or YouTube URL) and produces a long-form viral YouTube video (5-20 min) using AI-generated static B-roll images with Ken Burns effects, word-level karaoke captions, and optional film grain.

## MANDATORY: Read Channel Style Guide First
Before doing ANYTHING else, check the `CHANNEL` env var in `.env` (default: `rich_mantra`) and read `channels/<CHANNEL>.json`.

For example: if `CHANNEL=rich_mantra`, read `channels/rich_mantra.json`. If `CHANNEL=tech_explained`, read `channels/tech_explained.json`.

This file defines:
- The channel's host character (name, personality, physical look, voice)
- The base visual style for all videos
- Thumbnail rules (host position, text layout, accent colors)
- Narration tone and signature phrases

Every pipeline stage (script, style card, scenes, thumbnail, article) MUST align with the active channel style file. Do not skip this step.

## Dependencies Check
Before starting, run:
```bash
PYTHONPATH=/Users/psrmanju2/psr_workspace/idea-to-long-viral-static-broll python3 -m lib.pipeline --check
```

## Two Input Modes

### Mode A: From Idea
User provides a topic/idea directly. Skip to Step 2.

### Mode B: From YouTube URL
1. Run viral DNA extraction:
```bash
PYTHONPATH=/Users/psrmanju2/psr_workspace/idea-to-long-viral-static-broll python3 -m lib.pipeline --stage viral_dna --run-id <RUN_ID> --youtube-url "<URL>"
```
2. Read `skills/viral-dna-extractor.md`
3. Read the transcript at `outputs/<run_id>/transcript.txt`
4. Perform the 3-level dissection (Content → Structure → Psychology)
5. Save analysis to `outputs/<run_id>/viral_dna.json`
6. Present 5 new topic suggestions to the user
7. Wait for user to pick one
8. Proceed to Step 2 with chosen topic + viral DNA

## Pipeline Steps

### Step 1: Create Run

**Before asking for a topic — consider two strategic angles:**

**Trends Bias:** A trend wave carries any quality level further than perfect timing alone. If the user has a topic, ask: can it be attached to a current financial news event, economic moment, or cultural trend? A general "index fund" video competes with thousands; "index funds during a rate cut" rides a wave. Suggest a trend angle if one naturally fits.

**Recency Bias:** Older videos are algorithmically disadvantaged. Before creating a brand new topic, check `outputs/` for any run on a similar theme. A "v2" video — same core topic, updated with new data, comments, and a fresh angle — often outperforms the original because it starts with an existing audience signal. Mention this option if a related run exists.

Ask the user:
1. "What's your idea/topic?" (or use the topic from Mode B)
2. "How long should the video be?" (5 / 10 / 15 / 20 minutes)
3. "What visual vibe?"
   - Clean Modern (no effects)
   - Vintage Film (warm tones, 35mm grain)
   - Black & White Documentary (B&W, grain, classic)
   - Dark Cinematic (desaturated, deep shadows)
   - Sepia Archival (aged, heavy grain)
   - None (raw images)
4. "What voice?" (josh / koko / pixxy / prof / rochie / spraky / custom)

Create the run state (the pipeline CLI handles this, or create manually):
```python
from lib.state import create_run
run = create_run(title="<topic>", mode="idea"|"viral_dna", voice="josh", film_preset="vintage_film", duration_minutes=10)
```

### Step 2: Write Script
1. Read `skills/viral-script-writer.md`
2. If Mode B: also read `outputs/<run_id>/viral_dna.json` for Level 2+3 guidance
3. Write the narration script following all rules
4. Save to `outputs/<run_id>/script.md`
5. Update state: `update_stage(run_id, "script", "complete")`

### Step 3: Style Card + Characters + Scene Breakdown
1. Read `skills/cinematographic-breakdown.md`
2. Confirm you have the active channel style file loaded (already read at top)
3. Read `outputs/<run_id>/script.md`
4. Generate:
   - Style Card → base on active channel style `visual_style`, adapt to topic → save to `outputs/<run_id>/style.json`
   - Characters → ALWAYS include host from active channel style `host` as first entry → save to `outputs/<run_id>/characters.json`
   - Scene breakdown → use channel thumbnail rules for `thumbnail_prompt` → save to `outputs/<run_id>/scenes.json`
5. Update state for all three stages

### Step 3b: Write Medium Article
1. Read `skills/article-writer.md`
2. Read `outputs/<run_id>/script.md` and `outputs/<run_id>/scenes.json`
3. Write the Medium article and image prompts:
   - Article → save to `outputs/<run_id>/article.md`
   - Image prompts → save to `outputs/<run_id>/article_images.json`
4. Update state: `update_stage(run_id, "article", "complete")`

### Step 4: Generate TTS
```bash
PYTHONPATH=/Users/psrmanju2/psr_workspace/idea-to-long-viral-static-broll python3 -m lib.pipeline --stage tts --run-id <RUN_ID>
```
Timeout: 10+ minutes. Do NOT let local timeout kill this.

### Step 5: Extract Word Timestamps
```bash
PYTHONPATH=/Users/psrmanju2/psr_workspace/idea-to-long-viral-static-broll python3 -m lib.pipeline --stage timestamps --run-id <RUN_ID>
```

### Step 6: Generate B-Roll Images + Article Images
Run both in parallel (background):
```bash
# B-roll images
python -m lib.pipeline --stage images --run-id <RUN_ID>
# Article images (cover + inline)
python -m lib.pipeline --stage article_images --run-id <RUN_ID>
```
Timeout: 10+ minutes per batch. Do NOT let local timeout kill this.

### Step 7: Mandatory Image Review Approval
After B-roll images finish, STOP before rendering.

The `images` stage sets `image_review` to `pending_review`. The user must review:
```bash
outputs/<RUN_ID>/images/
```

Report the image directory to the user and wait for their approval signal. Do not render until the user explicitly approves the generated B-roll images.

After approval, record it:
```bash
python -m lib.pipeline --stage approve_images --run-id <RUN_ID>
```

The render stage will refuse to run until `image_review` is `approved`.

### Step 8: Render Final Video
```bash
cd /Users/psrmanju2/psr_workspace/idea-to-long-viral-static-broll/remotion && npx remotion render ViralBrollVideo ../outputs/<RUN_ID>/final.mp4 --props '{"outputDir":"../outputs/<RUN_ID>","filmPreset":"<PRESET>"}'
```
Timeout: 10+ minutes. Do NOT let local timeout kill this.

### Step 8b: Generate Metadata
```bash
python -m lib.pipeline --stage metadata --run-id <RUN_ID>
```
Generates `metadata.txt` and `metadata.json` from `scenes.json` (title, description, tags).

**Thumbnail note:** If `IMAGE_PROVIDER=openai`, skip the thumbnail stage — the user generates thumbnails manually in ChatGPT. Only run thumbnail for `gathos`/`gemini`/`comfyui` providers.

### Step 8c: Upload to YouTube
```bash
python -m lib.pipeline --stage upload --run-id <RUN_ID>
```
Uploads `final.mp4` as a **private draft** using credentials from `.env`. Reads title/description/tags from `scenes.json`. Returns a `youtu.be/` URL when done.

Requires in `.env`: `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`.
If any are missing the stage silently skips. The video stays private — the user reviews and publishes manually.

### Step 9: Output
Final deliverables in `outputs/<run_id>/`:
- `final.mp4` — the rendered video
- `metadata.txt` / `metadata.json` — title, description, tags
- `article.md` — Medium article (ready to paste)
- `article_images/cover.png` — Medium cover image
- `article_images/section_*.png` — inline article images
- `scenes.json` — full scene data

Report all output paths to the user.
