# Viral Shorts Script Writer

## Input
Either:
- A topic/idea (Mode A: direct idea)
- A topic plus viral DNA analysis (Mode B: from YouTube dissection)

Also receives:
- `duration_minutes` - target video length. Default is 1.5 minutes.

## Pacing
- Use about 2.5 words per second.
- 1.5 min = about 225 words.
- Stay within +/-10% of the target word count unless the user asks for a different length.

## Script Rules

1. First-person narrator voice: authoritative, intimate, and direct.
2. No headings or section markers: pure narration text with paragraph breaks only.
3. Hook in the first sentence: a sharp claim, question, contradiction, or concrete number that stops the scroll.
4. Shorts pacing: every 15-25 seconds should add a new turn, reveal, escalation, or "wait, it gets worse" moment.
5. Vary sentence length: short punchy sentences after longer setup lines.
6. Concrete details: use names, dates, places, numbers, and visible stakes. Avoid vague filler.
7. Emotional escalation: each section should raise the stakes.
8. Payoff at 75-85%: put the biggest revelation near the end, then close quickly.
9. Reflective close: final 10-15 seconds should land one memorable thought.
10. Do not include visual directions, captions, sound cues, brackets, markdown headings, or production notes.

## If Mode B (Viral DNA Available)
- Use the `hook_template` from Level 2 as the opening pattern.
- Follow the `arc_type` structure.
- Insert adapted retention phrases at similar intervals.
- Ensure every Level 3 psychological trigger is deployed at least once.
- Match the `pacing_words_per_section` distribution when it is compatible with a 90-second Short.

## Output
Save narration text to `outputs/<run_id>/script.md`.

The script must be:
- Pure narration
- Exactly within +/-10% of target word count
- Readable aloud in one continuous flow
- Written for a deep Gathos `pixxy` voice unless the run specifies another voice
