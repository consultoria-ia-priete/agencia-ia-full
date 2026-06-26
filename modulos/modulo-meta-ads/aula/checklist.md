# ✅ Checklist de conclusão — Esquadrão Meta Ads

## Pré-requisitos
- [ ] Business Manager com acesso Admin + ao menos 1 Ad Account
- [ ] `python3` responde

## Instalação
- [ ] App criado (Business) com Marketing API; App ID/Secret anotados
- [ ] System User (Employee) criado, com Ad Accounts em Add Assets e app vinculado
- [ ] Token **Never** gerado com scopes mínimos (ads_management, ads_read, business_management)
- [ ] Token salvo em `~/.claude/secrets/meta-token-bm-<slug>.txt` (chmod 600)

## Validação (teste de fogo)
- [ ] `meta_validate.py --slug <slug>` listou as ad accounts
- [ ] (se várias BMs) 1 token por BM, cada um validado

## Segurança
- [ ] Token só no vault, nunca no repo
- [ ] `scripts/scan-secrets.sh .` = 0 hits

## Aula
- [ ] Aula gravada: do Create App até as ad accounts aparecendo no validate
