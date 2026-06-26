# Playbook — Authority Copy 1.200 chars (Grupo B' autoridade pt-BR)

Para cliente Grupo B' (autoridade/infoproduto pt-BR). INK-AUTHORITY é o agente.

## Source of truth

Toda fonte é o `brand-profile.json` do cliente. Sem inventar.

| Linha da copy | Field do brand-profile |
|---|---|
| Hook | derivado de `voice.tone` + ângulo da semana |
| Reconhecimento do avatar | `audience` (dor/desejo do avatar) |
| Mecânica/argumento | `offer.mechanism` / `brand.differentiators` |
| Promessa | `offer.promise` / `audience.desired_outcome` |
| Prova | `brand.proof` / `brand.community` |
| CTA | variação de `publishing.cta` |
| Hashtags | `publishing.hashtags_default` |

Regras de voz e compliance (vocabulário aprovado/evitado, anti-dicotomia, temas internos vs públicos, marcas que não podem aparecer): tudo vem do brand-profile do cliente.

## Estrutura

```
[hook 60ch] Estilo direto. Pergunta provocadora ou contra-intuitiva.
            Puxar do ângulo da semana + voice.tone.

[reconhecimento avatar 130ch] Reconhecer dor/desejo do avatar (audience).
                              Sem dramatizar excessivamente.

[mecânica 200ch] Usar offer.mechanism / brand.differentiators.
                 Citar a promessa do cliente só se o brand-profile autorizar.

[prova 150ch] brand.proof / brand.community. Direto, sem hype.

[CTA — 1 variação de publishing.cta]

[hashtags pt-BR do nicho]
```

Total ~1.150 chars.

## Compliance checklist

- [ ] Sem palavrões / baixo calão
- [ ] Regras de voz do brand-profile respeitadas (vocabulário aprovado/evitado)
- [ ] Regras de compliance do brand-profile respeitadas (anti-dicotomia, temas internos vs públicos, etc.)
- [ ] Marcas/ferramentas internas não autorizadas NÃO aparecem
- [ ] CTA usa **uma única** variação de `publishing.cta`
- [ ] Promessa coerente com o que o brand-profile autoriza (não inventar números)

## Output

`squads/viral-reels-seo/output/<date>/<reel-id>/caption.md`
