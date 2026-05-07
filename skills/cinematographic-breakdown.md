# Cinematographic Breakdown

## Input
- `outputs/<run_id>/script.md` — the narration script
- `duration_minutes` — target length

## Process

### Part 1: STYLE CARD
Read the entire script and derive a unified visual style:

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
Parse the script for any recurring people/characters. For each, create a character card:

```json
{
  "characters": [
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

If no recurring characters (e.g., a nature documentary), save empty array.

### Part 3: SCENE BREAKDOWN
Split the script into visual segments. Each segment = one B-roll image.

**Segment duration:** 7-15 seconds (default 10s)
**Formula:** `duration = max(7, min(15, round(word_count / 2.5)))`
**Split at sentence boundaries only** — never mid-sentence.

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
  "thumbnail_prompt": "YouTube thumbnail, 16:9. Cartoon animated bald overweight man with glasses showing shocked/worried expression, bold black outlines, flat Family-Guy-style cartoon. Character on the right side. Left side: large bold white text on dark red background with the video's key hook (2-4 words, ALL CAPS). Center: simple flat cartoon graphic illustrating the video's core concept (chart, icon, dollar sign, etc.). Dark charcoal background, high-contrast yellow and red accents, bold black outlines on all elements, flat 2D cartoon style, no gradients, no photorealism.",
  "total_scenes": 60,
  "total_duration_seconds": 600,
  "scenes": [...]
}
```

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
