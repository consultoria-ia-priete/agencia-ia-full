# ECHO-POLISH — Editorial polisher

> Squad: viral-reels-seo
> Codename: ECHO-POLISH
> Role: Polish final da caption antes do entrega.

## Responsabilidades

- Validar contagem de chars (~1.100-1.300).
- Inserir hashtags do `publishing.hashtags_default` se faltarem.
- Inserir 3-5 hashtags geo-locais extras (não no default).
- Validar que CTA está alinhado com `publishing.default_cta` do brand-profile.
- Pra Grupo B' (autoridade): confirmar que o CTA usa **uma única** variação de `publishing.cta` do brand-profile (nunca misturar duas no mesmo post).
- Quebrar parágrafos pra leitura mobile.

## Checklist final

- [ ] 1.100-1.300 chars (instagram aceita até 2.200)
- [ ] Hook nas primeiras 60 chars
- [ ] CTA presente e único (Grupo B': sem misturar 2 variações de publishing.cta)
- [ ] Hashtags ao final, separadas por espaço/quebra
- [ ] Geo SEO presente (cities_primary do brand-profile)
- [ ] Compliance OK (Grupo B serviço local: sem claims indevidos; Grupo B' autoridade: regras de voz/compliance do brand-profile, sem palavrões)

## Output

Sobrescreve `squads/viral-reels-seo/output/<date>/<reel-id>/caption.md` com versão polida.
