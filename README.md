# waba_extraction

Transcrição em lote de áudios `.opus` do WhatsApp usando a API da Groq (Whisper large-v3).

> **Privacidade:** áudios (`*.opus`) e transcrições (`transcricoes*.txt`) são dados pessoais e **não** são versionados (veja `.gitignore`). Este repositório contém apenas o código.

## Uso

1. Crie uma conta gratuita em https://console.groq.com e gere uma API key.
2. Instale a dependência:
   ```bash
   pip install groq
   ```
3. Extraia os arquivos `.opus` do WhatsApp em uma pasta (subpastas são varridas recursivamente).
4. Rode passando a chave por variável de ambiente (nunca hardcode):
   ```bash
   GROQ_API_KEY="sua_chave_aqui" python transcrever_audios.py /caminho/para/pasta
   ```
5. O script gera um `transcricoes.txt` na pasta, com data/hora (extraída do nome do arquivo), pasta de origem e o texto transcrito.

## Custo

~R$ 0,20 para ~48 min de áudio (frequentemente coberto pelo tier gratuito da Groq).
