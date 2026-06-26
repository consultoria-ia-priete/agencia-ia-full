# 🚨 Troubleshooting — Erros conhecidos da API CRM Funnels Social

> Se você bater num erro que **não** está aqui, documente para evitar que outros agentes percam tempo.

---

## ❌ Erro: HTTP 422 "property fileIds should not exist"

**Causa:** Está usando o schema antigo da API (`fileIds`, `type: "Image"`, `scheduledAt`).

**Fix:** Migrar para schema novo:
- `fileIds: [...]` → `media: [{url, type: "image/jpeg"}]`
- `type: "Image"` → `type: "post"`
- `scheduledAt: "..."` → `scheduleDate: "..."`

Ver `references/api-schema.md`.

---

## ❌ Erro: HTTP 422 "media.0.Invalid media format type"

**Causa:** O campo `media[].type` recebeu valor inválido. **Só aceita `"image/jpeg"`**.

**Fix:**
- ❌ `"image/png"` → converter PNG para JPEG (`sips -s format jpeg in.png --out out.jpg`) e usar `"image/jpeg"`
- ❌ `"IMAGE"` → `"image/jpeg"`
- ❌ `"jpg"` → `"image/jpeg"`

---

## ❌ Erro: HTTP 422 "skip must be a number string"

**Causa:** No endpoint `/posts/list`, passou `skip` ou `limit` como inteiro JSON.

**Fix:** Passar como **string**:
```python
# ❌ Errado
{ "skip": 0, "limit": 50 }
# ✅ Certo
{ "skip": "0", "limit": "50" }
```

---

## ❌ Erro: HTTP 422 "scheduleDate must be after current date"

**Causa:** Está tentando agendar com `scheduleDate` no passado.

**Fix:** Use UTC com pelo menos 60 segundos de margem futura, ou use `status="published"` (imediato) e remova `scheduleDate`.

---

## ❌ Erro: HTTP 403 / "error code: 1010"

**Causa:** Cloudflare WAF bloqueando a requisição.

**Fix:** Adicionar header `User-Agent` com browser válido:
```
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15
```

Sem User-Agent, requisições Python/curl genéricas são bloqueadas.

---

## ❌ Erro: "Social Platform could not fetch the media from the source"

**Causa raiz:** Instagram (via Meta API) **não consegue baixar** as imagens das URLs informadas.

### Causas comuns
1. **Imagens em catbox.moe** — Instagram rejeita catbox (Content-Length: 0 em HEAD, ou bloqueio direto)
2. **Imagens em 0x0.st / transfer.sh** — esses serviços estão offline ou indisponíveis
3. **URLs com auth/token** — Instagram não envia auth na hora de baixar
4. **CDN com redirect chain longa**
5. **Arquivo vazio (0 bytes)** — verificar com `curl -s -o /dev/null -w "%{size_download}" URL`

### Fix definitivo
**Sempre usar CRM Funnels Media Library** (`POST /medias/upload-file`) — retorna URLs em `assets.cdn.filesafe.space` que **funciona com Instagram**.

Verificar se a URL responde corretamente:
```bash
curl -s -o /dev/null -w "Status: %{http_code} | Size: %{size_download} | Type: %{content_type}\n" "URL"
# Esperado: Status: 200 | Size: >0 | Type: image/jpeg
```

---

## ❌ Erro: "Social Account token has expired, been revoked, or is otherwise invalid"

**Causa:** O token OAuth do canal (Instagram ou LinkedIn) no CRM Funnels expirou ou foi revogado.

**Fix:**
1. Não tem solução via API — precisa de ação manual do Alex
2. Pedir Alex para entrar no CRM Funnels UI → Settings → Integrations → reconectar Instagram (ou LinkedIn)
3. Após reconexão, retentar a publicação

**Prevenção:** Antes de publicar, fazer `GET /social-media-posting/{locationId}/accounts` e validar `status: "active"` para cada canal.

---

## 🐛 BUG: Posts agendados criam sub-posts com `platform=google`

**Sintomas:**
- Post criado com `status="scheduled"` e `scheduleDate` futuro (>5 min)
- `GET /posts/{id}` retorna `platform: "google"` ao invés de `"instagram"` ou `"linkedin"`
- Apenas 1 item em `media[]`, mesmo que tenha enviado 8
- No horário do disparo, o post é **auto-deletado** com `deleted: true`

**Causa:** Bug não documentado da API CRM Funnels no fluxo de scheduling.

**Workarounds (em ordem de preferência):**

1. **🥇 Preferir publicação imediata:**
   ```python
   payload["status"] = "published"
   # NÃO incluir scheduleDate
   ```

2. **🥈 Agendar muito próximo (<5 min):**
   ```python
   from datetime import datetime, timedelta, timezone
   payload["status"] = "scheduled"
   payload["scheduleDate"] = (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()
   ```

3. **🥉 Para agendamentos longos, usar agente cron:**
   - Salvar payload em fila
   - Agente acorda perto do horário-alvo
   - Cria post com `status="published"`

**Validação pós-criação:** Sempre fazer `GET /posts/{id}` ~10s depois e verificar:
- `platform` é `instagram` ou `linkedin` (não `google`)
- `media` tem N itens (todos os slides)
- `status` é `published` ou `in_progress` (não `failed`)

---

## ⚠️ Comportamento estranho: parent post recria sub-posts

**Sintoma:** Você deletou os sub-posts platform=google de um agendamento antigo, mas no horário scheduledo o CRM Funnels **recriou** sub-posts novos automaticamente.

**Explicação:**
- A API tem dois níveis: parent post (template) e sub-posts (execução por canal)
- Deletar um sub-post não deleta o parent
- O parent pode recriar sub-posts no `scheduleDate` original
- Os sub-posts recriados podem ter `platform` correto desta vez (comportamento instável)

**Fix:** Se quiser cancelar definitivamente um agendamento, deletar o **parent post** (o que aparece com `parentPostId: null`).

---

## 📉 Rate limiting (informal)

CRM Funnels não documenta rate limits, mas observamos:
- ~30 req/min por API key parece estável
- Uploads de mídia em rajada (>10 em <5s) podem retornar respostas truncadas
- **Recomendação:** delays de ≥1s entre uploads, ≥0.5s entre criações de post

---

## 🔍 Como diagnosticar uma publicação que falhou

```python
# 1. Listar posts recentes
posts = list_posts(from_date="2026-04-24T00:00:00Z", to_date="2026-04-25T00:00:00Z")

# 2. Para cada post, fetch detalhado
for p in posts:
    details = get_post(p["_id"])
    print(f"ID: {p['_id']}")
    print(f"  platform: {details.get('platform')}")
    print(f"  status: {details.get('status')}")
    print(f"  media count: {len(details.get('media', []))}")
    print(f"  error: {details.get('error')}")
    print(f"  publishedAt: {details.get('publishedAt')}")
```

Padrões a procurar:
- `platform=google` + `media count=1` → Bug do scheduling
- `error="Social Platform could not fetch..."` → CDN errado (ver acima)
- `error="Social Account token..."` → Reconectar canal
- `status=failed` + sem error → Pode ser issue temporário, retry
