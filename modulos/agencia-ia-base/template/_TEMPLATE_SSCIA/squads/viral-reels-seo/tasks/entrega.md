# Task — entrega (step 8)

## Owner

GRIP (chief).

## Push pro worker

POST `{{SEO_WORKER_DOMAIN}}/admin/queue`:

```json
{
  "slug": "{{CLIENT_ID}}",
  "creative": {
    "id": "<reel-id>",
    "tema": "<nicho da semana>",
    "caption": "<caption polida 1.200 chars>",
    "urls": ["<URL do reel mp4>"],
    "media_type": "video/mp4",
    "kind": "video",
    "duration_s": 7,
    "aspect_ratio": "9:16",
    "platforms": ["instagram", "facebook", "tiktok", "google_business_profile"],
    "status": "pending",
    "scheduled_for": "<ISO 8601>"
  }
}
```

Para clientes Grupo B-prime (autoridade pt-BR), `platforms`: `["instagram", "facebook"]` (sem TikTok/GMB por enquanto).

## Saída

`squads/viral-reels-seo/output/<date>/_pacote-final.md`:

```markdown
# Reel semanal — {{CLIENTE_NOME}} — semana <YYYY-WW>

## Asset
- Vídeo: <id>/output.mp4 (7s, 9:16, DoP)
- Template usado: dop_top_down | dop_floor_level | dop_extreme_closeup
- Caption: <id>/caption.md (~1.150 chars)

## Custo
- Higgsfield: 12 créditos

## Status
Em pending no dashboard: https://{{SEO_WORKER_DOMAIN}}/{{CLIENT_ID}}/

## Aprovação
Aguarda operador.
```

## Checklist final

- [ ] Manifest atualizado pra `status: pushed`
- [ ] Worker retornou 200 OK
- [ ] Dashboard mostra reel em pending
- [ ] Operador notificado
