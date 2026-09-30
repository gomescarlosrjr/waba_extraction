# waba_extraction

Batch transcription of WhatsApp `.opus` audio files using the Groq API (Whisper large-v3).

> **Privacy:** audio files (`*.opus`) and transcripts (`transcricoes*.txt` / `transcripts*.txt`) are personal data and are **not** versioned (see `.gitignore`). This repository contains code only.

## Usage

1. Create a free account at https://console.groq.com and generate an API key.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Extract the WhatsApp `.opus` files into a folder (subfolders are scanned recursively).
4. Provide the API key in one of two ways (never hardcode it):
   - **Inline:**
     ```bash
     GROQ_API_KEY="your_key_here" python transcrever_audios.py /path/to/folder
     ```
   - **Via `.env`** (loaded automatically, git-ignored, stays local):
     ```bash
     echo 'GROQ_API_KEY=your_key_here' > .env
     python transcrever_audios.py .
     ```
5. The script writes a `transcricoes.txt` in the folder, with the date/time (parsed from the file name), the source folder, and the transcribed text.

## Cost

~US$ 0.05 for ~48 min of audio (often covered by Groq's free tier).
