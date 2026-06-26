# 🆘 Troubleshooting — Funil & Cockpits

### Sintoma: o lead não chega no CRM Funnels / pixel não dispara
**Causa:** placeholder não preenchido (`{{META_PIXEL_ID}}`, credencial CRM Funnels em `/api/lead`).
**Conserto:** preencha o SEU Pixel e configure o destino do lead com a credencial do módulo CRM Funnels.
Confirme que não sobrou `SEU-DOMINIO`/`{{...}}` cru: `grep -rE 'SEU-DOMINIO|\{\{' funis/<funil>/src`.

### Sintoma: `wrangler pages deploy` falha (account_id / projeto)
**Causa:** `wrangler.toml` não preenchido ou projeto Pages inexistente.
**Conserto:** preencha `account_id`; crie o projeto com `--project-name <nome>` no primeiro deploy.

### Sintoma: `npm run build` quebra
**Causa:** dependências não instaladas ou versão de Node antiga.
**Conserto:** `npm install` na pasta do funil; use Node LTS atual.

### Sintoma: o funil abre mas o domínio não resolve
**Causa:** domínio custom não apontado pro projeto Pages, ou DNS propagando.
**Conserto:** configure o domínio no painel Cloudflare Pages; aguarde a propagação.

### Sintoma: o cockpit gera vazio / erro
**Causa:** o gerador espera um readout/JSON de entrada que não existe ainda.
**Conserto:** confira o que o `build-cockpit-*.py` lê (caminho do readout) e gere/aponte o arquivo.
