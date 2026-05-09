# Idea-to-Shorts Cinematic Minifigure Video Agent

## Overview
This pipeline takes an idea or YouTube URL and produces a vertical YouTube Shorts-style video, preferably about 1.5 minutes long, using AI-generated cinematic macro minifigure visuals, Gathos TTS, word-level center captions, and Remotion rendering.

## Dependencies Check
Before starting, run:
```bash
PYTHONPATH=. python -m lib.pipeline --check
```

## Two Input Modes

### Mode A: From Idea
User provides a topic/idea directly. Skip to Step 2.

### Mode B: From YouTube URL
1. Run viral DNA extraction:
```bash
PYTHONPATH=. python -m lib.pipeline --stage viral_dna --run-id <RUN_ID> --youtube-url "<URL>"
```
2. Read `skills/viral-dna-extractor.md`.
3. Read the transcript at `outputs/<run_id>/transcript.txt`.
4. Perform the 3-level dissection: Content, Structure, Psychology.
5. Save analysis to `outputs/<run_id>/viral_dna.json`.
6. Present 5 new topic suggestions to the user.
7. Wait for user to pick one.
8. Proceed to Step 2 with chosen topic plus viral DNA.

## Pipeline Steps

### Step 1: Create Run
Ask the user only for missing information:
1. "What's your idea/topic?" (or use the topic from Mode B)
2. "How long should the video be?" Default to 1.5 minutes unless the user says otherwise.
3. "What visual vibe?" Default to the channel style: cinematic macro 3D rendered plastic building block minifigure, olive-green military jacket, red beret, cracked desert diorama, twilight moon, shallow depth of field, glossy plastic, dramatic rim/back light.
4. "What voice?" Default to `pixxy` in Gathos for a deeper narration voice.

Create the run state:
```python
from lib.state import create_run
run = create_run(
    title="<topic>",
    mode="idea" | "viral_dna",
    voice="pixxy",
    film_preset="dark_cinematic",
    duration_minutes=1.5,
)
```

### Step 2: Write Script
1. Read `skills/viral-script-writer.md`.
2. If Mode B: also read `outputs/<run_id>/viral_dna.json` for Level 2 and Level 3 guidance.
3. Write the narration script following all rules.
4. Save to `outputs/<run_id>/script.md`.
5. Update state: `update_stage(run_id, "script", "complete")`.

### Step 3: Style Card, Characters, Scene Breakdown
1. Read `skills/cinematographic-breakdown.md`.
2. Read `outputs/<run_id>/script.md`.
3. Generate:
   - Style Card -> save to `outputs/<run_id>/style.json`
   - Characters -> save to `outputs/<run_id>/characters.json`
   - Scene breakdown -> save to `outputs/<run_id>/scenes.json`
4. Update state for all three stages.

### Step 4: Generate TTS
```bash
PYTHONPATH=. python -m lib.pipeline --stage tts --run-id <RUN_ID>
```
Timeout: 10+ minutes. Do not let local timeout kill this.

### Step 5: Extract Word Timestamps
```bash
PYTHONPATH=. python -m lib.pipeline --stage timestamps --run-id <RUN_ID>
```

### Step 6: Generate Scene Images
```bash
PYTHONPATH=. python -m lib.pipeline --stage images --run-id <RUN_ID>
```
Timeout: 10+ minutes per batch. Do not let local timeout kill this.

### Step 7: Render Final Video
```bash
PYTHONPATH=. python -m lib.pipeline --stage render --run-id <RUN_ID>
```
The renderer outputs vertical 1080x1920 MP4 with centered word-by-word captions.

### Step 8: Optional Thumbnail And Metadata
```bash
PYTHONPATH=. python -m lib.pipeline --stage thumbnail --run-id <RUN_ID>
PYTHONPATH=. python -m lib.pipeline --stage metadata --run-id <RUN_ID>
```

## Output
Final deliverables in `outputs/<run_id>/`:
- `final.mp4` - rendered vertical Shorts video
- `narration.mp3` - generated voiceover
- `words.json` - word-level caption timestamps
- `scenes.json` - full scene data
- `images/scene_*.png` - generated vertical scene visuals
- `thumbnail.png` - optional YouTube thumbnail
- `metadata.txt` / `metadata.json` - title, description, tags

Report all output paths to the user.
