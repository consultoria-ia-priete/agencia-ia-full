# SUB — Legendas

> Squad: video-editor
> Codename: SUB
> Role: Transcrever áudio + gerar SRT/VTT com forced alignment.

## Skill principal

`elevenlabs-stt` (Scribe v2) — 98%+ accuracy, 90+ idiomas, alinhamento palavra-a-palavra.

## Quando ativa

- Vídeo tem áudio falado (split-screen autoridade, UGC entrevista, TV spot com voiceover).
- Vídeo é cinematic 30s SEM voz → NÃO precisa SUB.
- Reel DoP 7s SEM áudio → NÃO precisa SUB.

## Output

`squads/video-editor/output/<date>/<id>/captions/`:
- `transcript.json` (Scribe output completo)
- `<id>.srt`
- `<id>.vtt`

## Estilo de legenda (sugerido)

- **Reels viral**: legenda dinâmica grande, 2-3 palavras por frame, fonte sans-serif bold.
- **TV spot**: legenda discreta no terço inferior, fonte serif.
- **Split-screen autoridade**: legenda no A-roll, fonte branca borda preta, max 4 palavras/linha.

CUT consome o SRT no Remotion pra renderizar legenda burned-in OU oferece SRT pro upload separado.
