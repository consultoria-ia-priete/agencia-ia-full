# 📡 ghl-publisher — Skill GLOBAL de Publicação no CRM Funnels

> **Skill oficial do ecossistema** pra publicação social via CRM Funnels API. Atende todos os clientes da agência via brand-profile.json.
>
> **Localização:** `~/.claude/skills/ghl-publisher/` (global desde 2026-05-02). ALEX_SSCIA mantém symlink em `_opensquad/skills/ghl-publisher` pra compatibilidade.

---

## 🎯 Quando usar esta skill

Use esta skill **sempre** que precisar:

- ✅ Publicar carrossel ou single image em Instagram, Facebook, Google Business Profile (multi-platform em 1 chamada)
- ✅ Publicar/agendar no LinkedIn (legacy, Alex Priete)
- ✅ Listar, atualizar ou deletar posts via API
- ✅ Hospedar imagens em CDN que o Instagram aceite
- ✅ Diagnosticar falhas de publicação ("Social Platform could not fetch the media", platform=google, etc.)

**Suporte por plataforma:**
- ✅ **Instagram** (carrossel + single)
- ✅ **Facebook Page** (carrossel + single)
- ✅ **Google Business Profile** (single + CTA button: BOOK / LEARN_MORE / CALL / etc.)
- ✅ **LinkedIn** (legacy, single ou carrossel)
- ⏳ TikTok (planejado)
- ⏳ Vídeo / Reels (planejado, junto com viral-video-factory)
- ❌ Stories (não suportado pela API CRM Funnels)

---

## 🚀 Snippet preferido (multi-plataforma) — `multi_platform_post.py`

```python
from multi_platform_post import publish_multi

res = publish_multi(
    client_dir="/Users/.../FLOOR_TO_CEILING",
    platforms=["instagram", "facebook", "google_business_profile"],
    image_urls=["https://...slide-01.jpg", "...slide-02.jpg", "..."],
    caption="Spring cleaning before/after... Book your free quote — link in bio.",
    gmb_cta={"action": "BOOK", "url": "https://floortoceilingcleanings.com/"},
    dry_run=False,
)
```

**Resolve automaticamente:**
- CRM Funnels key + location → `<client>/.mcp.json`
- accountIds (IG, FB, GMB) → `<client>/_opensquad/_memory/brand-profile.json` → `publishing.ghl_account_ids`
- post_signature → adiciona automático no fim da caption
- Split de payload: IG+FB+LI vão em 1 request (carrossel ok); GMB vai em request separado (1 img + CTA button)
- Truncamento de caption respeita limite menor entre as plataformas selecionadas

---

---

## ⚡ TL;DR — Os 5 mandamentos

1. **Sempre faça upload das imagens via CRM Funnels Media Library** (`POST /medias/upload-file`) — Instagram **rejeita** catbox.moe, 0x0.st, transfer.sh. Só `assets.cdn.filesafe.space` (CDN do CRM Funnels com Google Cloud Storage por trás) funciona consistentemente.
2. **Use o schema novo da API:** `type: "post"`, `media: [{url, type: "image/jpeg"}]`, `scheduleDate`. **NÃO** use `fileIds`, `scheduledAt` ou `type: "Image"` (deprecated, retorna 422).
3. **`media.type` aceita SOMENTE `"image/jpeg"`** — não `"image/png"`, não `"IMAGE"`. Converta PNG para JPEG antes (use `sips`).
4. **Bug platform=google:** `status="scheduled"` com `scheduleDate` >5 min no futuro cria sub-posts inválidos que se auto-deletam. **Workaround: prefira `status="published"`** (imediato) sempre que possível.
5. **Headers obrigatórios em TODA requisição:** `Authorization: Bearer pit-...`, `Version: 2021-07-28`, `User-Agent: Mozilla/5.0 ...`. Sem User-Agent = 403/1010 (Cloudflare WAF).

---

## 🗂️ O que tem nesta skill

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | Este overview + quando usar |
| `references/api-schema.md` | Schema completo da API: endpoints, payloads, formatos |
| `references/troubleshooting.md` | Lista de erros conhecidos com causa e fix |
| `references/credentials.md` | IDs e credenciais (locationId, accountIds, userId, API key) |
| `snippets/upload_media.py` | Upload local file → CRM Funnels CDN URL |
| `snippets/create_post.py` | Criar/agendar post (carrossel ou single) |
| `snippets/list_posts.py` | Listar posts por intervalo de datas |
| `snippets/delete_post.py` | Deletar post por ID |
| `snippets/full_publish_pipeline.py` | Pipeline completo: upload → criar → verificar |
| `checklists/pre-publish.md` | Checklist obrigatório antes de qualquer publicação |

---

## 🚦 Fluxo recomendado de publicação

```
┌──────────────────────────────────────────────────────────────┐
│  1. PREPARAR ASSETS                                          │
│     • Imagens em JPEG (1080×1440 para carrossel — 3:4)       │
│     • Caption escrita com CTA padrão (Diretiva NEXUS-001)    │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  2. UPLOAD VIA CRM Funnels MEDIA LIBRARY                             │
│     • POST /medias/upload-file (multipart)                   │
│     • Retorna URL em assets.cdn.filesafe.space               │
│     • snippets/upload_media.py                               │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  3. CHECKPOINT: APROVAÇÃO DO ALEX                            │
│     • Mostrar prévia visual + caption + URLs                 │
│     • Aguardar OK explícito                                  │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  4. CRIAR POST                                               │
│     • POST /social-media-posting/{LOC}/posts                 │
│     • status="published" (imediato — preferido)              │
│     • OU status="scheduled" com scheduleDate <5min futuro    │
│     • snippets/create_post.py                                │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  5. VERIFICAR (após ~10s)                                    │
│     • GET /social-media-posting/{LOC}/posts/{id}             │
│     • Confirmar platform = instagram OU linkedin             │
│     • Confirmar status = published                           │
│     • Confirmar media count = N (todos os slides)            │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│  6. REGISTRAR                                                │
│     • Atualizar log-publicacoes.md do squad                  │
│     • Salvar IDs CRM Funnels e URLs                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🤝 Agentes que devem usar esta skill

| Squad | Agente | Uso |
|---|---|---|
| Conteúdo Viral | **PULSE** 📡 | Publicador principal — usa em todos os carrosséis |
| Meta Ads Copy | **TRIGGER** | Pode usar para reaproveitamento orgânico de criativos |
| Tráfego Pago | **FLUX** | Não publica, mas consulta status para reportar performance |
| Branding | **CORE** | Pode usar para auditar histórico de publicações |
| Landing Pages + SEO | **GATE** | Pode usar para postar updates de LPs |
| Infraestrutura | **INFRA** | Configura workflows CRM Funnels relacionados (CTA dual aula/treinamento) |

**Qualquer novo agente** que vier a publicar em redes sociais via CRM Funnels deve **referenciar esta skill no seu `.agent.md`** e seguir o fluxo recomendado.

---

## 🚨 Avisos importantes

### Sobre custos e rate limits
- A API do CRM Funnels não cobra por requisição, mas tem rate limit não documentado
- Em uploads de muitas imagens, faça delays de ~1-2s entre cada um
- Não tente fazer mais de ~30 requisições por minuto

### Sobre token expiry
- A `pit-*` API key não expira automaticamente, mas o **token interno do canal Instagram** pode expirar (erro: "Social Account token has expired")
- Quando isso acontece, Alex precisa reconectar o Instagram no CRM Funnels UI
- Use `GET /social-media-posting/{LOC}/accounts` para verificar status dos canais conectados antes de publicar

### Sobre o bug platform=google (CRÍTICO)
- **Não confiar em agendamentos com >5min de antecedência** via API
- Posts agendados com horário futuro distante criam sub-posts inválidos com `platform=google`
- Esses sub-posts são auto-deletados pelo CRM Funnels no momento do disparo
- O parent post pode (ou não) recriar sub-posts corretos automaticamente — comportamento instável
- **Sempre prefira publicação imediata** (`status="published"`) ou agendamento muito próximo (<5min)
- Para agendamentos longos, considere: agente acorda perto do horário-alvo e cria com publish imediato

---

## 📚 Histórico e contexto

Esta skill condensa aprendizados de uma operação real onde:
- 6 carrosséis foram publicados ao longo de 2 dias
- Múltiplos CDNs foram testados (catbox, 0x0.st, transfer.sh) — todos falharam
- O bug platform=google quebrou 4 agendamentos antes de ser diagnosticado
- A solução final (CRM Funnels media library + status=published) só foi descoberta após ~6h de debug

**Documentar tudo aqui evita que qualquer futuro agente precise repetir esse caminho.**
