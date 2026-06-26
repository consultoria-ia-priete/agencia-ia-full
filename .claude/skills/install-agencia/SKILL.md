---
name: install-agencia
description: "Instala a Agência de IA COMPLETA numa sequência única (pacote completo). Use quando o aluno disser 'instalar', 'instalar tudo', 'montar a agência completa', 'começar'. Orquestra todos os módulos na ordem certa, com checkpoint entre cada um."
---

# Skill: install-agencia — A agência completa, numa sequência

Você está montando a **Agência de IA completa** do aluno, módulo por módulo, na ordem certa.
O aluno **não programa** — fale simples, comemore cada módulo concluído, e **pare num checkpoint
entre os módulos** (ele decide se segue agora ou continua depois).

Cada módulo vive em `modulos/<nome>/` e tem a própria skill de instalação guiada. Sua função é
**conduzir a sequência**: para cada módulo, leia o `SKILL.md` dele e execute aquele passo a passo,
depois confirme o checklist e siga pro próximo.

## Ordem de instalação (não pule pré-requisitos)

| # | Módulo | Pasta | Skill a seguir |
|---|---|---|---|
| 1 | **Base** (obrigatória) | `modulos/agencia-ia-base/` | `install-base` |
| 2 | **Meta Ads** | `modulos/modulo-meta-ads/` | `install-meta-ads` |
| 3 | **Google Ads** | `modulos/modulo-google-ads/` | `install-google-ads` |
| 4 | **Funil & Cockpits** | `modulos/modulo-funil-cockpits/` | `install-funil-cockpits` |
| 5 | **CRM Funnels** | `modulos/modulo-crm-funnels/` | `install-crm-funnels` |
| 6 | **Tracking** | `modulos/modulo-tracking/` | `deploy-stack` |
| 7 | **SEO Content** | `modulos/modulo-seo-content/` | `install-seo-content` |
| 8 | **Windsor/GMB** | `modulos/modulo-windsor-gmb/` | `install-windsor-gmb` |

> A **Base** é sempre primeiro (atualiza o framework + instala as skills que os outros usam).
> Logo depois vêm **Meta (2) e Google (3)** — fecham o gancho do agente de Tráfego (André) que
> ficou em modo *preparar* na Base; o **Google começa cedo** por causa do Basic Access (~3 dias).
> Depois vem o **Funil (4)** e então o **CRM Funnels (5)** — o CRM que recebe os leads do funil. O aluno
> pode pular um módulo que não comprou/não vai usar agora.

## Como conduzir cada módulo

Para o módulo da vez:
1. Anuncie: "Agora vamos montar o **<módulo>**." Diga em 1 frase o que ele entrega.
2. Cheque os **pré-requisitos** daquele módulo (contas/planos). Se faltar, registre e siga pro
   próximo módulo que dê pra fazer agora (não trave a sequência inteira por 1 conta pendente).
3. **Leia** `modulos/<pasta>/.claude/skills/<skill>/SKILL.md` e execute o passo a passo dele,
   um passo por vez, esperando o "ok" do aluno.
4. Ao terminar, rode a **validação final** do módulo e marque o `aula/checklist.md` dele.
5. **Checkpoint:** pergunte se ele quer seguir pro próximo módulo agora ou continuar depois.

## Contas/planos que o aluno vai precisar (avise no começo)

- GitHub + Node + Python (Base) · Cloudflare (Tracking, SEO Content, Funil)
- CRM Funnels (CRM Funnels) · fal.ai + Higgsfield (SEO Content) · Meta Business Manager (Meta Ads)
- Google Ads MCC + Google Cloud (Google Ads — ⚠️ Basic Access ~3 dias) · Windsor.ai (GMB)

Diga isso logo no início pra ele já ir abrindo as contas. O **Google Ads** começa cedo por
causa do prazo de aprovação.

## Validação final (a agência inteira)

- [ ] Base: `/opensquad` abre e `/opensquad run nexus` passa pelo gate do NEXUS
- [ ] Cada módulo instalado tem o checklist 100% (os que o aluno escolheu fazer)
- [ ] `scripts/scan-secrets.sh .` = 0 hits antes de qualquer push

## Higiene de segredos

Nenhum módulo escreve segredo no repo. Antes de o aluno versionar qualquer coisa, rode
`scripts/scan-secrets.sh .`. `.mcp.json`, `.env*`, `wrangler.toml`, vault e `*.bak` ficam fora do git.

## Encerramento

Mostre o panorama do que ficou pronto e o que ficou pendente (ex: Google Ads aguardando Basic
Access). Parabenize: a agência de IA dele está no ar.
