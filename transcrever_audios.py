#!/usr/bin/env python3
"""
Batch-transcribe all WhatsApp .opus audio files using the Groq API (Whisper large-v3).
Approximate cost: under US$ 0.05 for the ~48 minutes of audio in this case
(often covered by Groq's free tier).

HOW TO USE:
1. Create a free account at https://console.groq.com and generate an API key.
2. pip install groq
3. Extract the WhatsApp .opus files into folders (e.g. one folder per conversation).
4. Run:  GROQ_API_KEY="your_key_here" python transcrever_audios.py /path/to/root/folder
5. The script writes a transcricoes.txt file with the date/time (parsed from the
   file name), the source folder, and the transcribed text.
"""

import os
import sys
import glob
import re
from groq import Groq

def main():
    if len(sys.argv) < 2:
        print("Usage: python transcrever_audios.py /path/to/root/folder")
        sys.exit(1)

    root = sys.argv[1]
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Set the GROQ_API_KEY environment variable before running.")
        sys.exit(1)

    client = Groq(api_key=api_key)

    # Find every .opus file in any subfolder
    audio_files = sorted(glob.glob(os.path.join(root, "**", "*.opus"), recursive=True))
    print(f"Found {len(audio_files)} audio files.")

    results = []
    for i, path in enumerate(audio_files, 1):
        fname = os.path.basename(path)
        folder = os.path.basename(os.path.dirname(path))
        # Try to parse date/time from the name, e.g. 00000005-AUDIO-2020-11-12-16-45-03.opus
        m = re.search(r"AUDIO-(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", fname)
        timestamp = m.group(1) if m else "?"

        print(f"[{i}/{len(audio_files)}] Transcribing {fname} ...")
        try:
            with open(path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    file=(fname, f.read()),
                    model="whisper-large-v3",
                    language="pt",
                    response_format="text",
                )
            text = str(transcript).strip()
        except Exception as e:
            text = f"[ERROR while transcribing: {e}]"

        results.append(f"{folder} | {timestamp} | {fname}\n{text}\n")

    out_path = os.path.join(root, "transcricoes.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n---\n".join(results))

    print(f"\nDone! Transcripts saved to: {out_path}")

if __name__ == "__main__":
    main()
