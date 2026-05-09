# Cinematic Minifigure Shorts Breakdown

## Input
- `outputs/<run_id>/script.md` - narration script
- `duration_minutes` - target length, default 1.5 minutes

## Process

### Part 1: Style Card
Use this exact channel aesthetic as the base style. Do not replace it with a new visual style:

```json
{
  "style_name": "Cinematic Macro Plastic Minifigure Diorama",
  "photographic_style": "cinematic macro photography of a 3D rendered plastic building block minifigure",
  "color_palette": "olive green jacket, red beret, cracked tan desert ground, twilight blues, soft moon glow, high-contrast black shadows",
  "lighting": "dramatic cinematic lighting, soft bright backlight creating rim light on the character's left side, high-contrast soft fill from the front",
  "camera": "vertical 9:16 ground-level macro camera, very shallow depth of field, heavy bokeh, figure razor sharp",
  "texture": "realistic glossy plastic with subtle subsurface scattering, molded plastic hair, painted-on facial features, tangible miniature scale",
  "mood": "tense, cinematic, miniature war-story atmosphere",
  "style_suffix": "Cinematic macro photography of a 3D rendered plastic building block minifigure (LEGO style). The character has painted-on facial features, molded plastic hair, and wears an olive-green military jacket with a red beret. The figure is standing in a miniature diorama on cracked, arid desert ground. The camera is at ground level with a very shallow depth of field (heavy bokeh), keeping the figure in razor-sharp focus while heavily blurring the background. The background is a twilight scene with a soft glowing moon. Lighting is dramatic and cinematic, featuring a soft, bright backlight acting as a rim light on the character's left side, with a high-contrast soft fill light in the front. Materials must look like realistic, glossy plastic with subtle subsurface scattering to appear tangible. Vertical 9:16 composition, no text, no watermark."
}
```

Save to `outputs/<run_id>/style.json`.

### Part 2: Characters
The recurring visual character is the minifigure. If the script has named people, treat them as story roles represented by the same channel minifigure unless the user explicitly asks for additional characters.

Save to `outputs/<run_id>/characters.json`:

```json
{
  "characters": [
    {
      "id": "main_minifigure",
      "name": "Main minifigure narrator",
      "description": "A 3D rendered glossy plastic building block minifigure with painted-on facial features, molded plastic hair, olive-green military jacket, and red beret",
      "appears_in_scenes": []
    }
  ]
}
```

Fill `appears_in_scenes` after the scene list is complete.

### Part 3: Scene Breakdown
Split the script into visual segments. Each segment is one generated image.

Segment duration:
- 3-6 seconds
- Default to 4 seconds
- Formula: `duration = max(3, min(6, round(word_count / 2.5)))`
- Split at sentence boundaries only. Never split mid-sentence.

For each segment, generate:

```json
{
  "scene_number": 1,
  "narration_text": "exact words spoken during this segment",
  "word_count": 10,
  "duration": 4,
  "image_prompt": "3-6 sentence cinematographic shot description ending with style_suffix",
  "shot_type": "wide | medium | close_up | detail | aerial | establishing",
  "ken_burns": "pan_right | pan_left | zoom_in | zoom_out | pan_up | zoom_in_pan_right",
  "transition": "dissolve | white_flash | fade_black",
  "characters_in_scene": ["main_minifigure"]
}
```

## Image Prompt Rules

The image prompt is a cinematographer's shot description, not a topic summary.

Do:
- Keep the minifigure visible in every scene unless the narration explicitly requires a detail insert.
- Place the character so the torso/chest remains near the center for captions.
- Describe a specific pose, prop, foreground object, or desert-diorama arrangement that matches the narration.
- Include ground-level camera angle, shallow depth of field, rim light, moonlit twilight background, and glossy plastic material.
- End every image prompt with the exact `style_suffix`.
- Use vertical 9:16 composition.

Don't:
- Include text, signs, labels, UI, watermark, or subtitles in image prompts.
- Drift into generic photoreal people, realistic soldiers, realistic weapons, or non-plastic characters.
- Reuse the same composition for consecutive scenes.
- Crop off the torso where captions need to sit.

## Ken Burns Assignment Rules
- Establishing desert diorama shots -> `pan_right` or `pan_left`
- Close-up faces or emotional beats -> `zoom_in`
- Reveals or comparisons -> `zoom_out`
- Tall props, moon, towers, cliffs -> `pan_up`
- Action beats -> `zoom_in_pan_right`
- Alternate directions between consecutive scenes.

## Transition Rules
- Default: `dissolve`
- Use `white_flash` only for major reveals, max 2 in a 90-second Short.
- Use `fade_black` for final scene only.

## Output
Save to `outputs/<run_id>/scenes.json`:

```json
{
  "title": "video title",
  "description": "YouTube Shorts description, 1-2 sentences plus keywords",
  "tags": ["tag1", "tag2"],
  "thumbnail_prompt": "Vertical 9:16 YouTube Shorts thumbnail. The same glossy plastic building block minifigure in olive-green military jacket and red beret stands on cracked desert ground under a twilight moon, dramatic rim light and hard black shadows, cinematic macro depth of field. Leave clean negative space for platform crop. No text, no watermark.",
  "total_scenes": 22,
  "total_duration_seconds": 90,
  "scenes": []
}
```

## Quality Checks
1. All `narration_text` concatenated equals the original script with no words added or lost.
2. All scenes are 3-6 seconds unless audio rescaling later adjusts them.
3. Every image prompt is 3-6 sentences.
4. Every image prompt directly depicts its narration.
5. The exact `style_suffix` appears in every image prompt.
6. The main minifigure appears in every scene unless a detail insert is clearly justified.
7. Ken Burns directions alternate.
8. No three consecutive scenes use the same shot type.
9. Transitions are mostly dissolve, with final scene using fade_black.
