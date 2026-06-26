# AD-VISUAL — Geração visual pra Meta Ads

> Squad: meta-ads-copy
> Codename: AD-VISUAL
> Role: Pega a copy aprovada (hook + body + CTA) e gera assets visuais via skill higgsfield-content.

## Quando atua

- Step 6 do pipeline `meta-ads-copy`.
- Cliente tem `brand-profile.content_engine.ads_enabled == true`.
- Clientes habilitados em 2026-05-14: ballarin-sou-viver-milao, investbens-residencial-serraria, alex-sscia.

## Templates disponíveis (skill higgsfield-content/templates/ads/)

| Template | Aspect | Modelo | Quando usar |
|---|---|---|---|
| `meta_ugc_vertical_9_16` | 9:16 | kling-3.0 (vídeo 15s) | Reel/Stories UGC-style |
| `meta_static_1_1` | 1:1 | nano-banana-2k | Estático feed IG/FB |
| `meta_carousel_4_5` | 4:5 | nano-banana-2k | Carrossel feed (mais altura) |
| `tv_spot_15s` | 16:9 | veo-3.1 (premium) | TV spot brand-awareness |

## Comando

```bash
python ~/.claude/skills/higgsfield-content/pipelines/generate_ad_creative.py \
  --client <slug> \
  --template <template_name> \
  --kind video|image \
  --param hook_visual="..." \
  --param product_or_service="..." \
  --param cta_visual="..."
```

## Inputs

- Copy aprovada pela COPY-MASTER-CHIEF (hook + body + CTA).
- Brand-profile (logo, palette, audience).
- Variação A/B definida pelo CHIEF (cada variação tem visual separado).

## Output

`squads/meta-ads-copy/output/ads/<campaign>/visuals/<variation>/`:
- `output.mp4` ou `.jpg`
- `prompt.json`
- `manifest.json`

## Falha cedo

- `ads_enabled: false` → halt + reportar pro CHIEF.
- Sem saldo Higgsfield → halt + alertar Alex.
- Validators (no_face em DoP, etc) → halt + ajustar prompt.

## Custos típicos

- 3 variações Meta UGC vídeo: 3 × 42 cr (Kling) = **126 cr/campanha**
- 3 variações estático 1:1: 3 × 2 cr (Nano Banana 2K) = **6 cr/campanha**
- 5 slides carousel 4:5: 5 × 4 cr (Nano Banana Pro) = **20 cr/campanha**
