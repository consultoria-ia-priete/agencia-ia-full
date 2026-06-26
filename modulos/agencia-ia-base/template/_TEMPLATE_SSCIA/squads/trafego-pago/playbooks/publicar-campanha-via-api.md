# Playbook FLUX — Publicar campanha via CRM Funnels Ad Manager API

> Descoberto e validado em 2026-04-27. Cobre Meta (Facebook + Instagram) e Google Ads. LinkedIn requer integração via UI antes.

## Pré-requisitos
1. Wrapper `_opensquad/_tools/ghl-ads.sh` disponível e executável
2. PIT da {{MARCA_PRINCIPAL}} com escopos default (já carregado por padrão no wrapper)
3. Conta da plataforma alvo já conectada via UI da CRM Funnels (Marketing > Ad Manager)

## Headers obrigatórios (já aplicados pelo wrapper)
```http
Authorization: Bearer pit-...
Version: 2021-07-28
Channel: OAUTH         <-- sem este, 403
Source: INTEGRATION    <-- sem este, 403
Content-Type: application/json
```

## Fluxo padrão de publicação

```
TRIGGER aprovou copy + criativo
        ↓
GATE entregou LP destino com URL pública
        ↓
AUDITOR confere coerência (brand, geo {{GEO_RESTRICAO}}, idioma {{IDIOMA_PUBLICACAO}})
        ↓
FLUX monta payload JSON e chama wrapper
        ↓
NEXUS valida resultado e registra em memories.md
```

## Contas {{MARCA_PRINCIPAL}} conectadas (snapshot 2026-04-27)

| Plataforma | Account ID | Detalhe |
|---|---|---|
| Meta | `act_4000740433583600` | Page `112903091740974` ({{MARCA_PRINCIPAL}}) |
| Google | `7646293343` | {{EMAIL_OPERADOR}}, ENABLED |
| LinkedIn | — | NÃO conectado (404) |

⚠️ **Nunca** usar `act_1076769139392165` (Vinicius Vidal) — é a conta pessoal e aparece junto na listagem.

## Exemplo 1 — Listar contas e validar conexão

```bash
cd $PROJECTS_ROOT/FLOOR_TO_CEILING
./_opensquad/_tools/ghl-ads.sh fb-accounts
./_opensquad/_tools/ghl-ads.sh google-accounts
./_opensquad/_tools/ghl-ads.sh fb-integration   # ver pages, fbAdAccountId, pricingModel
```

## Exemplo 2 — Subir campanha Meta (lead gen)

```bash
# 1. Pegar pages disponíveis e lead forms
./_opensquad/_tools/ghl-ads.sh fb-pages
./_opensquad/_tools/ghl-ads.sh fb-lead-forms 112903091740974

# 2. Montar payload conforme schema da doc oficial
#    https://marketplace.gohighlevel.com/docs/ghl/ad-manager/facebook-integration/
cat > /tmp/campaign-payload.json <<'JSON'
{
  "name": "{{MARCA_PRINCIPAL}}-2026-LeadGen-Test",
  "objective": "OUTCOME_LEADS",
  "adAccountId": "act_4000740433583600",
  "pageId": "112903091740974",
  "geo": { "countries": ["US"], "regions": ["New Jersey"], "exclude": ["Pennsylvania"] },
  "budget": { "type": "DAILY", "amount": 25 },
  "leadFormId": "<id retornado por fb-lead-forms>"
}
JSON

# 3. POST via wrapper genérico
./_opensquad/_tools/ghl-ads.sh request POST \
  "/ad-publishing/facebook/ads/campaigns?locationId=9MMGl6sqdAXk1MoF6LyH" \
  /tmp/campaign-payload.json
```

⚠️ **Schema do payload exato precisa ser confirmado nas docs por endpoint** — `objective`/`budget.type` enums variam por plataforma. Sempre testar com `name: "TEST-..."` antes.

## Exemplo 3 — Subir Google Search ad

Mesmo padrão, ajustando path `/ad-publishing/google/...` e payload com keywords + bidding strategy. Doc: https://marketplace.gohighlevel.com/docs/ghl/ad-manager/

## Restrições obrigatórias {{MARCA_PRINCIPAL}} (não viole nunca)

| Restrição | Onde aplica | Origem |
|---|---|---|
| **Excluir Pennsylvania** | Geo targeting de qualquer campanha paga | NEXUS memory 2026-04-25 |
| **Idioma {{IDIOMA_PUBLICACAO}}** | Copy + LP destino | preferences.md |
| **CPL é métrica primária** | Toda decisão de orçamento/scaling | NEXUS memory 2026-04-25 |
| **Geo Smart Bidding em pequenos passos** | Mudanças de geo nunca cortar 80%+ de uma vez | Padrão "Death Spiral" 2026-04-25 |

## Sinais de erro comuns

| Resposta | Causa | Ação |
|---|---|---|
| `403 Token source/channel mismatch` | Faltou `Channel: OAUTH` ou `Source: INTEGRATION` | Use o wrapper, ele aplica automático |
| `404 Cannot GET /ad-publishing/X/campaigns` | Path errado — campanha não tá direto em `/campaigns` | Cheque doc oficial pelo slug correto |
| `404 LinkedIn Integration ... does not exist` | LinkedIn não conectado | Conectar via UI primeiro |
| `422 fields/type must be...` | Reporting endpoint requer params específicos | Adicionar `?fields=...&type=...` |
| `401 Unauthorized` | PIT inválido ou expirado | Regenerar PIT no painel da agência |

## Pós-publicação

1. Confirmar campanha no painel CRM Funnels e na nativa (FB Ads Manager / Google Ads UI)
2. Adicionar tag de UTM se LP for capturar leads via formulário CRM Funnels
3. Verificar se action "Add to Google Ads" do workflow CRM Funnels tá com Custom Mapping ON (lição 2026-04-26)
4. Notificar AUDITOR pra validar 24h depois (campanha entregando? CPL na faixa esperada?)
5. Atualizar `squads/trafego-pago/_memory/memories.md` com a nova campanha
