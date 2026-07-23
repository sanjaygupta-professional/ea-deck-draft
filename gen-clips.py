#!/usr/bin/env python3
"""Regenerate all 22 narration clips with a given ElevenLabs voice.

Usage: python3 gen-clips.py <key-file> [voice_id] [--only 1,5,7]
Key file = plain text file containing only the ElevenLabs API key.
Texts come from narration.md (## Slide N sections). Output: audio/slideNN.mp3
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
VOICE_ID = "nlGgswSMHWB9KTixQBt5"  # Haresh clone v2 (6.6 min lecture sample)
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.5, "similarity_boost": 0.85, "style": 0.15, "use_speaker_boost": True}


def parse_narration():
    text = (HERE / "narration.md").read_text(encoding="utf8")
    slides = {}
    for m in re.finditer(r"^## Slide (\d+)\n(.*?)(?=^## Slide |\Z)", text, re.M | re.S):
        slides[int(m.group(1))] = m.group(2).strip()
    return slides


def tts(key, voice_id, text, out_path):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS}).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        out_path.write_bytes(r.read())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--only")]
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only"):
            only = {int(x) for x in a.split("=", 1)[1].split(",")} if "=" in a else None
    key = Path(args[0]).read_text().strip().splitlines()[0].strip()
    voice_id = args[1] if len(args) > 1 else VOICE_ID
    slides = parse_narration()
    assert len(slides) == 22, f"expected 22 slides in narration.md, got {len(slides)}"
    (HERE / "audio").mkdir(exist_ok=True)
    for n in sorted(slides):
        if only and n not in only:
            continue
        out = HERE / "audio" / f"slide{n:02d}.mp3"
        for attempt in range(3):
            try:
                tts(key, voice_id, slides[n], out)
                print(f"slide{n:02d}.mp3 OK {out.stat().st_size}b")
                break
            except Exception as e:  # ponytail: 3 tries then die loud
                print(f"slide{n:02d} attempt {attempt+1} failed: {e}")
                time.sleep(3)
        else:
            sys.exit(f"giving up on slide {n}")
    print("DONE")


if __name__ == "__main__":
    main()
