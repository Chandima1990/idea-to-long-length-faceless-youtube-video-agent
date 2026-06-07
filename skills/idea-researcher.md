# Idea Researcher

Triggered **only** when the user explicitly asks for video ideas, research, or topic suggestions.
Do NOT run this unless asked. If the user provides a topic directly, skip to the script stage.

---

## Context Block — Read This First

Before doing any research, confirm you have the following. If anything is missing, ask the user
for it explicitly rather than guessing.

**Required — ask if not provided:**
1. **Channel name** — which channel is this for? (e.g. rich_mantra, wonder_lab, amma_sindu, eternal_wisdom)

   ⚠️ **IMPORTANT:** These are private internal project names, NOT public YouTube channels.
   Do NOT search the internet for "rich_mantra" or "wonder_lab" — you will find nothing useful.
   The channel definition lives in a local JSON file that the user must paste for you.

2. **Channel JSON** — the full contents of `channels/<channel_name>.json`. If you don't have it,
   ask the user exactly this: *"Can you paste the contents of your channels/<channel_name>.json
   file? It defines the niche, audience, tone, and title style for this channel."*
   The JSON contains: niche, target audience, tone, title style examples, and host personality.

3. **Recent topics already covered** — to avoid repeating. Ask: *"Can you give me a quick list of
   your last 5-10 video topics so I don't suggest something you've already made?"*

**Optional — ask only if the user mentioned a direction:**
4. **User hints** — any angle, niche sub-topic, or trend the user wants to explore
   (e.g. "something about ETFs", "a trending news hook", "competitor angle on X").

**If you have web search:** proceed to the Research Process below.
**If you don't have web search:** tell the user upfront — *"I don't have live web access, so I'll
generate ideas based on the channel context and my training knowledge rather than live research.
The ideas will be solid but won't reflect breaking trends from the last few weeks."* Then proceed.

---

## Input
- `channels/<CHANNEL>.json` — read first. Channel niche, tone, audience, and title style define
  what a good idea looks like for this channel.
- Optional: user hints ("something about ETFs", "trending this week", "competitor angle")

## Goal
Surface 4-6 genuinely viral-worthy video ideas the channel has not recently covered, backed by
evidence that the audience is actively searching for or discussing the topic right now.

---

## Research Process

### 1. Understand the channel's content landscape
Read the active `channels/<CHANNEL>.json`. Extract:
- `channel.niche` — the topic space
- `channel.target_audience` — who watches and why
- `youtube_metadata.title_style.examples` — what winning titles look like
- Recent runs in `outputs/` — scan folder names to avoid repeating recent topics

### 2. Research competitor channels
Use WebSearch to find the top 5-8 YouTube channels in the same niche.
Search: `"[niche] YouTube channel 2025"` and `"best [niche] YouTube channels"`

For each major competitor, search:
`site:youtube.com "[channel name]"` or look for their most-viewed recent videos.

Note: topics they cover frequently (saturated), topics with high views but old upload dates
(ripe for a v2), and visible gaps (questions the audience asks in comments that nobody has answered well).

**Known competitors by channel:**
- `rich_mantra` → Graham Stephan, Andrei Jikh, Mark Tilbury, Humphrey Yang, Nischa, James Shack
- `wonder_lab` → Kurzgesagt, Veritasium, SciShow, MinuteEarth, TED-Ed, Wendover Productions
- `amma_sindu` → Sri Lankan music YouTube channels, Sinhala devotional/folk channels
- `eternal_wisdom` → einzelgänger, Ryan Holiday (Daily Stoic), Pursuit of Wonder, Einzelgänger

### 3. Mine audience questions and pain points
Search Reddit, Quora, and forums where the target audience hangs out.

**Search queries by channel:**
- `rich_mantra`: search `site:reddit.com/r/personalfinance`, `site:reddit.com/r/investing`,
  `site:reddit.com/r/financialindependence` for top posts this month. Look for recurring
  questions, frustrations with financial products, things people "wish they knew earlier."
- `wonder_lab`: search `site:reddit.com/r/todayilearned`, `site:reddit.com/r/science`,
  `site:reddit.com/r/askscience` for "TIL" posts with high upvotes and surprising facts
  that haven't been turned into a viral video yet.
- `amma_sindu`: search Sri Lankan Facebook groups, Sinhala music forums, Sinhala lyrics sites
  for song themes that resonate emotionally with diaspora audiences.
- `eternal_wisdom`: search `site:reddit.com/r/stoicism`, `site:reddit.com/r/philosophy`,
  `site:reddit.com/r/psychology` for questions about managing emotions, decision-making,
  and life regrets that recur often.

Use: `WebSearch("[subreddit or site] [topic] questions")`

### 4. Check trending topics and news hooks
Search Google News or YouTube Trending for current events that intersect the channel niche.
A trending hook makes any quality level go further (Trends Bias).

- `rich_mantra`: search recent news about Fed rate decisions, market corrections, retirement
  rule changes, SECURE Act updates, new ETF launches, inflation data.
- `wonder_lab`: search recent science journal highlights, NASA announcements, nature
  discoveries, biology/physics breakthroughs in plain language.
- `eternal_wisdom`: search cultural moments — a famous person's public failure, a viral
  debate about life choices, a book making waves.

Use: `WebSearch("[niche] news 2026")` and `WebSearch("trending [niche] YouTube 2026")`

### 5. Identify content gaps
Cross-reference what competitors cover vs. what the audience is asking.
A gap = audience asking X + no good recent video answering X on a channel like this one.

Also flag:
- Topics where the top result is 2+ years old → ripe for a "v2" or "updated" angle
- Topics where the top video has poor retention signals (short, vague title, low comment engagement)
  → this channel can do it better

---

## Idea Synthesis

From your research, generate **4-6 video ideas**. For each, write:

```
IDEA [N]: [Working title following channel title_style.format]

HOOK: One sentence — the uncomfortable truth, shocking number, or curiosity gap that stops the scroll.

PLOT: 2-3 sentences. The hidden mechanism this video exposes, the stakes (concrete number or outcome),
and the simple action or insight the viewer walks away with.

VIRAL TRIGGER: Which psychological lever this pulls (confirmation bias / hidden knowledge /
injustice framing / shocking number / fear of missing out / status validation).

EVIDENCE: 1-2 specific signals from research — a Reddit thread, a competitor gap, a news hook,
or a search volume indicator — that proves the audience wants this now.

DIFFICULTY: Easy / Medium / Hard — how much factual research the script will need.
```

---

## Output

Present the ideas directly in the conversation as a numbered list.
Do NOT save to a file unless the user asks.

After presenting, ask: **"Which of these do you want to develop? Or should I refine any of them?"**

Once the user picks one, proceed to Step 1 (Create Run) in AGENT_GUIDE.md with that topic,
carrying the HOOK and PLOT forward as inputs to the script writer.
