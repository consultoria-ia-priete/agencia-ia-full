# 🎬 Aula — Integração CRM Funnels

> Aula CURTA (alvo 7–10 min). Alex grava conectando o CRM Funnels de um cliente-exemplo.
> **Pré-produção:** Base já instalada; conta CRM Funnels com uma Location de teste à mão.

## Cena 0 — Gancho (0:00–0:30)
"Seu CRM inteiro nas mãos da IA: criar contato, responder lead, mover oportunidade,
publicar nas redes — tudo por comando. Em poucos minutos, sem código."

## Cena 1 — Cópia + baixar (0:30–1:30)
- `Use this template` → clone → `cd`.

## Cena 2 — `instalar` (1:30–7:00)
Abrir `claude`, digitar **`instalar`**. Narrar a `install-crm-funnels`:
1. **Criar a Private Integration** no CRM Funnels (Settings → Private Integrations) — mostrar os scopes.
2. Copiar a **API Key** (`pit-...`) e o **Location ID**.
3. **Validação** — "olha ele testando a chave de verdade ANTES de salvar; já lista meus canais conectados."
4. **Injeção** no `.mcp.json` (backup automático, não duplica).
5. **Reabrir o Claude Code** pra carregar o MCP.

## Cena 3 — Prova (7:00–9:00)
- Pedir: "lista meus últimos contatos do CRM Funnels" → o Claude responde via MCP.
- Bônus: "cria um contato de teste" e mostrar aparecendo no CRM Funnels.

## Cena 4 — Fechamento
- "CRM Funnels conectado e validado." Próximo módulo / CTA rotativo.

---
### Erros ao vivo
- 401/403 → faltou scope ou chave errada (a validação pega ANTES de gravar).
- MCP não aparece → reabrir o Claude Code na pasta da agência.
