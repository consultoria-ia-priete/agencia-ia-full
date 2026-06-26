---
name: install-meta-ads
description: "Cria o app na Meta e gera o token de API pra controlar anúncios pelo Claude Code (Esquadrão Meta Ads). Use quando o aluno disser 'instalar', 'conectar Meta', 'criar app Meta', 'integrar Meta Ads', 'gerar token', 'começar'. Guia os passos manuais no Business Manager, salva o token no vault e VALIDA com chamada real."
---

# Skill: install-meta-ads — Seu acesso de API à Meta

Você está dando ao aluno **acesso programático à Meta Ads**: criar o app, um System User,
gerar um token de longa duração e validá-lo. O aluno **não programa** — fale simples, um
passo por vez. Os passos no Business Manager são **manuais** (cliques no painel da Meta);
seu papel é guiar com precisão e validar o resultado.

Ao final, o aluno terá um **token Meta** salvo no vault local (`~/.claude/secrets/`),
validado, pronto pra usar nos scripts/squads de tráfego.

> Princípio de segurança da Meta: **1 token por Business Manager** (não reaproveite um token
> entre BMs — a Meta marca como atividade suspeita e bloqueia o app). Se o aluno tem várias
> BMs, repita a Fase 2 pra cada uma, com um System User próprio.

## Passo 0 — Pré-requisitos

- Conta **Facebook Business / Business Manager** com acesso de **Admin** à BM.
- Pelo menos **1 Ad Account** dentro da BM.
- A **Base** instalada (opcional, mas recomendado).
- `curl` e `python3` disponíveis.

## Fase 1 — Criar o App (Meta for Developers)

Guie no navegador:
> **developers.facebook.com → My Apps → Create App**
> - Tipo: **Business**.
> - Nome do app: algo neutro (ex: `Agencia API`).
> - Vincule à sua Business Manager.
> - Em **App Settings → Basic**, anote o **App ID** e o **App Secret** (trate como secret).
> - Adicione o produto **Marketing API**.

Explique: "O app é a 'identidade' que vai falar com a API da Meta."

## Fase 2 — System User + token (no Business Manager)

> **business.facebook.com → escolha a BM → Settings → Users → System Users → Add**
> - Nome: `agencia-prod-<slug-da-bm>` (um por BM).
> - Role: **Employee** (menor privilégio).
>
> **Add Assets** ao System User: selecione os **Ad Accounts** (e Pages/Pixels se for publicar),
> com **Full control / Manage**.
>
> **Assign App**: vincule o app criado na Fase 1 ao System User.
>
> **Generate New Token**:
> - App: o da Fase 1.
> - **Token expiration: Never**.
> - Scopes mínimos: `ads_management`, `ads_read`, `business_management`
>   (+ `pages_read_engagement`, `pages_manage_posts` se for publicar em Pages).
> - Gerar → **copiar o token** (só aparece uma vez).

## Passo 3 — Salvar no vault + VALIDAR

Salve o token com um slug por BM e valide com chamada real:
```bash
mkdir -p ~/.claude/secrets && chmod 700 ~/.claude/secrets
printf %s '<TOKEN>' > ~/.claude/secrets/meta-token-bm-<slug>.txt
chmod 600 ~/.claude/secrets/meta-token-bm-<slug>.txt

python3 .claude/skills/install-meta-ads/meta_validate.py --slug <slug>
```
O validador chama `/me/adaccounts` e lista as contas que o token enxerga.
- Se vier vazio/erro: faltou adicionar assets ao System User, ou o token está errado. Volte à Fase 2.
- Se listar as contas: pronto. Mostre ao aluno ("ele enxerga 2 ad accounts ✓").

> No Windows não há `chmod` igual — o vault já fica protegido pela conta do usuário.

## Passo 4 (opcional) — Meta Ads MCP

Se o aluno quiser operar a Meta por linguagem natural dentro do Claude, ative o
**Meta Ads MCP** (conectado via claude.ai). O token deste módulo continua servindo aos
scripts/squads de tráfego (relatórios, automações).

## Validação final

- [ ] App criado com Marketing API
- [ ] System User (Employee) com Ad Accounts atribuídos + app vinculado
- [ ] Token **Never** gerado e salvo em `~/.claude/secrets/meta-token-bm-<slug>.txt` (chmod 600)
- [ ] `meta_validate.py --slug <slug>` listou as ad accounts
- [ ] `scripts/scan-secrets.sh .` = 0 hits (o token vive no vault, fora do repo)

Marque com o aluno cada item de `aula/checklist.md`.

## Troubleshooting

`docs/troubleshooting.md`. Comuns: app bloqueado por "atividade incomum" (navegador limpo +
rede diferente + cooldown), token sem ad accounts (faltou assets no System User), reaproveitar
token cross-BM (não faça — 1 por BM).
