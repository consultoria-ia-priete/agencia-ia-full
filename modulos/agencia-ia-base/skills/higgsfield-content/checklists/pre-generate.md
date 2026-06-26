# Pre-generate checklist — higgsfield-content

Rodar mentalmente (ou marcar) **antes** de cada execução de pipeline.

## 1. Cliente / brand-profile

- [ ] Cliente está habilitado: `_opensquad/_memory/brand-profile.json` existe e tem `content_engine` preenchido.
- [ ] `content_engine.group` casa com o pipeline:
  - `cinematic-content` → group A
  - `viral-reels-seo` → group B ou B-prime
- [ ] Se for ads: `content_engine.ads_enabled` está `true`.
- [ ] Se for ConsultorIA Alex: `content_engine.carousel_canon` é `true` — **não interferir** com carrossel diário 14h BRT (Diretiva NEXUS-001 v2).

## 2. Higgsfield

- [ ] Plano Higgsfield assinado (verificar status no MCP).
- [ ] OAuth autenticado nesta sessão (primeira chamada MCP dispara browser).
- [ ] Saldo de créditos suficiente pra batch planejado (consultar via `mcp__claude_ai_Higgsfield__balance` se disponível).
- [ ] Não estourar 320 créditos/sem cross-cliente sem checar custo com Alex.

## 3. Template

- [ ] Template existe em `templates/<subdir>/<name>.yaml` (não `.RESERVED`).
- [ ] Todos `required_params` do template estão em `--param key=value`.
- [ ] Se for `dop-7s-reel`: prompt NÃO menciona rosto/pessoa (validator vai pegar, mas confere de olho).

## 4. Output

- [ ] Diretório `<CLIENT>/squads/<squad>/output/<date>/` existe ou será criado.
- [ ] Não há conflito de id (manifest_id auto-gerado por timestamp, raro mas possível).

## 5. Aprovação

- [ ] Saber qual squad é dono — output vai pro dashboard `{{SEO_WORKER_DOMAIN}}/<slug>` com `status: pending` (Diretiva MESTRE 2026-05-07).
- [ ] **NUNCA** publicar direto sem passar pelo dashboard de aprovação canônica.

## 6. Compliance

- [ ] **MCMV (Ballarin / Investbens):** disclaimer Lei 4.591/64 obrigatório em peças com valores. "*A partir de R$ XXX/mês, sujeito a análise de crédito e aprovação MCMV.*"
- [ ] **ConsultorIA (Alex):** sem palavrões, sem dicotomia, CTA rotativo (Aula | IA | ConsultorIA) — nunca misturar 2 no mesmo post.
- [ ] **Cleaning/Flooring US (FTC, Mendes, JRs):** sem person/face visível em raw shots DoP (validator bloqueia).

## 7. Audit

- [ ] `manifest.json` será gravado automaticamente (status inicial: `draft`).
- [ ] Atualizar manifest pra `generated` quando MCP retornar.
- [ ] Atualizar manifest pra `pushed` quando enviar pro worker.
- [ ] Atualizar manifest pra `published` quando dashboard publicar.

## Falha cedo

Se qualquer item acima falhar, **pare**. Não force a geração. Reporte ao operador (Alex / Vinicius / cliente owner) e ajuste o brand-profile antes.
