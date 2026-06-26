# 🎨 carousel-generator — Skill de geração de HTMLs de carrossel a partir de JSON

> Recebe um JSON estruturado descrevendo 1 carrossel (tema, variante de cor, 8 slides, caption) e produz os 8 HTMLs prontos pra render→JPEG→upload→publicação.
>
> Validado em produção contra os C08/C09/C10 publicados em 2026-04-25.

---

## 🎯 Quando usar

- Pipeline diário automatizado de geração de carrosséis (Fase 2 do plano NEXUS)
- Reprodução em batch de carrosséis a partir de roteiros JSON
- Eliminar a necessidade de escrever HTMLs à mão
- Garantir consistência absoluta com a Diretiva NEXUS-001 v2

---

## ⚡ Uso rápido

```bash
python3 ~/.claude/skills/carousel-generator/generate.py \
  caminho/do/carousel.json \
  caminho/da/pasta/output/
```

> **Nota:** desde 2026-05-02 esta skill é **global** (`~/.claude/skills/carousel-generator/`). Funciona pra qualquer cliente — basta apontar o JSON do carrossel e a pasta de output. O `_TEMPLATE_SSCIA` e os symlinks dos clientes apontam pra esta versão única.

O generator vai:
1. Validar o JSON contra o schema (8 slides, tipos válidos, palavra-gatilho coerente, etc.)
2. Renderizar 8 HTMLs (`<id>-slide-01.html` a `<id>-slide-08.html`)
3. Cada HTML é autocontido (CSS inline, fontes locais via `@font-face`)

A partir daí, usa o pipeline já existente:
- Chrome headless renderiza HTML → PNG (`--window-size=1080,1440`)
- `sips` converte PNG → JPEG
- Skill `ghl-publisher` faz upload + publicação

---

## 📋 Schema JSON

Documentação completa em [`schema.md`](schema.md). Em resumo:

```json
{
  "id": "C11",
  "data_publicacao": "2026-04-26",
  "slot_brt": "12h00",
  "tema": "...",
  "pilar": "educacao_mercado",
  "variant": "DARK | LIGHT | GREEN",
  "palavra_gatilho": "CNPJ",
  "tem_seeding_crm_funnels": false,
  "caption": "...última linha = CTA padrão...",
  "slides": [ ...8 objetos... ]
}
```

### 7 tipos de slide
1. **`capa`** — eyebrow + hook grande + subtitle (slide 1)
2. **`body`** — eyebrow + hook + parágrafos
3. **`lista`** — eyebrow + hook + lista de items com diamonds
4. **`metrics`** — tag + título + descrição + tabela Setup/Conversão/Stack
5. **`dados`** — eyebrow + hook + box terminal com estatísticas
6. **`climax`** — eyebrow + 3 linhas de impacto com highlights (slide 7 padrão)
7. **`seeding`** — climax + box CRM Funnels (slide 7 quando "1 em 3" da regra Diretiva §8)
8. **`cta`** — Comenta + palavra grande + payoff Treinamento Grátis (slide 8)

### Tags inline para highlight
Dentro de `hook`, `subtitle`, `paragraphs`, `items`, `lines`, `closing`:
- `<verde>X</verde>` · `<highlight>X</highlight>` · `<black>X</black>` · `<black-block>X</black-block>` · `<black-highlight>X</black-highlight>` · `<strike>X</strike>`

O generator escolhe o CSS correto baseado na `variant` raiz (DARK/LIGHT/GREEN). Veja [`schema.md`](schema.md) para tabela completa.

---

## 📂 Arquivos

```
carousel-generator/
├── SKILL.md           ← este arquivo
├── schema.md          ← schema JSON completo + exemplos por tipo de slide
├── generate.py        ← entrypoint (CLI)
├── _slides.py         ← funções renderizadoras dos 7 tipos
├── _styles.py         ← CSS base + paleta de cores por variant + helpers
└── examples/
    └── C09.json       ← roteiro completo do C09 (validação pixel-perfect)
```

---

## ✅ Validações automáticas

O generator rejeita JSONs inválidos com:
- Campos obrigatórios faltando na raiz
- `variant` ≠ DARK/LIGHT/GREEN
- ≠ 8 slides
- Slide 1 ≠ tipo `capa`
- Slide 8 ≠ tipo `cta`
- `tem_seeding_crm_funnels: true` mas slide 7 ≠ `seeding`
- `palavra_gatilho` (raiz) ≠ `comenta_word` (slide CTA)

---

## 🧬 Próximas fases do pipeline (Plano NEXUS)

Esta skill é a **Fase 1** do plano de rotina diária. Próximas:

### Fase 2 — ORACLE → SCRIPT → INK → GENERATOR (em construção)
Construir o agente que:
1. **ORACLE**: escolhe 3 pautas dos 5 pilares editoriais, sem repetir tema dos últimos 14 dias, garantindo "1 em 3 leva seeding CRM Funnels"
2. **SCRIPT**: desenvolve roteiro JSON de cada uma (8 slides estruturados)
3. **INK**: escreve a caption multilinha
4. **GENERATOR**: chama esta skill com o JSON pronto

### Fase 3 — Pipeline diário com checkpoint Alex
1. launchd às 7h dispara o pipeline completo
2. Renderiza 24 HTMLs + 24 PNGs + 24 JPEGs + upload pro CDN CRM Funnels
3. Salva preview HTML consolidado em `/tmp/preview-do-dia.html`
4. Alex abre o Claude, vê preview, aprova com 1 comando
5. Aprovado → cria 3 launchd pros slots 12h/18h/21h BRT
6. Rejeitado → roda nova iteração com feedback do Alex

---

## 📜 Referências cruzadas

- [Diretiva NEXUS-001 v2](_opensquad/_memory/diretiva-nexus-001-carrossel.md) — padrão visual e regra "1 em 3"
- [Skill `ghl-publisher`](../ghl-publisher/SKILL.md) — pipeline de upload + publicação
- Templates de referência (versão manual): `squads/conteudo-viral/output/design/C{08,09,10}-*/`
