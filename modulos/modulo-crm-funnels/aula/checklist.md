# ✅ Checklist de conclusão — Integração CRM Funnels

## Pré-requisitos
- [ ] Base instalada (pasta de agência com `.mcp.json` existe)
- [ ] Conta CRM Funnels com acesso à Location
- [ ] `python3` responde

## Instalação
- [ ] Private Integration criada no CRM Funnels com os scopes mínimos
- [ ] `ghl_validate.py` retornou **VÁLIDO** (e listou os canais)
- [ ] `ghl_inject.py` gravou o bloco `gohighlevel` no `.mcp.json` (só um, com backup)

## Validação (teste de fogo)
- [ ] Reabriu o Claude Code e "lista meus contatos do CRM Funnels" funcionou
- [ ] Nenhuma credencial inválida foi gravada

## Segurança
- [ ] `.mcp.json` no `.gitignore`
- [ ] `scripts/scan-secrets.sh <agência>` = 0 hits

## Aula
- [ ] Aula gravada: da criação da chave no CRM Funnels até a leitura de contatos pelo Claude
