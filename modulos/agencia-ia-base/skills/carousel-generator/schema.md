# 📐 Schema JSON — Carrossel ConsultorIA

Cada carrossel é descrito por um JSON. O generator Python lê esse JSON e produz 8 HTMLs prontos pra render→JPEG→upload→publicação.

## Estrutura raiz

```json
{
  "id": "C11",
  "data_publicacao": "2026-04-26",
  "slot_brt": "12h00",
  "tema": "Por que CNPJ paga em 15 dias e CPF demora 3 meses",
  "pilar": "educacao_mercado",
  "variant": "DARK",
  "palavra_gatilho": "CNPJ",
  "tem_seeding_crm_funnels": false,
  "caption": "...texto completo da caption...",
  "slides": [ ... 8 objetos ... ]
}
```

### Campos da raiz
| Campo | Tipo | Valores |
|---|---|---|
| `id` | string | Código (C11, C12...) |
| `data_publicacao` | string | YYYY-MM-DD |
| `slot_brt` | string | "12h00" \| "18h00" \| "21h00" |
| `tema` | string | Tema da peça (referência interna) |
| `pilar` | string | "provocacao" \| "educacao_tecnica" \| "educacao_mercado" \| "prova_social" \| "bastidor" \| "reframe" |
| `variant` | string | "DARK" \| "LIGHT" \| "GREEN" |
| `palavra_gatilho` | string | UPPERCASE única (ex: "CNPJ", "MODELO") |
| `tem_seeding_crm_funnels` | bool | Se true, slide 7 usa tipo "seeding" |
| `caption` | string | Caption multilinha, última linha sempre o CTA padrão |
| `slides` | array[8] | Os 8 slides |

## Tipos de slide

Cada slide tem `tipo` que define o template. Campos variam por tipo.

### `capa` (slide 1)
```json
{
  "tipo": "capa",
  "eyebrow": "A LÓGICA DO MERCADO",
  "hook": "Por que <verde>CNPJ</verde> fecha em <verde>15 dias</verde>",
  "subtitle": "E CPF demora 3 meses pra decidir."
}
```
- `eyebrow`: label uppercase com tracinho
- `hook`: título grande, suporta tags `<verde>...</verde>` (em DARK), `<highlight>...</highlight>` (LIGHT/GREEN), `<black>...</black>` (LIGHT) e `<black-block>...</black-block>` (GREEN, retângulo preto com verde)
- `subtitle`: texto cinza dim opcional

### `body` (texto narrativo)
```json
{
  "tipo": "body",
  "eyebrow": "A REGRA DO CNPJ",
  "hook": "Pensa <verde>comigo</verde>.",
  "paragraphs": [
    "Os gurus que vendem afiliação <verde>ganham vendendo o curso</verde>.",
    "Não fazendo afiliação."
  ]
}
```

### `lista` (lista com diamonds)
```json
{
  "tipo": "lista",
  "eyebrow": "QUEM ESTÁ PROCURANDO",
  "hook": "Olha quem <verde>procura agora</verde>:",
  "items": [
    "Dono de clínica, oficina, e-commerce, advocacia",
    "Operação travada, equipe enxuta",
    "Margem caindo todo mês",
    "Concorrência já usando IA"
  ],
  "closing": "Ele <highlight>sabe</highlight> que precisa. Não sabe o que fazer."
}
```

### `metrics` (automação com tabela)
```json
{
  "tipo": "metrics",
  "tag": "// AUTOMAÇÃO 02",
  "hook": "Triagem e classificação de leads",
  "desc": "IA lê leads que entram, classifica por temperatura.",
  "metrics": [
    {"label": "Setup", "val": "6 horas"},
    {"label": "Conversão", "val": "+25 a 40%", "highlight": true},
    {"label": "Stack", "val": "CRM Funnels + Claude Code"}
  ]
}
```
- `highlight: true` em uma métrica = destaque verde no valor

### `dados` (estatísticas em box terminal)
```json
{
  "tipo": "dados",
  "eyebrow": "O TAMANHO DO MERCADO",
  "hook": "O Brasil tem:",
  "rows": [
    {"num": "21 milhões", "label": "CNPJs ativos"},
    {"num": "6,5 milhões", "label": "com R$ 360K+/ano"},
    {"num": "< 1%", "label": "usando IA na operação"},
    {"num": "+38% / ano", "label": "de demanda"}
  ],
  "source": "// fonte: SEBRAE + FGV (2026)"
}
```

### `climax` (slide 7 punchline)
```json
{
  "tipo": "climax",
  "eyebrow": "A CONTA FECHA",
  "lines": [
    "<highlight>1 SEMANA</highlight>.",
    "<black-highlight>R$ 1.500/MÊS</black-highlight>.",
    "<highlight>RECORRENTE</highlight>."
  ],
  "subtitle": "É o que separa o consultor do curioso."
}
```

### `seeding` (slide 7 quando carrossel é o "1 em 3" do CRM Funnels)
```json
{
  "tipo": "seeding",
  "eyebrow": "A CONTA FECHA",
  "lines": [
    "<highlight>1 SEMANA</highlight>.",
    "<black-highlight>R$ 1.500/MÊS</black-highlight>.",
    "<highlight>RECORRENTE</highlight>."
  ],
  "subtitle": "É o modelo que eu vivo todo mês."
}
```
- Sempre adiciona o box "MEU SAAS · CRM Funnels · Toda minha entrega é vinculada a uma assinatura."
- NÃO inclui URL/link (regra de seeding, não venda)

### `cta` (slide 8)
```json
{
  "tipo": "cta",
  "comenta_word": "CNPJ",
  "payoff_pre": "e eu te mando o link do meu",
  "payoff_highlight": "Treinamento Grátis",
  "payoff_post": "de como criar sua ConsultorIA."
}
```

## Tags de inline highlighting

Dentro de `hook`, `subtitle`, `lines` etc. você pode usar:

| Tag | DARK | LIGHT | GREEN |
|---|---|---|---|
| `<verde>X</verde>` | texto verde sólido `#8FDF65` | n/a (use highlight) | n/a (use black-block) |
| `<highlight>X</highlight>` | n/a | retângulo verde com texto preto | retângulo verde com texto preto |
| `<black>X</black>` | n/a | retângulo preto com texto branco | n/a |
| `<black-block>X</black-block>` | n/a | n/a | retângulo preto com texto verde |
| `<black-highlight>X</black-highlight>` | n/a | retângulo preto com texto verde | n/a |
| `<strike>X</strike>` | strikethrough cinza | strikethrough cinza claro | strikethrough cinza escuro |

O generator escolhe a renderização CSS correta baseado em `variant` da raiz.

## Validações automáticas (do generator)
- ✅ Exatamente 8 slides
- ✅ Slide 1 deve ser `capa`, slide 8 deve ser `cta`
- ✅ Se `tem_seeding_crm_funnels: true`, slide 7 deve ser `seeding`
- ✅ `palavra_gatilho` aparece literalmente no slide 8 (`comenta_word`)
- ✅ `caption` termina com formula CTA padrão
