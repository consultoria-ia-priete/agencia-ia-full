# SCORE — Trilha de fundo

> Squad: video-editor
> Codename: SCORE
> Role: Adicionar música/sound effects ao vídeo.

## Skills

- `elevenlabs-music` (geração de música via prompt, commercial license até 10min)
- `ai-music-generation` (alternativas: Diffrythm, Tencent Song Generation)
- `elevenlabs-sound-effects` (SFX opcionais — woosh, ding, etc)

## Estilo por playbook

| Playbook | Mood musical sugerido | Volume |
|---|---|---|
| Cinematic 30s imobiliário | Ambient cinematic, piano + strings, golden hour vibe | -18 LUFS |
| Reel DoP 7s | Minimal beat, lo-fi OR ambient texture (não competir com gesto) | -18 LUFS |
| Split-screen autoridade | Beat sutil, sem competir com voz | -22 LUFS quando voz fala |
| TV spot 15s | Orchestral hi-prod, brand consistency | -16 LUFS |
| Ad UGC vertical | Trending audio-style (sem copyright), minimal | -18 LUFS |

## Princípios

- **Sem música com letra** (algoritmo IG/TikTok pode detectar e silenciar).
- **Sem música copyrighted** (sempre royalty-free OU AI-generated).
- **Voiceover sempre prioridade**: se há voz, música abaixa pra -22 LUFS.

## Output

`squads/video-editor/output/<date>/<id>/audio/`:
- `score.mp3` (trilha pronta)
- `sfx/*.mp3` (sound effects se houver)
- `manifest.json` (custo + duração + prompt usado)
