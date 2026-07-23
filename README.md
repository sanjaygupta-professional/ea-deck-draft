# Narrated Deck — US Enrolled Agent @ Hi-Educare (DRAFT)

Self-presenting HTML slideshow: 22 slides from `US EA @Hi-Educare.pptx`, each narrated,
auto-advancing after each voice segment. Open `index.html` (or the Pages URL), press Start.

**Status: DRAFT.** Narration script (`narration.md`) is AI-drafted from slide content and
NOT yet approved by Haresh. Voice: Haresh Ratnagrahi instant clone v2 — source is 6.6 min of clean
solo speech extracted from his Vimeo lecture (diarization-verified, loudness-normalized;
settings: stability 0.5, similarity 0.85, style 0.15, eleven_multilingual_v2).

## Pipeline (to redo for any deck)

1. **Slides → PNG**: PowerPoint COM on Windows host:
   `$pres.Export("C:\...\slides_png", "PNG", 1920, 1080)` (see `export.ps1` pattern)
2. **Script**: draft per-slide narration from slide text (`narration.md`); keep every factual
   claim verbatim from the slides; get the speaker's approval before publishing.
3. **Audio**: ElevenLabs TTS per slide → `audio/slideNN.mp3`
   (model `eleven_multilingual_v2`, stability 0.55, similarity 0.75).
4. **Player**: `index.html` — static, no build, no dependencies.

## Swapping in Haresh's cloned voice

The ElevenLabs MCP `voice_clone` tool currently 400s (`invalid_labels` — server-side bug in
elevenlabs-mcp). Create the clone directly instead (uses your API key, never share it):

```bash
curl -s https://api.elevenlabs.io/v1/voices/add \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F name="Haresh Ratnagrahi draft clone" \
  -F files=@voice-sample.mp3
```

Returns a `voice_id`. Then regenerate the 22 clips with that voice_id (same texts from
`narration.md`) and replace `audio/slideNN.mp3`. Nothing else changes.

Better clone quality: ask Haresh for 2–3 minutes of clean audio (quiet room, phone close,
normal lecture voice) — the 40s 16 kHz WhatsApp note is the current quality ceiling.

## Files

- `index.html` — player (Start overlay, auto-advance, ← → keys, space = pause, DRAFT watermark)
- `slides/slide01..22.png` — exported slides
- `audio/slide01..22.mp3` — narration (~7.6 min total)
- `narration.md` — the script, per slide (DRAFT v1)
- `voice-sample.{ogg,mp3}` — Haresh's WhatsApp voice note (clone source; not published)
