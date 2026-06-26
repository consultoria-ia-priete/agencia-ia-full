# ✅ Checklist de conclusão — Funil & Cockpits

## Pré-requisitos
- [ ] Base instalada
- [ ] CRM Funnels conectado (pro `/api/lead`) e, idealmente, Tracking
- [ ] Node + conta Cloudflare

## Personalização (por funil)
- [ ] `{{META_PIXEL_ID}}` trocado pelo SEU pixel
- [ ] `SEU-DOMINIO.com` trocado pelo seu domínio
- [ ] `{{LASTLINK_PRODUTO_*}}` trocados pelos seus checkouts
- [ ] `@{{SEU_INSTAGRAM}}` trocado
- [ ] `wrangler.toml` (account_id, domínio) preenchido
- [ ] `functions/api/lead.ts` apontando pro SEU CRM Funnels
- [ ] Nenhum `SEU-DOMINIO`/`{{...}}` cru sobrando

## Deploy
- [ ] `npm run build` ok
- [ ] `wrangler pages deploy dist` no ar + domínio custom apontado

## Validação (teste de fogo)
- [ ] Lead de teste chega no CRM Funnels + Pixel dispara
- [ ] Cockpit gerado e abrindo

## Segurança
- [ ] `scripts/scan-secrets.sh .` = 0 hits

## Aula
- [ ] Aula gravada: do template ao funil no ar capturando lead
