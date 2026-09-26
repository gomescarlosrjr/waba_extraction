#!/usr/bin/env python3
"""
Transcreve em lote todos os áudios .opus do WhatsApp usando a API da Groq (Whisper large-v3).
Custo aproximado: menos de R$ 0,20 para os ~48 minutos de áudio deste caso
(muitas vezes coberto pelo tier gratuito da Groq).

COMO USAR:
1. Crie uma conta gratuita em https://console.groq.com e gere uma API key.
2. pip install groq
3. Extraia os 4 arquivos .zip do WhatsApp em pastas separadas (ex.: eduardo_carlos, studio_carlos, etc).
4. Rode:  GROQ_API_KEY="sua_chave_aqui" python transcrever_audios.py /caminho/para/pasta/com/zips/extraidos
5. O script cria um arquivo transcricoes.txt com data/hora (extraída do nome do arquivo), pasta de origem e o texto transcrito.
"""

import os
import sys
import glob
import re
from groq import Groq

def main():
    if len(sys.argv) < 2:
        print("Uso: python transcrever_audios.py /caminho/para/pasta/raiz")
        sys.exit(1)

    root = sys.argv[1]
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Defina a variável de ambiente GROQ_API_KEY antes de rodar.")
        sys.exit(1)

    client = Groq(api_key=api_key)

    # Encontra todos os .opus em qualquer subpasta
    audio_files = sorted(glob.glob(os.path.join(root, "**", "*.opus"), recursive=True))
    print(f"Encontrados {len(audio_files)} arquivos de áudio.")

    results = []
    for i, path in enumerate(audio_files, 1):
        fname = os.path.basename(path)
        pasta = os.path.basename(os.path.dirname(path))
        # tenta extrair data/hora do nome, ex: 00000005-AUDIO-2020-11-12-16-45-03.opus
        m = re.search(r"AUDIO-(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", fname)
        timestamp = m.group(1) if m else "?"

        print(f"[{i}/{len(audio_files)}] Transcrevendo {fname} ...")
        try:
            with open(path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    file=(fname, f.read()),
                    model="whisper-large-v3",
                    language="pt",
                    response_format="text",
                )
            texto = str(transcript).strip()
        except Exception as e:
            texto = f"[ERRO ao transcrever: {e}]"

        results.append(f"{pasta} | {timestamp} | {fname}\n{texto}\n")

    out_path = os.path.join(root, "transcricoes.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n---\n".join(results))

    print(f"\nPronto! Transcrições salvas em: {out_path}")

if __name__ == "__main__":
    main()
