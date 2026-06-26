# 🎬 Aula — Funil & Cockpits

> Aula CURTA (alvo 12–16 min). Alex grava subindo o quiz low-ticket personalizado + o cockpit.
> Pode virar uma série (1 aula por funil). **Pré-produção:** Base + CRM Funnels + (idealmente) Tracking.

## Cena 0 — Gancho (0:00–0:45)
"O funil que vende é o mesmo que eu uso: quiz → webinar → consultoria. Você vai pegar o meu
template, botar a SUA cara e subir na SUA conta. Hoje a gente sobe o quiz."

## Cena 1 — Cópia + `instalar` (0:45–2:00)
- `Use this template` → clone → `cd` → `claude` → **`instalar`** → escolher o **quiz**.

## Cena 2 — Personalizar (2:00–7:00)
- Trocar placeholders: `{{META_PIXEL_ID}}` (seu pixel), `SEU-DOMINIO.com`, `{{LASTLINK_PRODUTO_LOW}}`, `@{{SEU_INSTAGRAM}}`.
- `wrangler.toml`: account_id + domínio.
- `functions/api/lead.ts`: apontar pro SEU CRM Funnels. "Sem isso, o lead ia pro lugar errado."

## Cena 3 — Build + deploy (7:00–11:00)
- `npm install` → `npm run build` → `wrangler pages deploy dist`.
- Apontar domínio custom. Abrir o funil no ar.

## Cena 4 — Prova (11:00–13:30)
- Fazer um lead de teste → mostrar chegando no CRM Funnels + Pixel disparando (Events Manager).

## Cena 5 — Cockpit (13:30–15:00)
- `build-cockpit-webinar.py` → abrir o dashboard do funil. "Acompanhamento na mão."

## Cena 6 — Fechamento
- "Funil no ar, no seu domínio, capturando no seu CRM." Próximo funil / CTA rotativo.

---
### Erros ao vivo
- Placeholder esquecido → lead/pixel errado (reforçar a checagem).
- `wrangler pages deploy` sem account_id → preencher wrangler.toml.
- `/api/lead` 500 → credencial CRM Funnels não configurada.
