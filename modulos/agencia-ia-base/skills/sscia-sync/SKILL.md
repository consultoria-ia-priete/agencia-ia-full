---
name: sscia-sync
description: Skill GLOBAL pra propagação de squads/agentes/playbooks do _TEMPLATE_SSCIA pra todos os clientes da agência, com confirmação obrigatória, backup automático e proteção hardcoded de arquivos exclusivos do cliente (brand-profile, CRM Funnels keys, memórias, output).
---

# 🔄 sscia-sync — Propagação template → clientes

Skill pra orquestrar a fábrica multi-cliente da agência. Resolve dois cenários:

1. **Provisionar cliente novo** do zero (substitui o `novo-cliente.sh`)
2. **Propagar updates** (squad, agente, playbook novo ou atualizado) pra todos os clientes existentes — sem destruir customização local nem perfis/credenciais.

## Contrato firmado (não viola nunca)

### 🟢 PROPAGÁVEL (template → clientes, com confirmação)
- `squads/*/squad.yaml`
- `squads/*/squad-party.csv`
- `squads/*/agents/*.md`
- `squads/*/playbooks/*.md`
- `squads/*/tasks/*.md`

### 🔒 EXCLUSIVO DO CLIENTE (NUNCA sobrescreve, hardcoded)
- `_opensquad/_memory/*` (brand-profile, company, brand-kit, preferences, credentials, ghl-credentials)
- `squads/*/_memory/*` (CHRONICLER local de cada squad)
- `squads/*/output/*` (trabalho gerado)
- `.mcp.json` (CRM Funnels key, MCPs por cliente)
- `.claude/`
- `.sscia-backup/`
- `.sscia-state.json`
- Qualquer arquivo cujo nome contenha `credentials`, `local`, `secret` ou `.env`

## Comandos

```bash
# ── Provisionar cliente novo ──────────────────────────────────────
sscia-sync --new-client JRS_FLOORING                # interativo
sscia-sync --new-client JRS_FLOORING \              # com flags
  --operator "Alex Priete" \
  --brand-main "JRS Flooring" \
  --instagram "@jrsflooring" \
  --industry "hardwood flooring services" \
  --country US --state NJ \
  --language en-US \
  --ghl-key "pit-xxx" \
  --ghl-location "xxx"

# ── Propagar TUDO de lógica pra TODOS os clientes ─────────────────
sscia-sync --propagate-all                          # pede confirmação por cliente
sscia-sync --propagate-all --dry-run                # só mostra diff, não aplica
sscia-sync --propagate-all --skip-customized        # pula arquivos customizados sem perguntar

# ── Propagar peça específica ──────────────────────────────────────
sscia-sync --propagate-squad nexus                  # 1 squad pra todos
sscia-sync --propagate-squad nexus --client ALEX_SSCIA   # 1 squad pra 1 cliente
sscia-sync --propagate-agent ad-creative-strategist \
           --in-squad meta-ads-copy

# ── Inventário ────────────────────────────────────────────────────
sscia-sync --status                                  # tabela de clientes + estado de sync

# ── Sempre disponível ─────────────────────────────────────────────
sscia-sync --help
sscia-sync --dry-run [qualquer comando]              # preview sem aplicar
```

## Fluxo de propagação

```
sscia-sync --propagate-all
  ↓
Pra cada cliente em PROJETOS_CLAUDE_CODE/ que tem _opensquad/ e squads/:
  ↓
1. Lê CLIENT/.sscia-state.json (hashes da última sync)
  ↓
2. Pra cada arquivo PROPAGÁVEL no template:
   - Calcula hash do arquivo no cliente atualmente
   - Compara com hash da última sync
   - Se ≠ → CUSTOMIZADO (cliente editou após última sync)
   - Calcula hash do arquivo no template
   - Se hash_template ≠ hash_state → ATUALIZADO no template (vale a pena propagar)
  ↓
3. Mostra ao operador:
   ✓ N arquivos atualizados no template (vai propagar)
   ⚠️ M arquivos CUSTOMIZADOS no cliente (vai sobrescrever a customização?)
   🔒 Arquivos EXCLUSIVOS preservados sempre
  ↓
4. Pede confirmação: y / n / skip-customized / details
  ↓
5. Backup em CLIENT/.sscia-backup/{timestamp}/
  ↓
6. Aplica substituições (placeholders → valores do brand-profile.json)
  ↓
7. Copia, atualiza .sscia-state.json
  ↓
8. Próximo cliente
```

## Substituições aplicadas (placeholders → brand-profile.json)

| Placeholder | Vem de |
|---|---|
| `{{CLIENTE_NOME}}` | `client.operator` |
| `{{CLIENT_ID}}` | `client.id` |
| `{{MARCA_PRINCIPAL}}` | `brand.main` |
| `{{COMUNIDADE}}` | `brand.community` |
| `{{PRODUTO_RECORRENTE}}` | `brand.saas_recurring` |
| `{{NICHO_PRINCIPAL}}` | `brand.industry` |
| `{{CLIENTE_IG}}` | `social.instagram_handle` |
| `{{SITE_PRINCIPAL}}` | `websites.primary` |
| `{{SITE_LOWTICKET}}` | `websites.lp_low_ticket` |
| `{{SITE_QUIZ}}` | `websites.quiz` |
| `{{TRACKING_DOMAIN}}` | `websites.tracking` |
| `{{DOMINIO_PRINCIPAL}}` | `websites.domain_root` |
| `{{EMAIL_OPERADOR}}` | `client.owner_email` |
| `{{IDIOMA_PUBLICACAO}}` | `language.publication` |
| `{{GEO_RESTRICAO}}` | derivado de `geo.exclusions[0]` |
| `{{RESULTADO_PROMETIDO}}` | `audience.promise` |
| `{{GHL_LOCATION_ID}}` | `publishing.ghl_location_id` |
| `{{NICHO_BUSCA}}` | `seo.primary_keywords[0]` ou `brand.industry` |
| `{{TICKET_RECORRENTE}}` | placeholder vazio se não tiver |
| `{{REFERENCIAS_MERCADO}}` | placeholder vazio se não tiver |
| `{{CREATED_AT}}`, `{{LAST_UPDATED}}` | data corrente |

## Arquivos da skill

| Arquivo | Propósito |
|---|---|
| `SKILL.md` | Este arquivo |
| `sync.py` | Script principal Python |
| `sscia-sync` | Wrapper bash chamável (symlink em `~/.local/bin/`) |
| `PROTECTED_PATHS.md` | Documentação do contrato de paths protegidos |

## Operação diária (lembrete)

Pra trabalhar com um cliente específico, **sempre entre na pasta do cliente** primeiro:

```bash
cd ~/Documents/PROJETOS_CLAUDE_CODE/FLOOR_TO_CEILING
/opensquad run nexus
```

`sscia-sync` é meta-operação (atualiza estrutura de múltiplos clientes ao mesmo tempo). Roda da pasta raiz `PROJETOS_CLAUDE_CODE/` ou de qualquer lugar via wrapper.
