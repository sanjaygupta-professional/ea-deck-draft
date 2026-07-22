# BRIEF

workflow: general-video
flow: standard

## Message

Full narrated lecture video: "US Enrolled Agent @ Hi-Educare" — 22 slides, each shown while its narration clip (Haresh voice clone) plays, sequential, one continuous MP4.

## Inputs

- Slides: `~/haresh-lecture/slides/slide01..22.png` (1920×1080 PNG, exported from PowerPoint)
- Narration: `~/haresh-lecture/audio/slide01..22.mp3` (Haresh clone, ~6.6 min total)
- Slide N pairs with audio N; slide holds for its clip duration + small gap.

## Audience / destination

Prospective EA students in India; shared by WhatsApp/YouTube/LMS. 16:9, 1920×1080, 30fps.

## Style

- Match deck: professional educational, clean. Slides are the visual — full-bleed, no reinvention.
- Subtle polish only: gentle Ken Burns (slow scale 1.0→1.03 per slide), quick crossfade between slides, thin progress bar.
- DRAFT watermark top-right (script not yet approved by Haresh) — same guard as the HTML deck.
- No music bed (narration only) unless trivially cheap.

## Constraints

- One best version, no variations.
- Total length = sum of clips + gaps (~7 min).
- Output: `lecture.mp4`, H.264.
