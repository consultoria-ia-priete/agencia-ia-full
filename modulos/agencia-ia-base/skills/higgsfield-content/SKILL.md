---
name: higgsfield-content
description: Engine global de geração de vídeo/imagem via MCP Higgsfield (DoP, Kling 3.0, Seedance 2.0, Veo 3.1, Nano Banana 2 2K, Soul 2.0). Serve 3 playbooks — cinematic-content (Grupo A imobiliário 30s), viral-reels-seo (Grupo B/B' reel 7s vertical), ads creatives (Meta UGC/static/carousel/TV spot). UGC reservado como stub.
---

# higgsfield-content — Engine de geração visual cross-cliente

> Multi-cliente. Padronizado pelo `_TEMPLATE_SSCIA`. Aprovação canônica via dashboard `{{SEO_WORKER_DOMAIN}}`.

## Quando usar

- Gerar **vídeo cinemático 30s** pra imóvel MCMV (Grupo A: Ballarin Sou Viver Milão, Investbens Residencial Serraria) — modelo Kling 3.0 ou Seedance 2.0.
- Gerar **imagem lifestyle 2K** pra carrossel imobiliário (Grupo A) — modelo Nano Banana 2 2K.
- Gerar **reel viral 7s vertical** (Grupo B local US: Floor to Ceiling, Mendes Flooring, JRs Flooring) ou **B-prime ConsultorIA Alex** — modelo DoP exclusivo Higgsfield.
- Gerar **creative pra Meta Ads** (clientes com `content_engine.ads_enabled: true`) — vertical 9:16, quadrado 1:1, retrato 4:5, TV spot 15s.
- (Reservado) UGC com entrevista talking-head OU UGC com B-roll + narração — stubs prontos, ativar caso-a-caso.

## Quando NÃO usar

- Carrossel de slides estáticos pro carrossel canônico do Alex 14h BRT — esse continua em `creative-factory` (fal.ai). Higgsfield-content **NÃO toca** no carrossel canon (`brand-profile.content_engine.carousel_canon: true` sinaliza intocável).
- Edição de vídeo / pós-produção / legendas / música — isso é responsabilidade da squad `video-editor` (que pode invocar a skill `video-edit` runcomfy).
- Vídeos com narração + legendas pré-renderizados (b-roll com voiceover Remotion+ElevenLabs) — esse é o domínio da skill `viral-video-factory`. Coexistem, são produtos diferentes.

## 5 mandamentos (NÃO violar)

1. **Brand-profile é a fonte de verdade.** Toda geração lê `_opensquad/_memory/brand-profile.json` do cliente. Sem brand-profile → halt.
2. **content_engine.group define o playbook.** `A` → cinematic, `B`/`B-prime` → viral-reels. Se for `null` → halt com mensagem clara.
3. **Aprovação SEMPRE via dashboard canônico.** Output da skill vai pro worker `{{SEO_WORKER_DOMAIN}}` com `status: pending`. Nunca publica direto.
4. **Grupo B raw shots: SEM rosto, ângulo canônico obrigatório.** `prompt_builder` rejeita prompt contendo `person`, `face`, `smile`, `human` quando playbook = `viral-reels-seo` E sub_playbook = `dop-7s-reel`. Ângulos válidos: `top-down`, `floor-level`, `extreme-closeup`.
5. **Audit log obrigatório.** Cada geração grava `manifest.json` com prompt completo, modelo, seed, custo em créditos, timestamp, brand-profile hash. Sem manifest → output não vai pro dashboard.

## Fluxo end-to-end

```
[Brand-profile do cliente]
        ↓
[Pipeline Python: ler brand + escolher template + montar prompt]
        ↓
[Claude (mediador) chama mcp__higgsfield__generate_video|generate_image]
        ↓
[Higgsfield retorna URL .mp4 / .jpg]
        ↓
[Pipeline: download + manifest.json + push pro /admin/queue do worker]
        ↓
[Dashboard {{SEO_WORKER_DOMAIN}} — status: pending]
        ↓
[Cliente aprova → worker publica via CRM Funnels]
```

## Arquitetura

```
~/.claude/skills/higgsfield-content/
├── SKILL.md                       (esse arquivo)
├── core/
│   ├── brand_loader.py            standalone — lê brand-profile.json + valida content_engine
│   ├── prompt_builder.py          standalone — monta prompt final a partir de template + brand
│   ├── manifest.py                standalone — grava audit log em output/<slug>/<date>/<id>/
│   └── higgsfield_helper.py       constrói payload pra Claude passar pro MCP higgsfield
├── models/
│   └── catalog.md                 quando usar DoP vs Kling vs Veo vs Nano Banana 2 + tabela de créditos
├── templates/
│   ├── cinematic/                 Grupo A — apartment_hero_30s.yaml, lifestyle_resident_30s.yaml, nano_banana_2k_image.yaml
│   ├── viral_reels/               Grupo B — dop_top_down.yaml, dop_floor_level.yaml, dop_extreme_closeup.yaml
│   ├── ads/                       Ads creatives — meta_ugc_vertical_9_16.yaml, meta_static_1_1.yaml, meta_carousel_4_5.yaml, tv_spot_15s.yaml
│   └── ugc/                       RESERVADO — interview_30s.yaml.RESERVED, broll_narration_15s.yaml.RESERVED
├── pipelines/
│   ├── generate_cinematic_video.py    CLI: --client X --template Y → constrói payload
│   ├── generate_lifestyle_image.py
│   ├── generate_viral_reel.py
│   ├── generate_ad_creative.py
│   ├── generate_ugc_interview.py      STUB (ativar caso-a-caso)
│   └── generate_ugc_broll.py          STUB (ativar caso-a-caso)
└── checklists/
    └── pre-generate.md            checklist obrigatório antes de cada execução
```

## Onde mora o output

Cada pipeline grava em **diretório do cliente** (não na skill):

```
<CLIENT_DIR>/squads/<squad-name>/output/<date>/<id>/
├── prompt.json          # prompt completo (auditável)
├── manifest.json        # modelo, seed, custo, hash brand-profile
├── output.mp4 ou .jpg   # asset gerado
├── thumbnail.jpg        # poster do vídeo (se aplicável)
└── push-payload.json    # payload final enviado ao worker /admin/queue
```

Exemplos:
- `FLOOR_TO_CEILING/squads/viral-reels-seo/output/2026-05-15/reel-001/`
- `INVESTBENS_RESIDENCIAL_SERRARIA/squads/cinematic-content/output/2026-05-16/cinematic-fachada-001/`
- `ALEX_SSCIA/squads/viral-reels-seo/output/2026-05-15/dop-mentoria-001/`

## Como invocar (do Claude)

1. **Pelo squad** (mais comum): Squad `cinematic-content` ou `viral-reels-seo` chama `python pipelines/generate_X.py --client <slug>` que retorna prompt + metadados. Claude lê o output, chama o MCP higgsfield, recebe URL, e o pipeline finaliza (download + manifest + push pro worker).

2. **Direto pra teste**:
```bash
python ~/.claude/skills/higgsfield-content/pipelines/generate_viral_reel.py \
  --client floor-to-ceiling \
  --template dop_top_down \
  --subject "vacuum on plush carpet" \
  --dry-run
```
Sem `--dry-run`, o pipeline também emite o payload mas aguarda Claude executar a chamada MCP.

## Authentication

MCP Higgsfield em `~/Documents/PROJETOS_CLAUDE_CODE/_TEMPLATE_SSCIA/.mcp.json` + nos 5 clientes (URL `https://mcp.higgsfield.ai/mcp`, OAuth).

- Plano Higgsfield: Alex assina até EOD 2026-05-14.
- Primeiro tool call do Higgsfield em qualquer sessão dispara OAuth via browser.
- `core/higgsfield_helper.py` valida via teste de chamada antes de executar batch grande — falha clara se OAuth expirou.

## Dependências externas

| Recurso | Onde está | Status |
|---|---|---|
| MCP Higgsfield | `https://mcp.higgsfield.ai/mcp` (OAuth) | Configurado, aguarda assinatura Alex |
| Brand-profiles dos 6 clientes | `<CLIENT>/_opensquad/_memory/brand-profile.json` | Todos atualizados com `content_engine` |
| Worker dashboard | `{{SEO_WORKER_DOMAIN}}/admin/queue` | Live (vai precisar Fase 4 pra aceitar mp4) |

## Squads consumidores

| Squad | Pipeline usado |
|---|---|
| `cinematic-content` (Grupo A) | `generate_cinematic_video.py`, `generate_lifestyle_image.py` |
| `viral-reels-seo` (Grupo B + B') | `generate_viral_reel.py`, eventualmente `generate_ugc_broll.py` |
| `meta-ads-copy` (UPGRADE) | `generate_ad_creative.py` |
| `video-editor` (downstream) | Recebe output e polish (legenda + music + grade) |

## Status

- 2026-05-14: Estrutura criada. Core/templates/pipelines implementados. Smoke test pendente até Alex assinar Higgsfield.
- ⏳ Voice cloning Alex (ElevenLabs) pra ativar UGC B-roll do ConsultorIA — pendente.
- ⏳ Confirmar nomes exatos das tools MCP Higgsfield (`mcp__higgsfield__generate_video` esperado, mas pode variar) no primeiro boot.
