# Flux Image Prompting (local ComfyUI provider)

Apply this **only when `IMAGE_PROVIDER=comfyui`** (local Flux.2 Klein). These are
*technical limits of the model*, layered on top of the active channel's art style
— they do NOT replace the channel style. Pull the look (watercolor, macro photo,
flat vector, etc.) from `channels/<CHANNEL>.json` as usual; add the rules below so
Flux doesn't hallucinate.

## Why this exists

Flux is excellent at scenes but unreliable at dense text, multi-value data, and
multi-column layouts. Left unconstrained it invents numbers and phantom table
columns. Constrain the *information density*, not the art direction.

## Text and numbers

- **Max 2–3 specific numeric values per image.** `$47K` is fine; a 5-row table
  with 5 different values will hallucinate wrong numbers.
- **Use SHORT alphanumeric tokens, do NOT spell numbers out.** Tested on
  Flux.2 Klein (2026-06-06): it renders `$186K` / `$47K` correctly but garbles
  spelled-out words ("forty-seven thousand dollars" → "forty-siven thouhaan
  dollars"). This is the OPPOSITE of generic "spell it out" advice written for
  other models. Write just `$47K`, and add "only this short dollar label, no
  other text or words" so the model doesn't invent a garbled caption.
- **When in doubt, use NO text at all** and let shapes/colors/icons carry the
  meaning — this is the single most reliable path on this model (see the race
  track / pie chart / magnifying-glass cases that came out flawless).
- **Never describe a comparison table** with multiple data columns — Flux adds a
  hallucinated second column every time. Use ONE column/axis of values only.
- If a scene genuinely needs many numbers, **describe the shape of the data**
  instead of the values: "four tall green bars of roughly equal height, one short
  red bar about one quarter as tall."

## Layout

- Describe structure as **"vertical ranked list"** or **"horizontal bar chart"** —
  never "scoreboard" or "table" (both trigger multi-column hallucination).
- When a character shares the frame with data: **character on the LEFT, infographic
  on the RIGHT.** Never a centered character with the infographic behind them.
- Say **"one value per row only"** explicitly when listing data rows.

## Style — comes from the channel, NOT this file

The art style (medium, palette, background, outlines) is whatever
`channels/<CHANNEL>.json` `visual_style` + the run's `style.json` specify. Examples:

- `rich_mantra` → flat 2D vector, bold black outlines, solid fills, white
  background, no gradients/shadows, 16:9.
- `amma_sindu` → soft pastel watercolor, rounded outlines, dreamy light, 16:9.
- `wonder_lab` → vivid macro photography, 16:9.

Always append the channel's `style_suffix` and `16:9 aspect ratio`. Do **not**
force the flat-vector white-background look onto channels that aren't vector —
that was a `rich_mantra`-specific instruction, not a universal Flux rule.

## Optional negative prompt

Set `COMFYUI_NEGATIVE_PROMPT` in `.env` for things to suppress globally, e.g.:
`text, watermark, signature, blurry, extra fingers, deformed hands, second column`.
