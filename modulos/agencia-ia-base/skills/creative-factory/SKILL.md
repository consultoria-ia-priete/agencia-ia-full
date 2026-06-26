---
name: creative-factory
description: Skill GLOBAL pra geração de imagens (carrosséis, ads, posts) via fal.ai gateway. Lê brand-profile.json do cliente e produz visuais coerentes com a marca, idioma e nicho. Acompanha sempre preview.html pra aprovação humana antes de publicar.
---

# 🎨 creative-factory — Fábrica de Criativos via fal.ai

> Skill global do ecossistema. Atende todos os clientes da agência (Floor to Ceiling, JRS, Mendes, Ballarin, Alex SSCIA) via brand-profile.json carregado dinamicamente.

## Quando usar

- ✅ Gerar carrossel diário (5 slides) por cliente
- ✅ Gerar batch de criativos pra Meta Ads (variações pra teste)
- ✅ Gerar imagem única pra GMB / single post
- ✅ Re-gerar variantes de um slide específico
- ❌ Vídeos curtos → use `viral-video-factory`
- ❌ HTML→PNG via Chrome headless → use `carousel-generator` (fluxo NEXUS-001 pro Alex)

## Arquitetura

```
~/.claude/skills/creative-factory/
├── SKILL.md                       (este arquivo)
├── core/
│   ├── fal_client.py              gateway fal.ai (submit, retry, error handling)
│   ├── brand_loader.py            lê brand-profile.json + company.md do cliente
│   ├── prompt_builder.py          combina template + brand → prompt final
│   └── preview.py                 gera preview.html (regra do ecossistema)
├── models/
│   └── catalog.md                 quando usar Flux Dev vs Pro vs Ideogram vs Nano Banana
├── templates/
│   ├── carousel/                  templates por nicho (cleaning, hardwood, imobiliario, alex)
│   ├── ads/                       pattern interrupt, before/after estático, UGC style
│   └── single/                    GMB post, single feed
├── pipelines/
│   ├── carousel_daily.py          pipeline ponta-a-ponta: brief → 5 imgs → preview
│   ├── ad_batch.py                batch com variações pra teste de criativo
│   └── single_image.py            1 imagem standalone
└── checklists/
    └── pre-publish-visual.md      checklist obrigatório antes de publicar
```

## Fluxo padrão

```
1. NEXUS recebe demanda do operador
2. Squad conteudo-viral chama: pipelines/carousel_daily.py
3. carousel_daily.py:
   a. brand_loader → lê brand-profile.json do cliente atual
   b. valida placeholders não-substituídos (failsafe)
   c. carrega template (ex: cleaning_before_after.md)
   d. pra cada slide: prompt_builder → fal_client.submit
   e. paralelismo: até 5 slides em flight ao mesmo tempo
   f. salva imagens em <client>/squads/conteudo-viral/output/criativos/<YYYY-MM-DD>/
   g. gera preview.html com os 5 slides + caption
4. AUDITOR (NEXUS) confere coerência (brand, geo, idioma)
5. Operador aprova preview → ghl-publisher publica
```

## Configuração

**Credencial fal.ai:** `~/.claude/.env` (chmod 600), variável `FAL_KEY`. Carregada automaticamente via `python-dotenv`.

**Conta fal.ai:** global ({{EMAIL_OPERADOR}}). Operador cobra clientes via fee — fal.ai não tem multi-account separation por enquanto.

## Modelos default (override via brand-profile.json)

| Uso | Modelo default | Custo aproximado |
|---|---|---|
| Carrossel orgânico | `fal-ai/flux/dev` | $0.025/img |
| Ad com texto na imagem | `fal-ai/ideogram/v3` | $0.08/img |
| Ad alta conversão / realismo | `fal-ai/flux/v1.1-pro` | $0.04/img |
| Mascote/personagem consistente | `fal-ai/nano-banana/edit` | $0.039/img |
| Vetor/ilustração de marca | `fal-ai/recraft/v3` | $0.04/img |

Cada cliente pode override em `creative_factory_defaults` do brand-profile.json.

## Princípios

1. **Sempre preview HTML antes de publicar** (regra do ecossistema, [memória](feedback_preview_html_obrigatorio.md))
2. **Brand profile é fonte da verdade** — cores, voz, geo, idioma sempre vêm dele
3. **Negative prompt nunca vazio** pra ad/orgânico — sempre pelo menos "no watermark, no text artifacts"
4. **Output isolado por cliente** — nunca cruza pastas
5. **Preserva originals** — gera versões em pasta com timestamp, nunca sobrescreve
6. **Falha rápido em placeholder** — se brand-profile.json tem `{{X}}` não substituído, aborta

## Uso rápido

```bash
# Gerar carrossel pro Floor to Ceiling
python3 ~/.claude/skills/creative-factory/pipelines/carousel_daily.py \
  --client $PROJECTS_ROOT/FLOOR_TO_CEILING \
  --template cleaning_before_after \
  --brief "Deep cleaning before spring — Mount Laurel + Cherry Hill"
```

## Status (2026-05-02)

- ✅ Estrutura completa
- ✅ fal_client.py com 5 modelos suportados
- ✅ brand_loader.py com validação de placeholder
- ✅ Pipeline carousel_daily.py
- ⏳ Templates: cleaning ✅ / hardwood ⏳ / imobiliario ⏳ / alex ⏳
- ⏳ Smoke test pendente (aguardando saldo fal.ai)
