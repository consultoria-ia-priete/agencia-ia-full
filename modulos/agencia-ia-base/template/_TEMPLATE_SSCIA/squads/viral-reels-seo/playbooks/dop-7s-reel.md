# Playbook — DoP 7s Reel (Grupo B + B')

Sub-playbook canônico do `viral-reels-seo`. Usado por padrão.

## Quando usar

- Sub-playbook `dop-7s-reel` (clientes B locais, serviço local) — sempre.
- Sub-playbook `mixed` (Grupo B' autoridade) — quando reel for raw shot puro (sem split-screen).

## 5 princípios INVIOLÁVEIS

Os mesmos que validam automaticamente em `prompt_builder.py`:

### 1. Câmera NO produto/processo, NUNCA no rosto
Validator `no_face_no_person` bloqueia se prompt contém `face`, `smile`, `person standing`, etc (ignora negações tipo "no face").

### 2. Ângulo incomum obrigatório
Validator `dop_valid_angle` requer 1 dos 3:
- `top-down aerial` / `top-down`
- `floor-level POV` / `floor-level`
- `extreme close-up` / `extreme-closeup`

### 3. Gesto autêntico de trabalho real
- ✓ "moving in rhythmic lines", "applying oil finish in long strokes", "buffing with cloth"
- ✗ "posing", "showing the camera", "demonstrating"

### 4. Texto sobreposto opcional, máx 6 palavras
Squad video-editor materializa. Exemplos válidos:
- "You deserve a clean home"
- "This floor deserved better"
- "Before someone else sees first"

### 5. Copy 1.200 chars faz o SEO + conversão
Squad delega pra INK-SEO (Grupo B local) ou INK-AUTHORITY (Grupo B' autoridade).

## Templates Higgsfield

- `dop_top_down.yaml` (12cr)
- `dop_floor_level.yaml` (12cr)
- `dop_extreme_closeup.yaml` (12cr)

## Comando padrão

```bash
python ~/.claude/skills/higgsfield-content/pipelines/generate_viral_reel.py \
  --client <slug> \
  --template <dop_top_down|dop_floor_level|dop_extreme_closeup> \
  --param subject="<the WHAT>" \
  --param action="<the HOW — rhythmic/deliberate/satisfying motion>"
```

## Falha cedo

Se prompt_builder rejeita por violação dos 5 princípios → reescrever subject/action sem mencionar rosto. NÃO bypassar.
