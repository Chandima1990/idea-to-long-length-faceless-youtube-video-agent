# Article Writer — Medium Post

## Input
- `channels/<CHANNEL>.json (path from CHANNEL_STYLE_PATH in lib/config.py)` — **Read this first.** It defines the host's personality and narration style. The article tone must match the host's voice.
- `outputs/<run_id>/script.md` — the narration script (source of truth for facts/claims)
- `outputs/<run_id>/scenes.json` — title, description, tags
- `outputs/<run_id>/style.json` — visual style for image prompts
- `outputs/<run_id>/viral_dna.json` — (if exists) hook template and psychological triggers

## Channel Voice (from channels/<CHANNEL>.json (path from CHANNEL_STYLE_PATH in lib/config.py))
Extract `host.personality` and `host.narration_style` from `channels/<CHANNEL>.json (path from CHANNEL_STYLE_PATH in lib/config.py)`. The article must read like this same host wrote it — same conversational warmth, same sentence rhythm, same use of "you" to address the reader. It is the script's written cousin, not a different voice.

## Output Files

### 1. `outputs/<run_id>/article.md`
The full Medium article in Markdown format.

### 2. `outputs/<run_id>/article_images.json`
Image generation prompts for cover + inline images.

---

## Article Spec

**Length:** 600–900 words (reading time: ~3–4 min)
**Tone:** Conversational, direct, slightly provocative — same voice as the video script but written for readers, not listeners. Use short paragraphs. No jargon.
**Structure:**
- No intro fluff. Start with a hook sentence.
- Use H2 headings for sections (2–3 sections max)
- 1 inline image per section (placed after the section heading)
- Closing paragraph with a soft CTA linking to the YouTube video

---

## Article Format (Markdown)

```markdown
![Cover](article_images/cover.png)

# [Title — rewritten for Medium readers, not copied from scenes.json verbatim]

*[Subtitle — one sentence, italic. Raises curiosity with a specific hint (a number, a comparison, a revealed tension). Not click-baity — the reader should feel informed, not tricked.]*

[Hook sentence — bold, one line]

[Introduction: 2–3 short paragraphs. Establish the problem/tension. Mirror the video hook but rewritten for reading.]

---

## [Section 1 Heading]

![Section 1](article_images/section_1.png)

[Section body: 150–200 words. Core argument or data point. Use specific numbers from the script.]

---

## [Section 2 Heading]

![Section 2](article_images/section_2.png)

[Section body: 150–200 words. Second major point or counter-argument.]

---

## [Section 3 Heading — optional]

![Section 3](article_images/section_3.png)

[Section body: 100–150 words. Decision framework or "who this applies to".]

---

[Closing paragraph: 2–3 sentences. Restate the key insight. Soft CTA: "Watch the full breakdown on YouTube."]

*Tags: [comma-separated tags from scenes.json]*
```

---

## Image Prompts Spec

Write image prompts that match the run's `style_suffix`. Each prompt should visually illustrate the SECTION content, not be generic.

The `article_images.json` format:

```json
{
  "cover": {
    "filename": "cover.png",
    "prompt": "Eye-catching cover image for a Medium article about [topic]. [3-4 sentence visual description. Should grab attention at thumbnail size. Do NOT include text overlays.]"
  },
  "inline": [
    {
      "filename": "section_1.png",
      "prompt": "Illustration for the section about [specific point]. [2-3 sentence visual description matching style_suffix.]"
    },
    {
      "filename": "section_2.png",
      "prompt": "..."
    }
  ]
}
```

**Cover image rules:**
- 16:9, eye-catching, visually bold
- Represents the article's central tension or reveal
- No text overlays in the prompt (Medium adds its own title on the cover)
- Match the run's style_suffix

**Inline image rules:**
- Illustrate the specific section — not a generic topic image
- Each must be visually distinct from the others
- Match the run's style_suffix

---

## Title + Subtitle Rules

**Title:**
- Rewrite for Medium — not a copy of the YouTube title
- Creates curiosity through tension, contrast, or an implied reveal
- Under 70 characters
- Avoid: "X Things", "You Won't Believe", fake urgency

**Subtitle (italic line directly under title):**
- One sentence, specific — includes a number, a comparison, or a named tension
- Gives the reader a genuine hint of what they will learn
- Reads like something a smart friend would say, not a tabloid headline
- Example: *A decade-long comparison of two people who started with the same $80,000 reveals what the listing price never mentions.*

---

## Quality Checks
1. Article word count is 600–900 words
2. Article facts/numbers match the script exactly (do not invent new stats)
3. All image filenames in article.md match keys in article_images.json
4. Cover image path is `article_images/cover.png`
5. Inline images are `article_images/section_1.png`, `section_2.png`, etc.
6. No em dashes (use commas or periods instead — Medium rendering can be inconsistent)
7. Article reads as standalone content — someone who hasn't watched the video should understand it fully
