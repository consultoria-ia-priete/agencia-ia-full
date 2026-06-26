# Playbook — Lifestyle Image Batch (Grupo A)

5 imagens lifestyle 2K/sem por cliente Grupo A.

## Quando usar

- Cliente com `content_engine.group == "A"` e `image_cadence_per_week == 5`.
- Compor carrosséis Instagram, ads estáticos, single-image Reels-cover.

## Mix sugerido (5 imagens/sem)

| # | Tipo | Exemplo |
|---|---|---|
| 1 | Hero estática | Fachada golden hour OU portaria |
| 2 | Cômodo interno | Cozinha integrada com fluxo natural |
| 3 | Cômodo interno | Sala / varanda |
| 4 | Área comum | Piscina / playground / churrasqueira |
| 5 | Detail close | Maçaneta, fechadura, vista da janela |

## Comando (GLOW)

```bash
python ~/.claude/skills/higgsfield-content/pipelines/generate_lifestyle_image.py \
  --client ballarin-sou-viver-milao \
  --template nano_banana_2k_image \
  --param subject="modern apartment living room with natural light, plants, contemporary furniture" \
  --param mood="warm lived-in family Brazilian middle-class lifestyle"
```

5 invocations × 2 créditos = **10 créditos/sem por cliente**.

## Output

`squads/cinematic-content/output/<date>/images/<id>/`:
- `output.jpg` (1:1 2K)
- `prompt.json`
- `manifest.json`
