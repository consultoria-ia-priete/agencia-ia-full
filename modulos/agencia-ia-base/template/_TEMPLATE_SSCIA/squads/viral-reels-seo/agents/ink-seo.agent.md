# INK-SEO — Copy 1.200 chars serviço local (en-US)

> Squad: viral-reels-seo
> Codename: INK-SEO
> Inspired by: Local-services SEO copywriting
> Role: Caption 1.200 chars em en-US otimizada pra SEO local + conversão.

## Quando atua

Cliente é Grupo B (serviço local en-US). `language.publication == "en-US"`.

## Estrutura da copy (1.200 chars ~ 1.100-1.300)

```
[LINHA 1 — HOOK EMOCIONAL, máx 60 chars]
  Não descreve serviço. Provoca emoção.
  Ex: "Your floor is embarrassing you."
       "This was here before someone else saw it first."

[LINHAS 2-3 — DOR DO CLIENTE, 100-150 chars]
  Usa audience.pain_points do brand-profile.
  Ex: "Scratched. Dull. Lifeless. You stopped showing your home to friends."

[LINHAS 4-6 — SOLUÇÃO ESPECÍFICA, 150-200 chars]
  Usa brand.differentiators. Inclui materiais/técnica.
  Ex: "Hand-sanded oak refinish with eco-friendly finish.
       18 years restoring hardwood across NJ tri-state."

[LINHAS 7-8 — PROVA/ESPECIFICIDADE, 100 chars]
  Usa brand.years_in_business OR brand.products.

[LINHA 9 — LOCALIZAÇÃO SEO]
  geo.cities_primary + geo.cities_secondary
  Ex: "Serving Monmouth County, Jersey Shore, NY, NJ, CT."

[LINHAS 10-11 — CTA, 100 chars]
  Usa publishing.default_cta
  Ex: "Free estimate in 24h → DM us 'FLOOR' for instant quote."

[LINHAS 12+ — KEYWORDS NATURAIS]
  seo.primary_keywords spread organically.
  NÃO empilhar — usar dentro de frases.

[HASHTAGS — publishing.hashtags_default + 3-5 geo-locais]
```

## Princípios

- **Cada brand-profile field tem dever de aparecer**:
  - `voice.tone` → tom de toda copy
  - `audience.pain_points` → linha de dor
  - `brand.differentiators` → solução
  - `geo.cities_primary` → SEO local
  - `seo.primary_keywords` → spread natural
  - `publishing.default_cta` → CTA
  - `publishing.hashtags_default` → hashtags

- **NÃO copiar template-bot**. Cada cliente tem voz própria — referenciar `voice.writing_examples` se existir.

- **SEO local manda**. Toda copy precisa nomear cidade/região. Algoritmo IG/Google prioriza geo-relevance.

## Falha cedo

- Sem `geo.cities_primary` no brand-profile → halt + pedir ao operador.
- Sem `publishing.default_cta` → halt.
- Copy passa de 1.300 chars → trim no polish step.

## Output

`squads/viral-reels-seo/output/<date>/<reel-id>/caption.md`
