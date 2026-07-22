#!/usr/bin/env python3
"""Generate index.html for the narrated lecture from assets/slides + assets/audio.

Timing: slide N visible for [start, start + audio + GAP]; audio starts LEAD after
slide appears; soft fade-in + gentle Ken Burns per slide on the main timeline.
Rerun after any audio regeneration: python3 build-composition.py
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
GAP = 0.9   # silence after each clip before next slide
LEAD = 0.35  # slide appears this long before its narration starts
FADE = 0.45

slides = sorted((HERE / "assets/slides").glob("slide*.png"))
durs = []
for p in slides:
    a = HERE / "assets/audio" / (p.stem + ".mp3")
    d = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(a)]))
    durs.append(d)

# integer milliseconds throughout so clip end == next clip start exactly
starts_ms, t_ms = [], 0
segs_ms = []
for d in durs:
    seg = int(round((LEAD + d + GAP) * 1000))
    starts_ms.append(t_ms)
    segs_ms.append(seg)
    t_ms += seg
total = t_ms / 1000

clips, tweens = [], []
for i, (p, d) in enumerate(zip(slides, durs), 1):
    s, seg = starts_ms[i - 1] / 1000, segs_ms[i - 1] / 1000
    clips.append(
        f'      <section id="s{i:02d}" class="clip" data-start="{s:.3f}" data-duration="{seg:.3f}" data-track-index="1">\n'
        f'        <div id="w{i:02d}" class="wrap"><img src="assets/slides/{p.name}" alt="Slide {i}"></div>\n'
        f'      </section>')
    clips.append(
        f'      <audio id="a{i:02d}" src="assets/audio/{p.stem}.mp3" data-start="{s + LEAD:.3f}" '
        f'data-duration="{d:.3f}" data-track-index="10" data-volume="1"></audio>')
    tweens.append(f'      tl.fromTo("#w{i:02d}", {{opacity: 0}}, {{opacity: 1, duration: {FADE}, ease: "power2.out"}}, {s:.3f});')
    tweens.append(f'      tl.fromTo("#w{i:02d} img", {{scale: 1.0}}, {{scale: 1.035, duration: {seg:.3f}, ease: "none"}}, {s:.3f});')

html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>US Enrolled Agent — Hi-Educare (Narrated Lecture)</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      body {{ margin: 0; background: #141413; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #141413; }}
      #bgfill {{ position: absolute; inset: 0; background: #141413; }}
      .clip {{ position: absolute; inset: 0; }}
      .wrap {{ position: absolute; inset: 0; display: grid; place-items: center; opacity: 0; }}
      .wrap img {{ width: 1920px; height: 1080px; object-fit: contain; will-change: transform; }}
      #draft {{ position: absolute; top: 20px; right: 24px; background: rgba(20,20,19,.92); color: #d97757;
               font: 600 20px/1 system-ui, sans-serif; letter-spacing: .12em; padding: 8px 18px; border-radius: 6px; z-index: 50; }}
      #pbar {{ position: absolute; left: 0; bottom: 0; height: 6px; width: 100%; background: rgba(255,255,255,.12); z-index: 50; }}
      #pfill {{ height: 100%; width: 100%; background: #d97757; transform-origin: left center; transform: scaleX(0); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{total}">
      <div id="bgfill"></div>
{chr(10).join(clips)}
      <div id="draft">DRAFT — PENDING APPROVAL</div>
      <div id="pbar"><div id="pfill"></div></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tweens)}
      tl.fromTo("#pfill", {{scaleX: 0}}, {{scaleX: 1, duration: {total}, ease: "none"}}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(HERE / "index.html").write_text(html)
print(f"index.html written — 22 slides, total {total}s ({total/60:.1f} min)")
