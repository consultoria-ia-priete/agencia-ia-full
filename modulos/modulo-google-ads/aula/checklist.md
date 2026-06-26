# ✅ Checklist de conclusão — Esquadrão Google Ads

## Pré-requisitos
- [ ] Conta Google Ads MCC
- [ ] Acesso ao Google Cloud Console
- [ ] `pip install google-ads google-auth-oauthlib` feito

## Instalação
- [ ] Developer Token gerado no MCC + Basic Access solicitado (design doc anexado)
- [ ] Dev token + MCC ID salvos no vault
- [ ] Google Ads API habilitada no projeto Cloud + OAuth consent em Produção
- [ ] OAuth client (Desktop) baixado e salvo no vault
- [ ] `get_refresh_token.py` salvou o refresh token

## Validação (teste de fogo)
- [ ] `smoke_test.py` terminou com `SMOKE_OK`
- [ ] (depois de ~3 dias) Basic Access aprovado → escrita liberada

## Segurança
- [ ] As 4 credenciais só no vault, nunca no repo
- [ ] `scripts/scan-secrets.sh .` = 0 hits

## Aula
- [ ] Aula gravada: do Developer Token até `SMOKE_OK`
