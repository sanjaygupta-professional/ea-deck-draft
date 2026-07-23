#!/usr/bin/env python3
"""Create an ElevenLabs instant voice clone from an audio sample.

Usage: python3 clone-voice.py <key-file> <sample.mp3> [name]
Prints only the new voice_id. Key never printed.
"""
import json
import sys
import urllib.request
import uuid
from pathlib import Path


def main():
    key = Path(sys.argv[1]).read_text().strip().splitlines()[0].strip()
    sample = Path(sys.argv[2])
    name = sys.argv[3] if len(sys.argv) > 3 else "Haresh Ratnagrahi clone v2 (lecture)"

    boundary = uuid.uuid4().hex
    parts = []
    for field, value in [("name", name), ("remove_background_noise", "true")]:
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{field}\"\r\n\r\n{value}\r\n".encode())
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; filename=\"{sample.name}\"\r\n"
        f"Content-Type: audio/mpeg\r\n\r\n".encode() + sample.read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)

    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/voices/add",
        data=body,
        headers={"xi-api-key": key,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")
    print(d["voice_id"])


if __name__ == "__main__":
    main()
