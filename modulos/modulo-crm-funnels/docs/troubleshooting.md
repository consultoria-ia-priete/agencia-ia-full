# 🆘 Troubleshooting — Integração CRM Funnels

### Sintoma: `ghl_validate.py` retorna 401/403
**Causa:** chave errada/expirada, ou faltou um scope na Private Integration.
**Conserto:** recrie a integração no CRM Funnels com os scopes do Passo 1 e copie a chave de novo.
Nunca injete sem o validate passar.

### Sintoma: validate diz "Location ID trocado"
**Causa:** colou o ID errado.
**Conserto:** Settings → Business Profile → copie o **Location ID** (não o nome).

### Sintoma: o Claude não enxerga o MCP do CRM Funnels depois de instalar
**Causa:** a sessão não recarregou o `.mcp.json`.
**Conserto:** feche e reabra o Claude Code **dentro da pasta da agência**.

### Sintoma: `send_sms`/mensagem "deu sucesso" mas não chegou
**Causa:** a API do CRM Funnels retorna sucesso otimista; status real (delivered/failed) só
aparece relendo a conversa depois de alguns segundos.
**Conserto:** releia a thread com um pequeno delay pra confirmar a entrega.

### Sintoma: quero desconectar o CRM Funnels
**Conserto:** `python3 .claude/skills/install-crm-funnels/ghl_inject.py --client-dir <agência> --remove`
