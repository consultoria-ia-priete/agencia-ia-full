# Task — entrega (step 6)

## Owner

CINE (chief).

## Input

- 3 vídeos gerados (output/videos/<id>/output.mp4)
- 5 imagens geradas (output/images/<id>/output.jpg)
- 3 captions (output/captions/<id>.md)
- 3 manifests vídeo + 5 manifests imagem (output/manifests/*.json)

## Push pro worker

Pra cada peça (vídeo ou imagem), POST pra `{{SEO_WORKER_DOMAIN}}/admin/queue`:

```json
{
  "slug": "{{CLIENT_ID}}",
  "creative": {
    "id": "<manifest_id>",
    "tema": "<tema da semana>",
    "caption": "<caption completa>",
    "urls": ["<url do CRM Funnels CDN OU URL pública R2>"],
    "media_type": "video/mp4" | "image/jpeg",
    "kind": "video" | "ad_creative" | "carousel",
    "duration_s": 30 | null,
    "aspect_ratio": "9:16" | "1:1",
    "platforms": ["instagram", "facebook", "google_business_profile"],
    "status": "pending",
    "scheduled_for": "<ISO 8601 — quando programar publicação>"
  }
}
```

Header: `X-Admin-Token: <token MESTRE>`.

## Saída

`squads/cinematic-content/output/<date>/_pacote-final.md`:

```markdown
# Pacote semanal — {{CLIENTE_NOME}} — semana <YYYY-WW>

## Vídeos (3)
- [Hero] [view dashboard](https://{{SEO_WORKER_DOMAIN}}/{{CLIENT_ID}}/?id=<id>)
- [Lifestyle 1] ...
- [Lifestyle 2] ...

## Imagens (5)
- [Img 1] ...
- ...

## Custos
- Higgsfield: 136 créditos
- video-edit (se usado): X créditos RunComfy

## Status
Todas peças em status: pending no dashboard. Aguarda aprovação do operador.
```

## Checklist final

- [ ] Todos 8 manifests atualizados pra `status: pushed`
- [ ] Worker retornou 200 OK em todos os POSTs
- [ ] Dashboard mostra todas as 8 peças em pending
- [ ] Operador notificado (Slack/email — manual)
