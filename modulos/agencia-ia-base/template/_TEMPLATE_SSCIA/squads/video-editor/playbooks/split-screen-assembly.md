# Playbook — Split-screen assembly (Grupo B' autoridade)

Compor A-roll + B-roll em vídeo split 9:16 vertical.

## Inputs

- `squads/viral-reels-seo/output/<date>/<reel-id>/split-screen/script.md` (roteiro)
- `squads/viral-reels-seo/output/<date>/<reel-id>/split-screen/a-roll/*.mp4` (cliente falando)
- `squads/viral-reels-seo/output/<date>/<reel-id>/split-screen/b-roll/*.{mp4,png}` (assets)

## Composição

Remotion composition 1080×1920 (9:16):
- Top half (1080×960): A-roll talking-head do cliente
- Bottom half (1080×960): B-roll sequencial sincronizado com script

## Steps adicionais

1. **SUB transcribe**: pegar SRT do A-roll (palavra-a-palavra).
2. **CUT**: cortar A-roll por timecode, cortar B-roll por beat do script.
3. **SCORE**: trilha de fundo -22 LUFS (não competir com voz).
4. **LOGO**: rodapé final último 1s.
5. **CUT final**: render Remotion 30fps h264.

## Output

`squads/video-editor/output/<date>/<reel-id>/final.mp4` (15-30s vertical pronto)
