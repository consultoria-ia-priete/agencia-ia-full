# AD-POST — Pós-produção de ad creative

> Squad: meta-ads-copy
> Codename: AD-POST
> Role: Polir assets gerados pelo AD-VISUAL via squad video-editor (legendas, CTA overlay, watermark, color grade).

## Quando atua

- Step 7 do pipeline `meta-ads-copy` (opcional).
- Quando AD-VISUAL gera vídeo (Meta UGC vertical / TV spot).
- Imagens estáticas/carousel NÃO passam por AD-POST — vão direto pra entrega.

## Handoff pra squad video-editor

```yaml
input:
  source_squad: meta-ads-copy
  source_path: squads/meta-ads-copy/output/ads/<campaign>/visuals/<variation>/output.mp4
  brief:
    add_captions: true               # SUB transcreve voiceover
    add_cta_overlay: true             # CUT renderiza CTA do brand-profile.publishing.default_cta
    add_watermark: true               # LOGO adiciona logo + CRECI rodapé
    color_grade: brand-consistent    # GRADE aplica paleta brand-profile.visual_identity
    music_score: subtle               # SCORE adiciona trilha -22 LUFS

output:
  target_path: squads/meta-ads-copy/output/ads/<campaign>/polished/<variation>/final.mp4
```

## Pipeline video-editor consumido

`reel-postproduction.md` ou `ad-creative-polish.md` dependendo do formato.

## Output

`squads/meta-ads-copy/output/ads/<campaign>/polished/<variation>/`:
- `final.mp4` (polido, pronto pra publicar via Meta Ads Manager)
- `final-with-captions-burned.mp4` (versão com legenda queimada — fallback)
- `captions.srt` (legenda separada — preferida pra Meta)
- `manifest.json`

## Decisão de uso

Não obrigatório. CHIEF decide se a campanha precisa do polish ou se o output bruto do Higgsfield já está aceitável.

Default: polish ON pra Meta UGC vertical + TV spot. OFF pra imagens estáticas.
