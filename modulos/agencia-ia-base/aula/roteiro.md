# 🎬 Aula — Instalar a NOSSA Base por cima do seu Opensquad

> Aula CURTA (alvo 8–12 min). **Vem DEPOIS** da aula "Instalar o Opensquad e criar seus agentes".
> Aqui o aluno pluga as skills da agência e atualiza o framework — **sem perder o que ele criou**.
> Alex grava num projeto que JÁ tem Opensquad + empresa criada (ex: o GF_CONSULTORIA).

**Pré-produção:** um projeto com Opensquad instalado e uma empresa/squad já criada (da aula
anterior). Mostrar que ela existe ANTES de começar (abrir o company.md / a squad).

## Cena 0 — Gancho (0:00–0:45)
"Na aula passada você instalou o Opensquad e criou seus agentes. Agora vem o pulo do gato:
plugar as skills da agência e turbinar o framework — **sem apagar nada** do que você já montou.
Repara: sua empresa e suas squads vão continuar exatamente onde estão."

## Cena 1 — Mostrar o que já existe (0:45–1:45)
- Abrir `_opensquad/_memory/company.md` e a squad que ele criou. "Isso aqui é seu, e vai ficar."

## Cena 2 — Gerar a cópia + baixar a Base (1:45–3:00)
- `Use this template` → clone → `cd` → `claude` → **`instalar`**.

## Cena 3 — Instalar (3:00–8:00) — com a prova de proteção
- **Skills da agência** entrando em `~/.claude/skills/` (publicação, fal.ai, Higgsfield, carrossel).
- `sscia-sync` habilitado.
- **Update protegido:** rodar primeiro o **`--dry-run`** e MOSTRAR na tela: "esses arquivos de
  framework vão atualizar; estes aqui (sua empresa, suas squads) estão 🔒 protegidos". Aplicar.
- Voltar no `company.md` e na squad dele → **intactos**. "Tá tudo lá. Esse é o ponto."

## Cena 4 — Prova (8:00–10:00)
- `/opensquad` abre; as squads dele continuam; `/opensquad run nexus` passa pelo NEXUS.
- Abrir os **escritórios dos agentes** (dashboard).

## Cena 5 — Fechamento + GANCHO (10:00–11:30)
- "Base instalada, sua agência turbinada e nada perdido."
- **Gancho:** "Repara que o seu agente de Tráfego (o André) já monta campanha — mas ele está em
  modo *preparar*: só publica de verdade quando tiver as credenciais da Meta e do Google. **Isso
  é o próximo curso: Esquadrão Meta Ads / Google Ads.**" CTA rotativo.

---
### Erros ao vivo
- `sscia-sync: command not found` → PATH do `~/.local/bin`.
- O update perguntou se sobrescreve algo do aluno → responder "não" / usar `--skip-customized`.
- `/opensquad` não abre → rodar o `claude` dentro da pasta do projeto dele.
