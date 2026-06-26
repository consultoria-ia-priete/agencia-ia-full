# Catálogo de modelos — fal.ai gateway

Referência rápida pra escolher modelo certo por uso. Atualizar conforme novos modelos entram em produção.

## Resumo por uso

| Uso | Modelo recomendado | ID curto | Custo |
|---|---|---|---|
| **Carrossel orgânico (cleaning, flooring, dia a dia)** | Flux Dev | `flux-dev` | $0.025/img |
| **Ad com texto on-image (CTA, headline)** | Ideogram V3 | `ideogram` | $0.080/img |
| **Ad alta conversão / fotorrealismo** | Flux 1.1 Pro | `flux-pro` | $0.040/img |
| **Mascote/personagem consistente entre slides** | Nano Banana Edit | `nano-banana` | $0.039/img |
| **Vetor / ilustração de marca** | Recraft V3 | `recraft` | $0.040/img |

## Quando NÃO usar IA generativa

- Logo do cliente → use o oficial em `_opensquad/_memory/brand-kit.md`
- Foto real do cliente / produto → mantém foto real, NÃO substitua por IA
- Antes/depois real do trabalho → real sempre vence; IA só pra topo de funil

## Detalhes por modelo

### Flux Dev (`flux-dev` → `fal-ai/flux/dev`)
**Quando:** workhorse pra orgânico. Bom prompt-following, qualidade ~ 90% do Pro a 1/2 do custo.
**Aspect:** quadrado (square_hd 1024×1024), portrait (portrait_16_9 768×1344).
**Limitações:** texto on-image fraco — pra texto, troca pra Ideogram.
**Latência típica:** 8-15s.

### Flux 1.1 Pro (`flux-pro` → `fal-ai/flux-pro/v1.1`)
**Quando:** quando o ad PRECISA chamar atenção e qualquer detalhe ruim mata conversão.
**Aspect:** todos.
**Limitações:** custo 2x do Dev. Reserve pra ads premium.

### Ideogram V3 (`ideogram` → `fal-ai/ideogram/v3`)
**Quando:** texto na imagem (CTA, headline, número grande). Fonte legível, sem artefatos.
**Aspect:** ASPECT_1_1, ASPECT_9_16, ASPECT_16_9.
**Limitações:** estilo às vezes "design polido" demais (vibe Behance) — mau pra UGC.

### Nano Banana Edit (`nano-banana` → `fal-ai/nano-banana/edit`)
**Quando:** consistência entre slides. Passa imagem(s) ref e ele re-imagina mantendo a identidade.
**Input:** `image_urls=[...]` (1 ou mais URLs públicas).
**Aspect:** sai no aspect das refs.
**Limitações:** menos criativo, mais imitativo. Bom pra continuidade visual.

### Recraft V3 (`recraft` → `fal-ai/recraft/v3`)
**Quando:** ilustração vetorial, ícones, estilo "design system". Não pra fotorrealismo.
**Limitações:** estilo bem específico. Use pra branded content que precisa de identidade gráfica.

## Custos mensais estimados (200 slides + 50 ads)

- Org. (Flux Dev): 200 × $0.025 = **$5.00**
- Ads texto (Ideogram): 30 × $0.08 = **$2.40**
- Ads premium (Flux Pro): 20 × $0.04 = **$0.80**
- **Total estimado: $8.20/mês** (5 clientes)

## Como override por cliente

No `brand-profile.json` do cliente, em `creative_factory_defaults`:

```json
{
  "image_model_organic": "flux-dev",
  "image_model_ads": "flux-pro",
  "image_model_with_text": "ideogram",
  "image_model_consistency": "nano-banana"
}
```

Cliente que faz mais conteúdo de marca pesado pode setar `image_model_organic: flux-pro` e pagar mais por slide.
