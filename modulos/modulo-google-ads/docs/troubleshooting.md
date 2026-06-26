# 🆘 Troubleshooting — Esquadrão Google Ads

### Sintoma: `get_refresh_token.py` não retorna refresh token
**Causa:** o app OAuth está em modo "Testing".
**Conserto:** Google Cloud → OAuth consent screen → **Publish app** (Produção). Rode de novo.

### Sintoma: `DEVELOPER_TOKEN_NOT_APPROVED`
**Causa:** o Basic Access ainda não foi aprovado (~3 dias).
**Conserto:** a leitura (smoke test) funciona mesmo assim. A escrita só após o email de aprovação.

### Sintoma: erro de autenticação no smoke test
**Causa:** uma das 4 credenciais está errada/ausente no vault.
**Conserto:** confira os 4 arquivos em `~/.claude/secrets/`: `google-ads-developer-token.txt`,
`google-ads-oauth-client.json`, `google-ads-refresh-token.txt`, `google-ads-mcc.txt`.

### Sintoma: `login_customer_id` inválido
**Causa:** MCC com traços ou ID errado.
**Conserto:** use o MCC só com dígitos (o script já remove traços; confira o `google-ads-mcc.txt`).

### Sintoma: `ImportError: google.ads`
**Conserto:** `pip install google-ads google-auth-oauthlib`.
