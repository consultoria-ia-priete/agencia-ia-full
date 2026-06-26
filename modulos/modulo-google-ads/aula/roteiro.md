# 🎬 Aula — Esquadrão Google Ads (MCC + API)

> Aula CURTA (alvo 10–14 min). Como tem o prazo de ~3 dias do Basic Access, a aula mostra
> tudo até o smoke test (leitura) e explica que a escrita libera depois.
> **Pré-produção:** conta Google com MCC; `pip install google-ads google-auth-oauthlib`.

## Cena 0 — Gancho (0:00–0:45)
"Mesmo papo do André de Tráfego: aqui a gente dá pra ele o acesso do **Google Ads** pra publicar
de verdade. São 4 chavinhas que se encaixam — a gente faz juntos. E já adianto: tem um prazo de
3 dias do Google, então a gente começa por ele."

## Cena 1 — Developer Token + Basic Access (0:45–4:00)
- MCC → API Center → gerar Developer Token.
- Solicitar Basic Access (mostrar o modelo de design doc). "Isso aqui demora ~3 dias — por isso é o primeiro passo."
- Salvar dev token + MCC no vault.

## Cena 2 — OAuth no Google Cloud (4:00–8:00)
- Cloud Console → projeto → Enable Google Ads API.
- OAuth consent (Produção) → Credentials → OAuth client **Desktop** → baixar JSON → vault.

## Cena 3 — Refresh token (8:00–10:00)
- `get_refresh_token.py` → navegador → logar como dono do MCC → autorizar. "Token salvo, sem aparecer na tela."

## Cena 4 — Smoke test (10:00–12:30)
- `smoke_test.py` → mostra as contas + `SMOKE_OK`. "Leitura validada. Escrita libera quando o Basic chegar."

## Cena 5 — Fechamento
- "Acesso de API ao Google Ads montado." Lembrar de checar o email do Basic em ~3 dias.
- CTA rotativo.

---
### Erros ao vivo
- refresh_token vazio → app OAuth em "Testing"; publicar em Produção.
- `DEVELOPER_TOKEN_NOT_APPROVED` → Basic pendente; leitura funciona, escrita não.
