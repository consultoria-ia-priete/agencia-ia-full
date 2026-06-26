# 📐 CRM Funnels API — Schema de Publicação Social

> Endpoints, payloads e formatos validados em produção (2026-04-24).

---

## 🌐 Base URL

```
https://services.leadconnectorhq.com
```

## 🔐 Headers obrigatórios (TODA requisição)

```
Authorization: Bearer {{GHL_API_KEY}}
Version: 2021-07-28
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15
```

> ⚠️ **Sem `User-Agent` o Cloudflare WAF retorna 403 (error code 1010).**

Para uploads multipart, substituir `Content-Type` pelo boundary multipart.

---

## 📤 1. Upload de mídia — `POST /medias/upload-file`

**Single source of truth para imagens que serão postadas no Instagram.**

### Request (multipart/form-data)
```
POST /medias/upload-file HTTP/1.1
Host: services.leadconnectorhq.com
Authorization: Bearer pit-...
Version: 2021-07-28
User-Agent: Mozilla/5.0 ...
Content-Type: multipart/form-data; boundary=----FormBoundaryXXX

------FormBoundaryXXX
Content-Disposition: form-data; name="altId"

{{GHL_LOCATION_ID}}
------FormBoundaryXXX
Content-Disposition: form-data; name="altType"

location
------FormBoundaryXXX
Content-Disposition: form-data; name="file"; filename="C05-slide-01.jpg"
Content-Type: image/jpeg

[binary JPEG data]
------FormBoundaryXXX--
```

### Response 200
```json
{
  "fileId": "69ebeaf09a82ea51cf7d6cdd",
  "url": "https://assets.cdn.filesafe.space/{{GHL_LOCATION_ID}}/media/7d6b9ae9-fe5c-43f6-ad2b-812c4848cfa2.jpg",
  "traceId": "54c56601-c54b-44e3-9817-3bbab843f0eb"
}
```

A URL retornada é **publicamente acessível**, com `Content-Type: image/jpeg` e `Content-Length` correto. Backed por Google Cloud Storage. **Funciona com Instagram.**

### Limites
- Máx 25 MB por arquivo
- Apenas JPEG/PNG/PDF/MP4 (para social, use **JPEG** sempre)

---

## 📝 2. Criar post — `POST /social-media-posting/{locationId}/posts`

### Schema do payload (NOVO — 2026)
```json
{
  "type": "post",
  "userId": "{{GHL_USER_ID}}",
  "accountIds": [
    "{{GHL_COMPANY_ID}}_{{GHL_LOCATION_ID}}_{{IG_NATIVE_ID}}"
  ],
  "media": [
    { "url": "https://assets.cdn.filesafe.space/.../slide-01.jpg", "type": "image/jpeg" },
    { "url": "https://assets.cdn.filesafe.space/.../slide-02.jpg", "type": "image/jpeg" }
  ],
  "summary": "Caption do post incluindo hashtags",
  "status": "published",
  "scheduleDate": "2026-04-24T23:30:00.000Z"
}
```

### Campos obrigatórios
| Campo | Tipo | Valores aceitos | Notas |
|---|---|---|---|
| `type` | string | `"post"` \| `"story"` \| `"reel"` | **Não use** `"Image"` (deprecated → 422) |
| `userId` | string | `{{GHL_USER_ID}}` | UserID do Alex no CRM Funnels |
| `accountIds` | array | um ID por requisição | Cada canal precisa de sua própria requisição |
| `media` | array | items: `{url, type}` | `type` **só** aceita `"image/jpeg"` |
| `summary` | string | até ~2200 chars | Caption do post |
| `status` | string | `"draft"` \| `"scheduled"` \| `"published"` | `"published"` = imediato |

### Campos opcionais
| Campo | Quando usar |
|---|---|
| `scheduleDate` | Obrigatório se `status="scheduled"`. ISO 8601 UTC |
| `tags` | Array de tag IDs do CRM Funnels |
| `categoryId` | Categoria do CRM Funnels |
| `followUpComment` | Comentário automático após publicação |

### Campos DEPRECATED (não usar — retornam 422)
| Campo | Substituto |
|---|---|
| `fileIds` | `media: [{url, type}]` |
| `scheduledAt` | `scheduleDate` |
| `type: "Image"` | `type: "post"` |

### Response 201
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Created Post",
  "traceId": "1f27da14-a574-4faa-b32f-dfc46a8fb3b0"
}
```

> ⚠️ **A response NÃO inclui o ID do post criado.** Para obter o ID, use o endpoint de listagem com filtro de data próximo da criação.

---

## 📋 3. Listar posts — `POST /social-media-posting/{locationId}/posts/list`

### Request
```json
{
  "fromDate": "2026-04-24T00:00:00.000Z",
  "toDate": "2026-04-25T00:00:00.000Z",
  "skip": "0",
  "limit": "50"
}
```

> ⚠️ **`skip` e `limit` devem ser STRING, não int.** Passar como int retorna `"skip must be a number string"`.

### Response 200
```json
{
  "results": {
    "posts": [
      { "_id": "69ebfc91...", "summary": "...", "status": "published", "scheduleDate": "..." }
    ]
  }
}
```

> ⚠️ Posts ficam aninhados em `result['results']['posts']`, **não** em `result['posts']`.

---

## 🔍 4. Detalhar post — `GET /social-media-posting/{locationId}/posts/{postId}`

### Response 200 (campos relevantes)
```json
{
  "success": true,
  "results": {
    "post": {
      "_id": "69ebfc91a7472002b07827d2",
      "platform": "instagram",
      "status": "published",
      "accountIds": ["..."],
      "accountId": "{{GHL_COMPANY_ID}}...",
      "media": [{"url": "..."}],
      "summary": "...",
      "publishedAt": "2026-04-24T23:28:17.778Z",
      "postId": "...",
      "error": null,
      "deleted": false
    }
  }
}
```

### Estrutura: parent posts vs sub-posts
- **Parent post** = template (UUID em `parentPostId`)
- **Sub-post** = execução por canal (`platform: instagram` ou `linkedin`)
- O endpoint de detalhar retorna **sub-posts** com `parentPostId` apontando ao parent
- O endpoint de listar pode retornar uma mistura

### Estados de `status`
| Status | Significado |
|---|---|
| `draft` | Rascunho não enviado |
| `scheduled` | Agendado |
| `in_progress` | Sendo processado/publicado agora |
| `published` | Publicado com sucesso |
| `failed` | Falha — ver campo `error` |

### Campo `platform`
| Valor | OK? |
|---|---|
| `instagram` | ✅ Correto |
| `linkedin` | ✅ Correto |
| `google` | ❌ Bug — sub-post inválido, será auto-deletado |
| `null` | ⚠️ Pode ser parent post |

---

## ✏️ 5. Atualizar post — `PUT /social-media-posting/{locationId}/posts/{postId}`

### Quando usar
- Mudar `scheduleDate` de um post agendado
- Atualizar `summary`
- Adicionar `tags`

### Limitação importante
A documentação sugere que atualizações simples funcionam, mas em alguns casos a API exige o **payload completo** (incluindo `accountIds`, `media`, `type`) — caso contrário retorna 422 "accountIds must be an array".

**Recomendação:** Para evitar bugs, é mais confiável **deletar e recriar** do que atualizar.

---

## 🗑️ 6. Deletar post — `DELETE /social-media-posting/{locationId}/posts/{postId}`

### Response 200
```json
{ "success": true, "message": "Social media post {id} deleted successfully" }
```

> ⚠️ Deletar um sub-post **não** deleta o parent post. O parent pode recriar sub-posts no horário agendado.

---

## 🔌 7. Listar canais conectados — `GET /social-media-posting/{locationId}/accounts`

Use para validar que Instagram e LinkedIn estão conectados antes de publicar.

### Response 200
```json
{
  "results": {
    "accounts": [
      { "_id": "{{GHL_COMPANY_ID}}...", "platform": "instagram", "name": "@{{SEU_INSTAGRAM}}", "status": "active" },
      { "_id": "{{GHL_COMPANY_ID}}...", "platform": "linkedin", "name": "{{SEU_NOME}}", "status": "active" }
    ]
  }
}
```

Se algum canal aparecer com `status` diferente de `"active"` ou faltar — **bloquear a publicação** e pedir para Alex reconectar no CRM Funnels UI.
