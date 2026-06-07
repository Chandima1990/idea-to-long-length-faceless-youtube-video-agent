# Cinematographic Breakdown

## Input
- `channels/<CHANNEL>.json` — **Read this first** (path from `CHANNEL_STYLE_PATH` in `lib/config.py`; default `channels/rich_mantra.json`). It defines the channel's base visual style, host character (physical description), and thumbnail rules. All three parts of this breakdown must align with it.
- `outputs/<run_id>/script.md` — the narration script
- `duration_minutes` — target length

## Provider check (before writing image prompts)
Check `IMAGE_PROVIDER` in `lib/config.py` / `.env`. If it is `comfyui` (local
Flux), **also read [`skills/flux-image-prompting.md`](flux-image-prompting.md)**
and apply its number/table/layout constraints to every `image_prompt` — layered
on top of the channel style, not replacing it. For `gathos`/`gemini`, skip it.

## Process

### Part 1: STYLE CARD
Read the active channel style file (`visual_style` section) and the script, then derive a unified visual style.

**Rules for style derivation:**
- Start from `channel_style.visual_style.style_suffix_base` — this is the brand DNA that MUST appear in every video's style_suffix
- Adapt the style to the video's specific topic (e.g., for a finance video: add "clean financial infographic elements"; for a history video: add "cinematic period-accurate documentary")
- The `style_suffix` you generate must include the channel's base elements PLUS topic-specific elements
- Never create a style that contradicts the channel's `visual_style.mood` or `visual_style.photographic_style`

```json
{
  "style_name": "descriptive name (e.g., 'Epic Prehistoric Documentary')",
  "photographic_style": "what kind of imagery (e.g., 'photorealistic BBC documentary')",
  "color_palette": "dominant colors and tones",
  "lighting": "lighting approach (e.g., 'natural golden hour, misty mornings')",
  "camera": "composition approach (e.g., 'wide-angle, rule of thirds, layered depth')",
  "texture": "surface quality (e.g., 'high detail natural textures')",
  "mood": "emotional tone (e.g., 'awe-inspiring, epic, ancient')",
  "style_suffix": "append to EVERY image prompt for consistency"
}
```

Save to `outputs/<run_id>/style.json`

The `style_suffix` is the KEY to consistency. It gets appended word-for-word to every image prompt. Example:
> "cinematic documentary photography, photorealistic, earth tones, natural lighting, shot on RED V-Raptor, 8K detail"

### Part 2: CHARACTERS
Read the active channel style file (`host` section) first.

**Always include the channel host** as the first character entry, using `channel_style.host.physical_description` verbatim as their `description`. The host's `id` is their name lowercased (e.g., `"josh"`). Scan the script for scenes where the narration uses first-person action ("I tried", "I asked", "I found", "I looked") or explicitly calls out the host — those are the `appears_in_scenes` values.

If `channel_style.host.appears_in_broll` is `false`, set `appears_in_scenes` to an empty array (host is voice-only).

If `channel_style.host.appears_in_broll` is `true`, scan the entire script first and select scene numbers where Josh should appear, guided by `host.broll_inclusion_rules`. Pick scenes where:
- Narration is direct-address ("you", "I", "we") or delivers an emotional hook or reveal
- The scene is visually simple enough for Josh to appear without crowding financial elements
- A Josh pose would meaningfully match the narration (pointing for insights, gesturing at a chart, reacting to a bad number, thumbs up for a positive step)

Skip scenes that are chart-heavy, data-heavy, or abstract/concept-driven. Aim for 25-35% of total scenes. Record the selected scene numbers in `appears_in_scenes`.

Then parse the script for any OTHER recurring people/characters and add them:

```json
{
  "characters": [
    {
      "id": "josh",
      "name": "Josh",
      "description": "[copy channel_style.host.physical_description verbatim here]",
      "appears_in_scenes": [2, 8, 15]
    },
    {
      "id": "george",
      "name": "George Hadley",
      "description": "A weathered middle-aged American farmer in his 50s, strong build, sun-tanned face with stubble, wearing a tan baseball cap and blue denim work shirt, brown leather boots",
      "appears_in_scenes": [1, 3, 7, 12, 18]
    }
  ]
}
```

Save to `outputs/<run_id>/characters.json`

### Part 3: SCENE BREAKDOWN
Split the script into visual segments. Each segment = one B-roll image.

**Segment duration:** 7-15 seconds (default 10s)
**Formula:** `duration = max(7, min(15, round(word_count / 2.5)))`
**Split at sentence boundaries only** — never mid-sentence.

**SCENE COUNT MUST BE DIVISIBLE BY 4** (OpenAI collage pipeline constraint):
The total number of scenes must be a multiple of 4 (e.g., 24, 28, 32, 36).
If your natural split produces a non-multiple, merge the last 1-3 short scenes into adjacent scenes OR split a long scene into two to reach the next multiple of 4.
Never leave a remainder — individual scene generation calls to OpenAI cost more and produce inconsistent style.

For EACH segment, generate:

```json
{
  "scene_number": 1,
  "narration_text": "exact words spoken during this segment",
  "word_count": 25,
  "duration": 10,
  "image_prompt": "3-6 sentence cinematographic shot description (SEE RULES BELOW)",
  "shot_type": "wide | medium | close_up | detail | aerial | establishing",
  "ken_burns": "pan_right | pan_left | zoom_in | zoom_out | pan_up | zoom_in_pan_right",
  "transition": "dissolve | white_flash | fade_black",
  "characters_in_scene": ["george"]
}
```

### IMAGE PROMPT RULES (Critical)

The image prompt is a CINEMATOGRAPHER'S SHOT DESCRIPTION, not a topic summary.

**DO:**
- Describe the SPECIFIC ACTION matching the narration verb
- Include character descriptions (copy from character card) when characters appear
- Specify camera angle, lighting, depth of field
- End with the style_suffix from the Style Card
- Use 3-6 detailed sentences

**DON'T:**
- Write generic topic illustrations ("a farmer in a field")
- Use abstract concepts ("the feeling of loss")
- Include text, watermarks, or UI elements in the prompt
- Reuse the same composition for consecutive scenes

**WHEN JOSH APPEARS IN A SCENE** (`characters_in_scene` includes `"josh"`):
- Use `channel_style.host.broll_character_prompt` verbatim as the character description — do not paraphrase or abbreviate it
- Match Josh's pose/expression to the scene emotion: pointing up for an insight, gesturing at a chart for a data reveal, arms crossed or concerned face for a warning, thumbs up for a positive outcome, neutral presenting for explanations
- Keep infographic elements (charts, icons, arrows) as the visual anchor — Josh complements them, not the reverse
- Place Josh naturally: left or center for direct-address/presenter poses, right side for pointing/reacting poses

**EXAMPLE:**
Narration: "George knelt in the freshly turned earth and placed the first sapling into the hole he'd dug that morning."

BAD: "A farmer planting a tree"

GOOD: "A weathered middle-aged American farmer in his 50s, tan cap, blue denim shirt, kneeling in dark freshly-tilled soil, carefully placing a small green sapling into a shallow hole. Golden hour sunlight from the left casts long shadows across the field. Wide-angle shot, low camera position at ground level, shallow depth of field with blurred Kansas flatlands in the background. Cinematic documentary photography, photorealistic, earth tones, natural lighting, 8K detail."

### KEN BURNS ASSIGNMENT RULES
- **Landscapes / establishing shots** → `pan_right` or `pan_left`
- **Close-up faces / emotional moments** → `zoom_in`
- **Group scenes / reveals** → `zoom_out`
- **Tall subjects (buildings, mountains)** → `pan_up`
- **Action / dynamic moments** → `zoom_in_pan_right`
- **ALTERNATE** directions between consecutive scenes (never same direction twice in a row)

### TRANSITION RULES
- Default: `dissolve` (smooth crossfade)
- Use `white_flash` for major chapter breaks / dramatic reveals (max 3-4 per video)
- Use `fade_black` for final scene only

### SHOT TYPE VARIETY
Ensure variety across the video:
- No more than 2 consecutive scenes with the same shot_type
- Mix of: 30% wide/aerial, 30% medium, 25% close_up/detail, 15% establishing
- Opening scene should be `establishing` or `aerial`
- Closing scene should be `wide` or `establishing`

## Output
Save to `outputs/<run_id>/scenes.json`:

```json
{
  "title": "video title",
  "description": "YouTube description (2-3 sentences + keywords)",
  "tags": ["tag1", "tag2"],
  "thumbnail_prompt": "[Generated from channel_style.json — see Thumbnail Prompt Rules below]",
  "total_scenes": 60,
  "total_duration_seconds": 600,
  "scenes": [...]
}
```

### THUMBNAIL PROMPT RULES
Read the active channel style file (`thumbnail` section) and compose the `thumbnail_prompt` by filling in this template from `thumbnail.thumbnail_prompt_template`:

1. Replace `HOST_DESCRIPTION` with `thumbnail.host_image_description`
2. Replace `REACTION_TYPE` with a reaction appropriate for the video topic (surprised / excited / concerned / intrigued)
3. Replace `VIDEO_HOOK` with 2-5 word ALL-CAPS version of the video's core hook
4. Replace `ACCENT_COLOR` with one of the `thumbnail.accent_colors` (pick the one that fits the emotional tone)
5. Replace `BACKGROUND_STYLE` with `thumbnail.background_style`

If `thumbnail.include_host` is `false`, omit the host from the prompt entirely and use a bold graphic/icon composition instead.

## Quality Checks
1. All narration_text concatenated = original script (no words added or lost)
2. All scenes 7-15 seconds
3. Image prompts are 3-6 sentences each
4. EVERY image prompt directly depicts its narration (verify scene by scene)
5. style_suffix from Style Card appears in EVERY image prompt
6. Character descriptions from characters.json are injected when character appears
7. Ken Burns directions alternate (no consecutive repeats)
8. Shot types are varied (no 3+ consecutive same type)
9. Transitions: mostly dissolve, 3-4 white_flash max, fade_black only at end
