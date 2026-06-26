# Task — briefing (step 1)

## Owner

CINE (chief).

## Input

Operador do cliente (Vinicius pro Ballarin, Lilian pro Investbens) traz tema da semana.

## Saída

`squads/cinematic-content/output/<date>/_briefing.md`:

```markdown
# Briefing — {{CLIENTE_NOME}} — semana <YYYY-WW>

## Tema
<o que vamos mostrar essa semana>

## Vídeos planejados (3)
1. [Hero] <descrição>
2. [Lifestyle interno] <descrição>
3. [Lifestyle externo OU área comum] <descrição>

## Imagens planejadas (5)
1-5. <listagem>

## Notas operacionais
- Restrições especiais (eventos, datas, condições temporárias)
- Mudanças no brand-profile desde a última semana

## Aprovação prévia
- [ ] Operador validou tema antes de gerar
```

## Checklist

- [ ] Lido `_opensquad/_memory/brand-profile.json` (especialmente `content_engine`, `brand.products`, `geo`, `voice`, `audience`)
- [ ] Verificado `content_engine.group == "A"` (se não, abortar e redirecionar pro squad correto)
- [ ] Confirmado calendário/temas com operador antes de iniciar geração (custos significativos)
- [ ] Conferido saldo Higgsfield disponível
