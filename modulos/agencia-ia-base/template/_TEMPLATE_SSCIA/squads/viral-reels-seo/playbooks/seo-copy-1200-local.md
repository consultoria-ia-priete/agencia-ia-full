# Playbook — SEO Copy 1.200 chars (Grupo B local en-US)

Para clientes de serviço local (en-US). INK-SEO é o agente.

## Source of truth

Toda fonte é o `brand-profile.json` do cliente. Sem inventar.

| Linha da copy | Field do brand-profile |
|---|---|
| Hook | derivado de `voice.tone` |
| Dor | `audience.pain_points` |
| Solução | `brand.differentiators` |
| Prova | `brand.years_in_business` ou `seo.competitors` |
| Geo | `geo.cities_primary` + `geo.cities_secondary` |
| Keywords | `seo.primary_keywords` + `seo.long_tail_keywords` |
| CTA | `publishing.default_cta` |
| Hashtags | `publishing.hashtags_default` + 3-5 geo extras |

## Exemplo — serviço local de limpeza (genérico)

> Substitua nomes, cidades, anos e handle pelos valores do `brand-profile.json` do cliente.

```
[hook 60ch] You deserve a clean home. Not someone else's "good enough".

[dor 130ch] Dust on the baseboards. Streaks on the granite. The kind
of clean that fades the moment guests arrive.

[solução 180ch] {{MARCA_PRINCIPAL}} does deep cleans the way you'd do
them if you had 8 hours. Eco-friendly products. Same crew every time.
We learn your home.

[prova 100ch] {{ANOS}}+ years cleaning across {{N}} towns. 200+ recurring
families. Background-checked teams.

[geo SEO] Serving {{CIDADES_PRIMARIAS}} — and growing across {{REGIAO}}.

[CTA 80ch] Free quote in 24h → DM "CLEAN" or visit {{SITE}}

[keywords spread]
  ...natural integration of seo.primary_keywords, e.g.:
  "house cleaning {{CIDADE}}", "deep clean {{REGIAO}}",
  "eco-friendly cleaners {{ESTADO}}"

[hashtags]
publishing.hashtags_default + 3-5 geo-locais
```

Total ~1.150 chars.

## Falha cedo

- Sem `geo.cities_primary` → halt + pedir operador preencher.
- Sem `publishing.default_cta` → halt.
- Copy > 1.300 chars → ECHO-POLISH trim.

## Output

`squads/viral-reels-seo/output/<date>/<reel-id>/caption.md`
