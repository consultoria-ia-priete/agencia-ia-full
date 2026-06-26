# 🎬 Aula — Esquadrão Meta Ads (app + token de API)

> Aula CURTA (alvo 9–12 min). Alex grava criando o app + token numa BM de teste.
> **Pré-produção:** BM com 1 ad account; navegador limpo (evita o checkpoint da Meta).

## Cena 0 — Gancho (0:00–0:40)
"Lembra do seu agente de Tráfego (o André), que ficou em modo *preparar* lá na Base? Hoje a
gente **evolui ele pra publicar de verdade** — dando o acesso de API da Meta. Anúncio criado,
otimizado e no ar, por comando."

## Cena 1 — Cópia + baixar (0:40–1:30)
- `Use this template` → clone → `cd` → `claude` → **`instalar`**.

## Cena 2 — Criar o app (1:30–4:00)
- developers.facebook.com → Create App (Business) → Marketing API.
- Anotar App ID/Secret. "Esse é o crachá do seu sistema."

## Cena 3 — System User + token (4:00–8:30)
- business.facebook.com → BM → System Users → Add (Employee).
- **Add Assets**: marcar os ad accounts. "Sem isso, o token não enxerga nada."
- Assign App → Generate Token (**Never**), scopes mínimos. Copiar.

## Cena 4 — Salvar + validar (8:30–11:00)
- Salvar no vault (`meta-token-bm-<slug>.txt`).
- `meta_validate.py --slug <slug>` → mostrar as ad accounts aparecendo. "Validado de verdade."

## Cena 5 — Fechamento
- "Acesso de API à Meta pronto." Próximo módulo / CTA rotativo.
- Reforçar: 1 token por BM.

---
### Erros ao vivo
- App "atividade incomum" → navegador limpo + rede diferente + cooldown 12–24h.
- Token sem contas → faltou Add Assets no System User.
