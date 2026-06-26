# ✅ Checklist Pré-Publicação CRM Funnels

> Use este checklist **antes** de qualquer publicação no Instagram/LinkedIn via API CRM Funnels.
> Cada item deve ser explicitamente verificado — nada de "deve estar OK".

---

## 1️⃣ Assets

- [ ] Imagens estão em **JPEG** (não PNG, não WebP)
  - Converter PNG → JPEG: `sips -s format jpeg input.png --out output.jpg -s formatOptions 95`
- [ ] Resolução das imagens segue o formato escolhido:
  - **Carrossel:** 1080×1440 (3:4 — Diretiva NEXUS-001)
  - **Single image:** 1080×1080 (1:1) ou 1080×1350 (4:5)
- [ ] Cada arquivo tem **>0 bytes** (verificar `ls -la`)
- [ ] Foto do Alex aparece em todos os slides do carrossel (avatar 64×64 com borda verde)
- [ ] Conteúdo crítico está dentro da zona segura (y: 144→1296 no formato 3:4)

## 2️⃣ Caption

- [ ] Caption escrita em PT-BR
- [ ] Hashtags relevantes ao tema (#ConsultorIA, #IAparaNegocios, #NDE, #AlexPriete)
- [ ] **Última linha da caption tem o CTA padrão** (Diretiva NEXUS-001):
  > Comenta **[PALAVRA]** aqui e eu te mando o link do meu **Treinamento Grátis** de como criar sua ConsultorIA.
- [ ] Palavra-gatilho registrada no log do squad para configuração do workflow CRM Funnels (responsabilidade INFRA)

## 3️⃣ Aprovação do Alex

- [ ] Apresentei prévia visual (lista de títulos dos slides) ao Alex
- [ ] Apresentei caption completa ao Alex
- [ ] Apresentei horário proposto ao Alex
- [ ] **Recebi OK explícito** — não publicar sem isso

## 4️⃣ Validação técnica antes de chamar a API

- [ ] Canais conectados estão `active` (`GET /social-media-posting/{LOC}/accounts`)
- [ ] Imagens já fizeram upload via CRM Funnels Media Library e tenho as URLs `assets.cdn.filesafe.space/...`
- [ ] **NÃO estou usando** catbox.moe, 0x0.st, transfer.sh ou qualquer outro CDN alternativo
- [ ] Validei pelo menos 1 URL no terminal:
  ```bash
  curl -s -o /dev/null -w "Status: %{http_code} | Size: %{size_download}\n" "URL"
  # Esperado: Status: 200 | Size: >0
  ```

## 5️⃣ Estratégia de publicação

- [ ] **Modo preferido: imediato** (`status="published"`, sem `scheduleDate`)
- [ ] Se for agendamento, é **muito próximo** (<5 min no futuro) para evitar bug platform=google
- [ ] Para agendamentos longos, agente tem cron/loop configurado para acordar próximo do horário-alvo

## 6️⃣ Payload da API

- [ ] `type: "post"` (NÃO `"Image"`)
- [ ] `media: [{url, type: "image/jpeg"}]` (NÃO `fileIds`)
- [ ] `media[].type` é literalmente `"image/jpeg"` (NÃO `"image/png"`, `"IMAGE"`, etc.)
- [ ] `userId` é o ID do Alex (`{{GHL_USER_ID}}`)
- [ ] `accountIds` tem **um** account ID (Instagram OU LinkedIn — uma requisição por canal)
- [ ] Headers incluem `Authorization`, `Version: 2021-07-28`, `User-Agent: Mozilla/5.0...`

## 7️⃣ Pós-publicação (validação obrigatória ~10s depois)

- [ ] Localizei o post na listagem (`POST /posts/list`)
- [ ] `GET /posts/{id}` retorna:
  - [ ] `platform` é `instagram` ou `linkedin` (NÃO `google`)
  - [ ] `status` é `published` ou `in_progress` (NÃO `failed`)
  - [ ] `media` tem N itens (todos os slides do carrossel)
  - [ ] `error` é `null`
- [ ] Se algum item acima falhar, **rollback**: deletar post e reportar a Alex

## 8️⃣ Registro

- [ ] Adicionei entrada em `output/log-publicacoes.md` do squad com:
  - Data/hora UTC
  - Carrossel (codinome ex: C08)
  - Canal (Instagram ou LinkedIn)
  - Status (publicado/falhou)
  - ID CRM Funnels do post
  - URN da rede social (se publicado: `urn:li:ugcPost:...` ou IG media ID)

---

## 🚨 Bloqueios automáticos (NÃO publicar se)

- ❌ Algum canal não está `active` no CRM Funnels
- ❌ Alguma imagem tem 0 bytes ou content-type errado
- ❌ Caption não tem o CTA padrão na última linha
- ❌ Não recebi aprovação explícita do Alex
- ❌ Estou tentando agendar com >5min de antecedência sem agente cron configurado
- ❌ Estou usando CDN diferente de `assets.cdn.filesafe.space`
