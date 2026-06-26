# 🆘 Troubleshooting — Esquadrão Meta Ads

### Sintoma: o app fica bloqueado por "atividade incomum"
**Causa:** padrão que a Meta marca como suspeito (token cross-BM, rede/extensões estranhas).
**Conserto:** navegador limpo (Safari/Firefox sem extensões), rede diferente (hotspot 4G),
cookies de facebook.com limpos. Se persistir, cooldown de 12–24h. Use **1 token por BM**.

### Sintoma: `meta_validate.py` diz "não enxerga nenhum ad account"
**Causa:** o System User não tem os ad accounts atribuídos.
**Conserto:** Business Manager → System Users → seu user → **Add Assets** → marque os ad
accounts com Manage. Gere o token de novo se necessário.

### Sintoma: token rejeitado (190/OAuth)
**Causa:** token copiado errado/incompleto, ou expirou (gerou sem "Never").
**Conserto:** gere de novo com **expiration: Never** e copie inteiro.

### Sintoma: falta permissão pra um scope
**Causa:** scope não marcado na geração do token.
**Conserto:** regenere marcando `ads_management`, `ads_read`, `business_management`
(+ pages_* se for publicar).
