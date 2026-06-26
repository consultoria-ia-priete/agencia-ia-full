---
name: install-windsor-gmb
description: "Conecta o Windsor.ai ao Claude e puxa dados do Google My Business (reviews, posts, métricas) pra SEO local e prova social. Use quando o aluno disser 'instalar', 'conectar Windsor', 'integrar Google My Business', 'puxar reviews', 'GMB', 'começar'. Não instala software — guia a conexão via claude.ai e o primeiro pull de dados."
---

# Skill: install-windsor-gmb — Windsor.ai + Google My Business

Você está conectando o **Windsor.ai** (um hub de 325+ conectores de dados) ao Claude e
puxando os dados do **Google My Business (GMB)** do aluno: avaliações, posts, métricas.
O aluno **não programa** — fale simples, um passo por vez.

> Diferente dos outros módulos: **não há software pra instalar**. O Windsor.ai é um
> **MCP remoto conectado via claude.ai** (OAuth no navegador). Sem token em arquivo local.

Ao final, o aluno consegue pedir ao Claude coisas como "puxa minhas últimas avaliações do
Google" e usar isso em prova social, SEO local e resposta a reviews.

## Passo 0 — Pré-requisitos

- Conta **Google** que administra o perfil do **Google Meu Negócio** (a ficha da empresa).
- Acesso ao **claude.ai** (pra conectar o Windsor como integração).
- Uma conta no **Windsor.ai** (tem plano free pra começar).

## Passo 1 — Conectar o Windsor.ai no claude.ai

Guie:
> No **claude.ai → Settings → Connectors** (ou "Integrações") → adicione o **Windsor.ai**.
> Autorize via OAuth (login na sua conta Windsor).

Explique: "É uma conexão na nuvem — não fica chave nenhuma na sua máquina."

## Passo 2 — Autorizar o conector Google My Business no Windsor

No painel do Windsor.ai:
> Adicione o conector **Google My Business** (`google_my_business`) → autorize com a conta
> Google que administra a ficha → selecione a(s) localização(ões).

## Passo 3 — Achar o Location ID (formato certo)

O GMB usa o formato `locations/XXXXXXXXXXXXXXXXXXX` (NÃO é o `place_id` do Maps).
Peça ao Claude (via Windsor) pra listar as localizações disponíveis e copie o `locations/...`
da ficha certa. Guarde — é o identificador que você passa nos pulls.

## Passo 4 — Primeiro pull (prova de que funcionou)

Peça ao Claude algo como:
> "Use o Windsor, conector google_my_business, location `locations/<ID>`, e me traga as
> avaliações dos últimos 2 anos: nota, comentário, autor, data e a resposta."

Campos úteis de review: `review_star_rating`, `review_comment`, `review_reviewer`,
`review_create_time`, `review_reply_comment`. Mostre ao aluno a tabela de reviews aparecendo.

## Passo 5 — Ações de escrita (responder review / postar)

O Windsor expõe ações além de leitura. Peça ao Claude pra rodar `list_actions` no conector
`google_my_business` e veja o que dá pra escrever (ex: responder avaliação, publicar post no
GMB). Use sempre com confirmação do aluno antes de publicar.

## Como isso encaixa na agência

- **Prova social:** curar as melhores reviews pra landing pages e criativos.
- **SEO local:** a squad `landing-pages-seo` (agente GMB) usa esses dados na estratégia local.
- **Publicação multiplataforma:** posts em IG+FB+GMB (via `ghl-publisher`).

## Validação final

- [ ] Windsor.ai conectado no claude.ai (OAuth ok)
- [ ] Conector `google_my_business` autorizado, localização selecionada
- [ ] Location ID no formato `locations/...` identificado
- [ ] Pull de reviews retornou dados reais
- [ ] (opcional) `list_actions` mostrou as ações de escrita disponíveis

Marque com o aluno cada item de `aula/checklist.md`.

## Troubleshooting

`docs/troubleshooting.md`. Comuns: usar `place_id` em vez de `locations/...`; conta Google sem
permissão na ficha; conector não aparece em runs headless/cron (a conexão é via claude.ai).
