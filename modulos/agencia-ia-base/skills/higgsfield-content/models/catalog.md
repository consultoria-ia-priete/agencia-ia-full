# Higgsfield — Catálogo de modelos

Última atualização: 2026-05-14.
Source: memória `_opensquad/_memory/skills-disponiveis.md` + endpoint `https://mcp.higgsfield.ai/mcp`.

## Vídeo

| Modelo | Identificador (this skill) | Créditos por vídeo | Duração ideal | Quando usar |
|---|---|---|---|---|
| **DoP** (Director of Photography) | `dop` | **12** | 5-7s | Grupo B raw shots — viral reels SEO. Câmera no produto/processo, sem rosto, ângulo incomum. Exclusivo Higgsfield. |
| **Kling 3.0** | `kling-3.0` | **42** | 15-30s | Grupo A cinematic — vídeo aspiracional de empreendimento, lifestyle, hero shot. Movimento de câmera suave. |
| **Seedance 2.0** | `seedance-2.0` | **42** | 15-30s | Alternativa ao Kling — bom pra cenas com character identity consistente. |
| **Veo 3.1** | `veo-3.1` | **50** | 8-15s | Premium — TV spots, ads brand-awareness alta produção. Melhor coerência temporal/física. |
| **Sora 2** | `sora-2` | **60** | até 60s | Top-of-line — usar com critério. Maior custo. |

### Quando escolher qual vídeo

- **Reel viral SEO 7s** (Grupo B + B'): `dop` — não há substituto. Princípios viralizados (câmera no produto, sem rosto) são nativos do DoP.
- **Cinematic 30s imobiliário** (Grupo A): `kling-3.0` default. Sobe pra `veo-3.1` se quiser fotorealismo extra.
- **Ad video UGC 15s vertical**: `kling-3.0` (mais barato) ou `veo-3.1` (premium polish).
- **TV spot 15s 16:9**: `veo-3.1` — cinematic polish + coerência temporal.

## Imagem

| Modelo | Identificador | Créditos | Quando usar |
|---|---|---|---|
| **Nano Banana 2 2K** | `nano-banana-2k` | **2** | Default Higgsfield pra imagem. Lifestyle, single shot, carrossel. 2K resolution. |
| **Nano Banana Pro** | `nano-banana-pro` | **4** | Mais polish + character consistency leve. Pra ads onde personagem aparece em várias imagens. |
| **Flux 2** | `flux-2` | **3** | Alternativa quando Nano Banana ficar inconsistente. |

### Quando escolher qual imagem

- **Lifestyle 1:1** (Grupo A, 5/sem): `nano-banana-2k`. Default.
- **Ad estático 1:1**: `nano-banana-2k` ou `nano-banana-pro` se precisar character consistency.
- **Carrossel 4:5** (sibling slides com mesma identidade): `nano-banana-pro` (consistência > custo).

## Character / Avatar

| Modelo | Identificador | Status | Notas |
|---|---|---|---|
| **Soul 2.0** | `soul-2.0` | **Reservado** | Avatar Alex consistente. NÃO TREINAR ainda (decisão Alex 2026-05-14). Quando ativar: ~50 créditos de treino + ~12 créditos por reel com avatar. |

## Estimativa de custo cross-cliente (cadência semanal)

| Cliente | Grupo | Vídeos × créditos | Imagens × créditos | Total/sem |
|---|---|---|---|---|
| ballarin-sou-viver-milao | A | 3 × 42 = 126 | 5 × 2 = 10 | **136** |
| investbens-residencial-serraria | A | 3 × 42 = 126 | 5 × 2 = 10 | **136** |
| floor-to-ceiling | B | 1 × 12 = 12 | 0 | **12** |
| mendes-flooring | B | 1 × 12 = 12 | 0 | **12** |
| jrs-flooring | B | 1 × 12 = 12 | 0 | **12** |
| alex-sscia | B-prime | 1-2 × 12 = 12-24 | 0 | **12-24** |
| **Total orgânico/sem** | | | | **~320 créditos** |

Ads creatives: ~10-20 créditos extra por batch (on-demand, sem cadência fixa).

## Aspect ratios suportados

| Aspect | Onde usa | Modelos |
|---|---|---|
| `9:16` | Reels, Stories, TikTok, vídeo cinematic vertical | Todos |
| `1:1` | Carrossel orgânico, ad estático feed | Imagem |
| `4:5` | Carrossel ads (mais altura no feed) | Imagem |
| `16:9` | TV spot, YouTube | Todos |
| `3:4` | Carrossel ConsultorIA (canon Alex 14h BRT) | Imagem |

## Skills companheiras (instaladas globalmente)

- `viral-video-factory` — produto **diferente** (Remotion + ElevenLabs + fal.ai) pra reels com voiceover+legendas. Coexiste.
- `video-edit` (skills.sh/runcomfy) — pós-produção AI (color grade, restyling, motion transfer). Usada pela squad video-editor.
- `elevenlabs-tts` / `elevenlabs-stt` — voiceover (UGC B-roll quando ativar) + legendas.
- `elevenlabs-music` / `ai-music-generation` — trilha (squad video-editor).
- `ai-voice-cloning` — clone da voz do Alex (pendente, pra UGC B-roll ConsultorIA).
- `ai-avatar-video` / `talking-head-production` — alternativas a Soul 2.0 pra UGC entrevista.

## Auth / OAuth

MCP em `https://mcp.higgsfield.ai/mcp` configurado em todos `.mcp.json` cliente desde 2026-04-30. Plano Higgsfield: aguarda Alex assinar (EOD 2026-05-14). Primeiro tool call dispara OAuth via browser.
