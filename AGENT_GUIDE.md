# Idea-to-Long-Viral-Static-BRoll — Agent Guide

## Overview
This pipeline takes an idea (or YouTube URL) and produces a long-form viral YouTube video (5-20 min) using AI-generated static B-roll images with Ken Burns effects, word-level karaoke captions, and optional film grain.

## MANDATORY: Read Channel Style Guide First
Before doing ANYTHING else, read `channel_style.json` in the project root.

This file defines:
- The channel's host character (name, personality, physical look, voice)
- The base visual style for all videos
- Thumbnail rules (host position, text layout, accent colors)
- Narration tone and signature phrases

Every pipeline stage (script, style card, scenes, thumbnail, article) MUST align with `channel_style.json`. Do not skip this step.

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
2. Read `channel_style.json` (already read at top — confirm you have it loaded)
3. Read `outputs/<run_id>/script.md`
4. Generate:
   - Style Card → base on `channel_style.visual_style`, adapt to topic → save to `outputs/<run_id>/style.json`
   - Characters → ALWAYS include host from `channel_style.host` as first entry → save to `outputs/<run_id>/characters.json`
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

### Step 7: Render Final Video
```bash
cd /Users/psrmanju2/psr_workspace/idea-to-long-viral-static-broll/remotion && npx remotion render ViralBrollVideo ../outputs/<RUN_ID>/final.mp4 --props '{"outputDir":"../outputs/<RUN_ID>","filmPreset":"<PRESET>"}'
```
Timeout: 10+ minutes. Do NOT let local timeout kill this.

### Step 8: Output
Final deliverables in `outputs/<run_id>/`:
- `final.mp4` — the rendered video
- `thumbnail.png` — YouTube thumbnail
- `metadata.txt` / `metadata.json` — title, description, tags
- `article.md` — Medium article (ready to paste)
- `article_images/cover.png` — Medium cover image
- `article_images/section_*.png` — inline article images
- `scenes.json` — full scene data

Report all output paths to the user.
