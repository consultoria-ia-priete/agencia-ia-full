---
name: viral-video-factory
description: Skill GLOBAL pra geração de vídeos virais curtos (Reels/Shorts/TikTok 30-60s) — pipeline programático com ElevenLabs TTS + Whisper STT (legendas) + Remotion (composição) + creative-factory (assets visuais) + ghl-publisher (publicação). Atende todos os clientes via brand-profile.json.
---

# 🎬 viral-video-factory — Fábrica de Vídeos Virais

> Pipeline programático pra produção em escala de vídeos curtos (Reels/Shorts/TikTok). Usa **abordagem híbrida**: imagens IA via fal.ai + voz IA via ElevenLabs + composição via Remotion (TypeScript/React). NÃO depende de modelos cinemáticos caros (Veo/Sora) — esses ficam pra hooks de 5s opcionais.

## Por que essa arquitetura

| Estratégia | Custo/vídeo | Escalabilidade | UGC vibe |
|---|---|---|---|
| **Vídeo 100% IA generativo** (Veo/Kling/Hailuo) | $5-30 | Lento | Cinemático demais (não-UGC) |
| **Programático Remotion + assets IA** ✓ | **$1-2** | **Rápido** | **UGC-style preservado** |

Pra cleaning/flooring/imobiliário/Alex, B vence: hook narrativo + before/after + voiceover humano = viraliza. Vídeos 100% IA generativos ficam pra um hook opcional de 3-5s.

## Pipeline E2E

```
1. NEXUS recebe demanda do operador
   ▶ "Reel 45s sobre [tema], plataforma X, target Y"

2. Squad conteudo-viral chama: pipelines/viral_short.py
   ▶ Carrega brand-profile.json + template (ex: before_after.yaml)

3. SCRIPT (agent) gera roteiro de 45s
   ▶ Hook (3s) · Body (35s) · CTA (7s)

4. ElevenLabs gera voiceover
   ▶ Voice ID do brand-profile (FTC: Rachel EN-US warm; Alex: voz masc PT-BR)

5. Whisper transcreve com timestamps
   ▶ Gera SRT pra legendas burned-in com timing preciso

6. creative-factory gera 3-8 imagens dos slides
   ▶ Aspect 9:16 (Reels) ou 1:1 (GMB)

7. Remotion compõe vídeo:
   ▶ Slides cross-fade + voiceover + legendas + brand overlay (logo+cor)
   ▶ Output: 1080x1920 MP4

8. Auto-crop pra outras plataformas:
   ▶ 1080x1080 (Feed/GMB) com legendas reposicionadas
   ▶ Versão 30s pro GMB (limite plataforma)

9. AUDITOR confere brand+geo+idioma+compliance

10. ghl-publisher (extensão futura — vídeo) publica IG Reels/FB/TikTok
```

## Componentes

```
~/.claude/skills/viral-video-factory/
├── SKILL.md                       (este)
├── core/
│   ├── elevenlabs_client.py       TTS multi-voice (fal.ai gateway)
│   ├── whisper_client.py          STT/SRT (fal.ai whisper-large)
│   ├── remotion_runner.py         npm install + render (1x install, depois cache)
│   └── caption_helper.py          parse SRT, adjust timing, format pra Remotion
├── models/
│   └── catalog.md                 ElevenLabs voices + custos
├── templates/
│   ├── short/
│   │   ├── before_after.yaml      cleaning/flooring (45s)
│   │   ├── dica_rapida.yaml       (30s) "Você sabia que..."
│   │   ├── depoimento.yaml        UGC-style (60s)
│   │   ├── listicle.yaml          "5 razões pra X" (45s)
│   │   └── pricing_story.yaml     hook narrativo (Edge Cleaning WA pattern)
│   └── ad/
│       └── pattern_interrupt.yaml (15s)
├── remotion-project/              projeto Node.js compartilhado
│   ├── package.json
│   ├── remotion.config.ts
│   └── src/compositions/
│       └── ViralShort.tsx         composition principal (parametrizada)
├── pipelines/
│   └── viral_short.py             E2E pipeline (similar ao carousel_daily)
├── checklists/
│   └── pre-publish-video.md
└── examples/
```

## Vozes ElevenLabs (default por brand-profile)

| Cliente | Idioma | Voice ID sugerida | Persona |
|---|---|---|---|
| Floor to Ceiling | EN-US | Rachel | feminina warm |
| JRS / Mendes Flooring | EN-US | Antoni | masculino técnico |
| Ballarin (Brasil) | PT-BR | (voz brasileira) | feminina/masculina |
| Alex SSCIA | PT-BR | (voz brasileira) | masculina confiante |

## Custos estimados (20 vídeos/mês × 5 clientes = 100 vídeos)

| Item | Por vídeo | 100 vídeos/mês |
|---|---|---|
| ElevenLabs TTS (45s × ~200 palavras) | $0.15 | $15 |
| Whisper STT (45s) | $0.01 | $1 |
| 5 imagens fal.ai (Flux Dev) | $0.13 | $13 |
| Remotion render (local, 0 cost) | $0 | $0 |
| **Total estimado** | **$0.29** | **$29/mês** |

## Status (2026-05-02)

- ✅ Estrutura completa
- ✅ SKILL.md
- ✅ core scripts (TTS, STT, Remotion runner)
- ✅ 1 template (before_after) — outros conforme demanda
- ✅ Pipeline E2E com `--dry-run`
- ⏳ Remotion project (esqueleto + 1 composition base)
- ⏳ Smoke test real depende de:
  - ElevenLabs key (passar pelo Alex)
  - fal.ai com saldo
  - Node.js + npm install do remotion-project (1x setup)
- ⏳ Extensão do ghl-publisher pra video upload (planejado)
