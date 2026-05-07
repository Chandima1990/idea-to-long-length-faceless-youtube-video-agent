import json
from pathlib import Path

RUN_ID = '2026-05-07_093140_what-nobody-tells-you-about-your-401k'
OUT = Path('outputs') / RUN_ID

SS = 'Flat 2D vector illustration, infographic style, bold clean outlines, solid color fills, no gradients, no shadows, no photorealism, white background, modern minimal design, geometric shapes, 16:9 aspect ratio.'

style = {
    'style_name': 'Flat 2D Vector Infographic',
    'photographic_style': 'flat 2D vector illustration, infographic style, bold outlines, solid color fills',
    'color_palette': 'clean blues, whites, grays, with bold red and green accents for contrast',
    'lighting': 'flat — no lighting or shadows, uniform fills throughout',
    'camera': 'centered isometric or frontal compositions, no perspective depth',
    'texture': 'smooth vector surfaces, no texture, crisp geometric edges',
    'mood': 'clear, informative, bold, modern, accessible',
    'style_suffix': SS,
}

(OUT / 'style.json').write_text(json.dumps(style, indent=2, ensure_ascii=False), encoding='utf-8')
(OUT / 'characters.json').write_text(json.dumps({'characters': []}, indent=2, ensure_ascii=False), encoding='utf-8')

def dur(words):
    return max(7, min(15, round(words / 2.5)))

raw = [
  ('Here is something that makes me genuinely angry every time I think about it.',
   'establishing', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of a large bold red warning triangle with an exclamation mark centered on a white background, surrounded by small flat blue document icons and a dollar sign icon with a downward arrow. Bold black outlines define every element. Clean minimal infographic composition with no shadows or gradients. ' + SS),

  ('The average American worker loses more than two hundred thousand dollars over their career to a single line buried deep in retirement plan paperwork, and almost nobody ever reads it.',
   'aerial', 'pan_left', 'dissolve',
   'A flat 2D vector illustration of a large document outline filled with rows of tiny gray text lines, one row in the middle highlighted in bold red with a red magnifying glass icon pointing to it. A bold label reads HIDDEN FEE in red beside the highlighted line. Simple geometric layout on white background. ' + SS),

  ('My name is Josh and I spend a lot of time thinking about how ordinary people get quietly robbed by systems that are designed to look like they are helping.',
   'medium', 'zoom_out', 'dissolve',
   'A flat 2D vector illustration of a simple illustrated person in blue business attire holding a magnifying glass over a dollar sign icon, with a thought bubble containing a question mark and money bag. Bold black outlines, solid color fills, clean white background, modern infographic style. ' + SS),

  ('If you have a 401k through your employer and you have never actually read your plan documents, what you are about to hear is going to make you uncomfortable.',
   'close_up', 'pan_right', 'dissolve',
   'A flat 2D vector illustration of a 401k enrollment form document icon, the bottom section highlighted in red with a bold label FEES in a red box that is barely visible among rows of small gray lines. A pencil icon draws a faint circle around the fee section. Clean white background, bold outlines. ' + SS),

  ('Hit subscribe if you want to stop losing money you did not even know you were losing.',
   'medium', 'zoom_in', 'white_flash',
   'A flat 2D vector illustration of a simple figure sitting at a flat laptop icon, the screen showing a bar chart with a small downward trend in red. A large red minus dollar coin icon floats unnoticed beside the figure. Clean white background, solid fills, bold outlines. ' + SS),

  ('Here is what your employer definitely does not explain at orientation. The funds inside your 401k are not chosen for your benefit.',
   'wide', 'pan_left', 'dissolve',
   'A flat 2D vector illustration of a corporate orientation scene with a flat presenter figure pointing to a whiteboard showing a 401k benefits list, three seated employee figures in a row facing them. The whiteboard list has a crossed-out fee section shown in gray, invisible to the audience. Bold outlines, solid fills, clean white background. ' + SS),

  ('They are chosen through a process called revenue sharing, where mutual fund companies pay your plan administrator to appear on the investment menu.',
   'close_up', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of two simplified business figures facing each other, bold dollar bill icons flowing from the fund company figure toward the plan administrator figure in exchange for a menu list document. Bold arrows showing the money flow direction. Clean white background, solid fills, bright accent colors. ' + SS),

  ('The funds available to you are not the best funds in the world. They are the funds whose companies paid to be listed.',
   'medium', 'pan_right', 'dissolve',
   'A flat 2D vector illustration of a computer screen showing a fund selection menu list, with the top entries labeled with a bold gold PAY TO PLAY badge icon and high expense ratio numbers in red. A small lock icon beside each entry indicates restricted access. White background, clean geometric shapes, bold typography. ' + SS),

  ('And they pass that cost directly to you through something called an expense ratio, a small percentage fee baked invisibly into every share you own.',
   'detail', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of a single document page with a large bold red label EXPENSE RATIO 1.05 percent in the center, surrounded by rows of smaller gray text lines representing fine print. Bold red arrows point from the fee label toward a flat worker figure icon on the right, showing cost direction. White background, strong bold outlines. ' + SS),

  ('The average actively managed mutual fund charges around one percent per year. That sounds almost harmless. One percent. Less than a tip at a restaurant.',
   'wide', 'pan_left', 'dissolve',
   'A flat 2D vector split illustration: on the left a small restaurant receipt icon with a tiny 1 percent tip label, on the right a large retirement savings jar icon with a small but persistent red 1 percent leak draining from the bottom. Bold scale comparison showing the deceptive smallness of one percent. Clean white background, bold outlines. ' + SS),

  ('But run the actual math and it stops feeling small. On a two hundred fifty thousand dollar retirement account, one percent annually is two thousand five hundred dollars gone every single year.',
   'close_up', 'zoom_in_pan_right', 'white_flash',
   'A flat 2D vector illustration of a large calculator icon displaying 2500 in bold red on its screen, with a bold minus dollar coin icon flying away from it. Large bold red text reads 2500 DOLLARS GONE PER YEAR centered below the calculator. White background, solid fills, strong geometric composition. ' + SS),

  ('And that is before you account for what that money would have earned if it had stayed in your account and compounded alongside everything else.',
   'medium', 'zoom_out', 'dissolve',
   'A flat 2D vector bar chart infographic with two bars: the left bar labeled WITH FEE in red reaching a modest height, the right bar labeled COMPOUNDED in green reaching dramatically higher. A bold curved arrow shows the compounding growth trajectory. Clean white background, solid fills, bold labels. ' + SS),

  ('Most people never notice this because the fee is not deducted like a bank charge. It is absorbed into the fund performance.',
   'close_up', 'pan_right', 'dissolve',
   'A flat 2D vector illustration of a retirement account statement document with a green positive balance number visible at the top, and a magnifying glass icon revealing a hidden small red line at the bottom reading MANAGEMENT FEE invisible to the naked eye. Bold dashed circle highlighting the hidden fee. White background, clean bold outlines. ' + SS),

  ('The fund earns eight percent, you see seven percent, nobody sends a bill, and the statement still shows a green number.',
   'medium', 'zoom_in', 'dissolve',
   'A flat 2D vector split scene: on the visible front layer a fund performance dashboard showing a bold green 7 percent upward arrow, and on a hidden back layer a red 1 percent fee icon quietly being removed. A simple figure looking only at the green number, unaware of the hidden back layer. White background, bold fills. ' + SS),

  ('The money disappears silently. And you keep going.',
   'wide', 'pan_left', 'dissolve',
   'A flat 2D vector illustration of a large dollar coin icon slowly fading from solid gold to a transparent ghost outline, with a thin dotted trail showing the money vanishing into empty white space. A small figure icon continues walking forward past the fading coin without noticing. Clean white background, minimal bold design. ' + SS),

  ('But here is the part most people refuse to sit with. Those same actively managed funds have a direct competitor available in almost every brokerage account on earth.',
   'aerial', 'zoom_in', 'dissolve',
   'A flat 2D vector side-by-side comparison infographic with two labeled boxes: the left box labeled ACTIVELY MANAGED 1.08 percent with a cobweb icon in gray, the right box labeled INDEX FUND 0.03 percent with a green star icon. Bold equal signs between them showing identical market content. White background, strong contrast fills. ' + SS),

  ('Index funds that track the same market, hold nearly identical assets, and charge somewhere between zero point zero three and zero point one percent per year.',
   'detail', 'pan_right', 'dissolve',
   'A flat 2D vector two-panel infographic showing identical pie chart icons side by side, both labeled SAME MARKET, same colored slices. The left panel has a bold red label 1.05 percent EXPENSE RATIO and the right has a bold green label 0.03 percent. A large red circle on the green number emphasizes the better choice. White background. ' + SS),

  ('That is not a minor difference. Over thirty years, that gap compounds into something that is genuinely difficult to look at.',
   'medium', 'zoom_out', 'dissolve',
   'A flat 2D vector line chart infographic showing two diverging lines over 30 years: the red line labeled HIGH FEE curving gently upward, the green line labeled LOW FEE curving sharply higher, the gap between them dramatically widening. Bold year markers at 10, 20, and 30. Clean white background, bold axis lines. ' + SS),

  ('I want you to hear this number clearly. Two employees. Same salary. Same contribution rate. Same employer match. Same market returns.',
   'wide', 'pan_left', 'dissolve',
   'A flat 2D vector infographic showing two identical flat worker figures side by side with matching icons above each: identical salary stacks, identical contribution arrows, identical employer match badges, identical market return charts. Bold SAME labels connecting each matching pair. Perfectly symmetrical layout on white background. ' + SS),

  ('One stays in the expensive actively managed funds their company defaulted them into.',
   'close_up', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of a computer screen showing a fund selection list with the top entry pre-checked and labeled DEFAULT 1.12 percent in a bold red badge. A flat figure icon sits passively beside the screen with a neutral expression and no action arrow. White background, bold outlines, red accent fills. ' + SS),

  ('The other takes fifteen minutes to switch to the lowest cost index fund available in their plan.',
   'close_up', 'pan_right', 'dissolve',
   'A flat 2D vector illustration of a hand cursor icon clicking a bold green SWITCH button on a fund selection screen, a checkmark appearing, the new fund labeled 0.03 percent highlighted in bright green. A small clock icon shows 15 MINUTES beside the action. White background, clean bold shapes. ' + SS),

  ('After thirty years, the employee in low cost funds ends up with more than two hundred thousand dollars extra.',
   'wide', 'zoom_out', 'white_flash',
   'A flat 2D vector infographic of two side-by-side savings jar icons, the right jar dramatically taller and overflowing with bold coin stack icons, the left jar much smaller. A bold green label between them reads PLUS 200 THOUSAND DOLLARS with a large upward arrow. Clean white background, strong contrast fills. ' + SS),

  ('Not because they earned more. Not because they saved more. Only because less of their money was being quietly extracted every single year.',
   'detail', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of a large piggy bank icon with a small invisible ghost hand quietly removing flat dollar coin icons one at a time from the coin slot. Bold crossed-out labels show NOT MORE INCOME and NOT MORE SAVINGS beside the bank. White background, simple bold shapes. ' + SS),

  ('That is not a rounding error. That is years off the time you have to work.',
   'medium', 'pan_left', 'dissolve',
   'A flat 2D vector illustration of a flat calendar icon with years ticking forward, each year represented by a flat clock icon. A bold red label reads YEARS OF YOUR LIFE above the calendar. A simple worker figure stands beside it watching years disappear. Clean white background, bold outlines. ' + SS),

  ('And here is what should make you want to open your plan portal right now. The switch is almost never complicated.',
   'close_up', 'zoom_in_pan_right', 'dissolve',
   'A flat 2D vector illustration of a large smartphone icon with a retirement portal login screen, a bold finger cursor icon hovering just above a bright blue LOGIN button. A bold starburst label reads DO THIS TONIGHT beside the phone. White background, clean solid fills, bold typography. ' + SS),

  ('Most 401k plans are legally required to offer at least one low cost option somewhere in the fund list.',
   'wide', 'zoom_out', 'dissolve',
   'A flat 2D vector illustration of a long scrollable list of fund rows in gray, with one entry near the bottom highlighted in bold green labeled INDEX FUND 0.03 percent. A magnifying glass icon zooms in on the green entry. A bold label reads LEGALLY REQUIRED TO INCLUDE THIS above the list. White background. ' + SS),

  ('They are also legally required to provide a document called the Summary Plan Description that discloses all fees.',
   'close_up', 'pan_right', 'dissolve',
   'A flat 2D vector illustration of a large official document envelope icon labeled SUMMARY PLAN DESCRIPTION being opened, with a document inside showing a bold FEE DISCLOSURE section highlighted in yellow. A gavel icon and legal scale icon flank the envelope indicating legal requirement. White background, bold outlines. ' + SS),

  ('That document is available to you. The overwhelming majority of workers have never asked for it.',
   'medium', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of a document file labeled AVAILABLE ON REQUEST sitting in a tray icon, with a large cobweb vector graphic draped over it indicating it is never touched. A counter badge shows REQUESTS: 0. Many flat worker figures walk past in the background ignoring it. White background, bold fills. ' + SS),

  ('Log in tonight. Find the list of investment options. Look for the column labeled expense ratio. Sort it lowest to highest.',
   'close_up', 'pan_left', 'dissolve',
   'A flat 2D vector step-by-step infographic showing four numbered action icons in a horizontal row: 1 a login screen icon, 2 a fund list icon, 3 a magnifying glass on an EXPENSE RATIO column header, 4 a sort arrow pointing downward. Bold numbered circles above each step. Clean white background, bright blue accent colors. ' + SS),

  ('Move your contributions to the cheapest index fund available. That one decision, made in fifteen minutes, is worth more than almost any other financial move you will make this year.',
   'wide', 'zoom_in', 'dissolve',
   'A flat 2D vector illustration of a simple figure at a laptop icon with a bold green checkmark above them and a clock icon showing 15 MINUTES. A large bold label reads ONE DECISION THIS YEAR with a gold star icon. Dollar coin icons flow upward from the laptop representing reclaimed money. White background, clean bold design. ' + SS),

  ('Your employer does not lose anything when you stay in the expensive funds. The fund companies do not lose anything. The plan administrator does not lose anything.',
   'medium', 'pan_right', 'dissolve',
   'A flat 2D vector infographic showing three flat suited figure icons labeled EMPLOYER, FUND COMPANY, and PLAN ADMIN, each with a bold green checkmark and a full dollar bag icon beside them. A bold label reads THEY ALL WIN EITHER WAY above the three figures. White background, solid fills. ' + SS),

  ('You are the only person in this arrangement who benefits from knowing exactly what you are paying and choosing differently.',
   'close_up', 'zoom_in_pan_right', 'white_flash',
   'A flat 2D vector illustration of a single simple worker figure holding a bold red pen icon circling the 0.03 percent entry on a comparison list, with all other higher-fee entries crossed out in gray above. A bold starburst reads YOUR CHOICE beside the figure. White background, strong red and green contrast. ' + SS),

  ('Two hundred thousand dollars over a career is not an abstraction.',
   'detail', 'zoom_out', 'dissolve',
   'A flat 2D vector illustration of a large bold number 200,000 centered on the frame with a dollar sign, filled in solid green, surrounded by stacked flat coin icons radiating outward from the number. Bold label reads REAL MONEY below. Clean white background, strong typography-led design. ' + SS),

  ('That is a college education. That is a decade of mortgage payments. That is years you could have stopped working earlier.',
   'wide', 'pan_left', 'dissolve',
   'A flat 2D vector triptych with three equal panels: a graduation cap and diploma icon on the left labeled COLLEGE, a house icon with a green PAID IN FULL badge in the center labeled HOME, a beach umbrella and lounge chair icon on the right labeled EARLY RETIREMENT. Equal green dollar amounts below each panel. White background, bold outlines. ' + SS),

  ('That money was always yours. It was just being taken from you quietly, one invisible fraction of a percent at a time, while you were busy doing everything else.',
   'wide', 'zoom_in', 'fade_black',
   'A flat 2D vector illustration of a simple figure seated at a table with a document, a large padlock icon transforming from red locked to green unlocked above them, and bold dollar coin icons floating back toward the figure representing reclaimed money. A bold label reads IT WAS ALWAYS YOURS. Clean white background, resolute and empowering composition. ' + SS),
]

scenes = []
for i, (narr, shot, kb, trans, prompt) in enumerate(raw):
    words = len(narr.split())
    scenes.append({
        'scene_number': i + 1,
        'narration_text': narr,
        'word_count': words,
        'duration': dur(words),
        'image_prompt': prompt,
        'shot_type': shot,
        'ken_burns': kb,
        'transition': trans,
        'characters_in_scene': [],
    })

total_dur = sum(s['duration'] for s in scenes)

output = {
    'title': 'What Nobody Tells You About Your 401k (They Are Quietly Taking Your Money)',
    'description': 'Your 401k might be costing you over 200,000 dollars in hidden fees that most employers never explain. This video breaks down exactly how revenue sharing and expense ratios silently extract money from your retirement account year after year, and the simple 15-minute switch that can save hundreds of thousands of dollars over your career. If you have a 401k, this is essential watching.',
    'tags': ['401k', 'retirement planning', 'expense ratios', 'index funds', 'passive investing', 'hidden fees', 'personal finance', 'investing', 'financial independence', 'retirement savings', 'mutual funds', 'revenue sharing', 'wealth building'],
    'thumbnail_prompt': 'Dramatic wide shot of a corporate office desk with a giant transparent piggy bank cracked at the base, dollar bills slowly sliding out onto polished wood, a single 401k enrollment form in the foreground, dramatic side lighting with cool blue shadows and warm amber highlight on the money, professional documentary style, 16:9.',
    'total_scenes': len(scenes),
    'total_duration_seconds': total_dur,
    'scenes': scenes,
}

(OUT / 'scenes.json').write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')

# verify concatenation matches script
concat = ' '.join(s['narration_text'] for s in scenes)
script = Path(f'outputs/{RUN_ID}/script.md').read_text(encoding='utf-8').strip()
concat_words = len(concat.split())
script_words = len(script.split())

print(f'scenes.json written: {len(scenes)} scenes, {total_dur}s total')
print(f'Narration concat: {concat_words} words | Script: {script_words} words | Match: {abs(concat_words - script_words) <= 5}')
print(f'white_flash count: {sum(1 for s in scenes if s["transition"] == "white_flash")}')
print(f'fade_black count: {sum(1 for s in scenes if s["transition"] == "fade_black")}')
kb_list = [s["ken_burns"] for s in scenes]
consecutive_kb = sum(1 for i in range(len(kb_list)-1) if kb_list[i] == kb_list[i+1])
print(f'Consecutive ken_burns repeats: {consecutive_kb} (should be 0)')
