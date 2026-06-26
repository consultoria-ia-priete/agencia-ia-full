---
name: install-base
description: "Instala NOSSA Base por cima de um Opensquad já existente: adiciona as skills globais (ghl-publisher, creative-factory, higgsfield-content, carousel-generator, viral-video-factory, sscia-sync) e ATUALIZA o framework Opensquad, SEM apagar a empresa/squads que o aluno já criou. Use quando o aluno disser 'instalar a base', 'atualizar', 'puxar as skills', 'começar'."
---

# Skill: install-base — Nossa Base por cima do seu Opensquad

O aluno **já instalou o Opensquad e criou a empresa/squad dele** (a aula anterior, fluxo
nativo `/opensquad create`). Agora ele instala **a NOSSA Base**: ela **adiciona as skills da
agência** e **atualiza o framework Opensquad**, **sem mexer no que ele já criou** (a empresa
dele, as squads dele, as memórias). Atualização **aditiva e protegida**.

O aluno **provavelmente não programa** — fale simples, um passo por vez, comemore os marcos.

Ao final, ele terá: as skills globais da agência em `~/.claude/skills/`, o framework Opensquad
atualizado, e **a empresa + squads dele intactas**.

> 🔒 **Contrato (NUNCA viole):** não sobrescreva `_opensquad/_memory/*` (company.md,
> brand-profile, preferences), `squads/*/_memory/*`, `.mcp.json`, `.env`, nem as squads que o
> aluno criou. Em dúvida, pergunte antes de copiar por cima.

## Passo 0 — Pré-requisitos

- **Opensquad já instalado** e a empresa criada (existe a pasta do projeto dele com
  `_opensquad/_memory/company.md` preenchido + as squads dele). Se NÃO existe, pare e mande
  ele fazer a aula de instalação do Opensquad primeiro.
- `git`, `python3`, `node`/`npx` respondendo. (`claude --version`, `git --version`.)

Pergunte qual é a pasta do projeto do aluno (onde está o `_opensquad/`). Guarde como `PROJ`.

## Passo 1 — Baixar a Base (git)

Repo da Base: **https://github.com/consultoria-ia-priete/agencia-ia-base**

Experiência do aluno (recomendado): abra o link → botão verde **`Use this template`** →
`Create a new repository` (gera a cópia dele) → clona a cópia:
```bash
git clone https://github.com/SEU_USUARIO/minha-agencia-base.git
cd minha-agencia-base
```
Atalho pra teste/gravação (clona direto, sem gerar cópia):
```bash
git clone https://github.com/consultoria-ia-priete/agencia-ia-base.git
cd agencia-ia-base
```
Confirme que está dentro da pasta da Base (tem `skills/`, `template/`, `.claude/`).

## Passo 2 — Adicionar as skills da agência

Copia as skills pra `~/.claude/skills/` (idempotente — atualiza sem apagar as que ele já tem):
```bash
mkdir -p ~/.claude/skills
for s in sscia-sync ghl-publisher carousel-generator creative-factory higgsfield-content viral-video-factory; do
  cp -R "skills/$s" ~/.claude/skills/
done
# opensquad: só atualiza se a nossa versão for mais nova; preserve a do aluno em dúvida.
cp -R skills/opensquad ~/.claude/skills/
```
Resuma: "Suas skills da agência entraram — publicação no CRM Funnels, geração de imagem (fal.ai) e
vídeo (Higgsfield), carrossel, e a fábrica de clientes (sscia-sync)."

## Passo 3 — Habilitar o `sscia-sync` (a ferramenta do update protegido)

```bash
mkdir -p ~/.local/bin
cp ~/.claude/skills/sscia-sync/sscia-sync ~/.local/bin/sscia-sync && chmod +x ~/.local/bin/sscia-sync
```
Garanta `~/.local/bin` no PATH (`export PATH="$HOME/.local/bin:$PATH"` no `~/.zshrc`; reabra o
terminal). Valide: `sscia-sync --help`.

## Passo 4 — Posicionar o molde + ATUALIZAR o Opensquad do aluno (protegido)

O molde traz o NEXUS + as squads-base da agência e as versões novas dos playbooks/tasks.
```bash
cp -R template/_TEMPLATE_SSCIA "$HOME/Documents/PROJETOS_CLAUDE_CODE/_TEMPLATE_SSCIA"
```
Agora aplique o update **protegido** no projeto do aluno. Faça um **dry-run primeiro** pra
mostrar o que vai mudar (e provar que NÃO toca na empresa/squads dele):
```bash
sscia-sync --propagate-all --dry-run
```
Mostre ao aluno: os arquivos de FRAMEWORK/squad-base que serão atualizados, e os
🔒 EXCLUSIVOS preservados (company.md, brand-profile, as squads dele, .mcp.json). Confirmado,
aplique:
```bash
sscia-sync --propagate-all --skip-customized
```
> `--skip-customized` = se ele editou algo, não sobrescreve sem perguntar. O contrato hardcoded
> do sscia-sync já protege `_opensquad/_memory/*`, `squads/*/_memory/*`, `.mcp.json`, `.env`.

## Passo 5 — Validar (empresa intacta + skills no ar)

- [ ] `cat "$PROJ/_opensquad/_memory/company.md"` ainda mostra a empresa que o aluno criou (intacta)
- [ ] `ls ~/.claude/skills/` mostra as skills da agência
- [ ] `cd "$PROJ" && claude` → `/opensquad` abre o menu; as squads dele continuam lá
- [ ] `/opensquad run nexus` passa pelo gate do NEXUS

## Passo 6 — Escritórios dos agentes (dashboard)

```bash
cd "$PROJ" && python3 _opensquad/dashboard/build-office.py 2>/dev/null && open _opensquad/dashboard/office.html
```
"Esse é o escritório — seus agentes e squads num painel."

## Gancho pro próximo curso (importante na aula)

Se o aluno tem um **agente de Tráfego** (ex: o "André Anúncios"), lembre: ele nasce em modo
**"preparar"** — monta campanha/criativos/públicos, mas **só publica quando tiver as credenciais
de API**. Esse é o gancho: **"pra ele publicar de verdade, é o curso Esquadrão Meta Ads / Google
Ads"**. Aponte isso no fim.

## Higiene de segredos

Antes de o aluno versionar a pasta dele: `.gitignore` cobrindo `.mcp.json`, `.env*`,
`_opensquad/_memory/`, `*.bak`. Rode `scripts/scan-secrets.sh "$PROJ"` (0 hits) antes de push.
Nunca comitar `company.md`/`brand-profile.json` preenchidos nem `.mcp.json` com chave.

## Troubleshooting

`docs/troubleshooting.md`. Comuns: `sscia-sync: command not found` (PATH do `~/.local/bin`);
update tentou tocar em arquivo do aluno (responda "n"/`skip-customized`); `/opensquad` não abre
(rodar o `claude` dentro da pasta do projeto dele).
