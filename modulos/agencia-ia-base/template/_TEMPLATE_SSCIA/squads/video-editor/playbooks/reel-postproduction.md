# Playbook — Reel post-production

Pipeline default pra polir reel Higgsfield raw (7s DoP).

## Fluxo

```
INGEST (raw reel 7s)
   ↓
[opcional] GRADE — apply brand palette via video-edit (RunComfy)
   ↓
[opcional] SCORE — trilha de fundo lo-fi sem letra
   ↓
[obrigatório] LOGO — watermark subtle canto inferior
   ↓
CUT — final render via Remotion (mantém 7s 9:16)
   ↓
DELIVERY → handoff de volta pra viral-reels-seo
```

## Inputs típicos

- `squads/viral-reels-seo/output/<date>/<reel-id>/output.mp4` (raw Higgsfield)
- Brand-profile (logo + paleta)

## Outputs

- `squads/video-editor/output/<date>/<reel-id>/final.mp4` (polished)
- `_handoff.md` indicando que viral-reels-seo pode pushar pro worker

## Custos

- GRADE (video-edit RunComfy): a confirmar
- SCORE (elevenlabs-music): ~$0.05 por trilha 7s
- LOGO: free (Remotion)
- CUT render: free (Remotion local)
