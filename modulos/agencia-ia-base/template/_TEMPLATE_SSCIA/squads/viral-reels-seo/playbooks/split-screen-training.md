# Playbook — Split-screen training (Grupo B' autoridade — exclusivo)

Sub-playbook de `viral-reels-seo`. **Caso-a-caso**. Não automatizado.

## Quando usar

- Cliente: Grupo B' (autoridade pt-BR) exclusivo.
- `content_engine.sub_playbook == "mixed"`.
- Operador decide manualmente que esse reel é split-screen.

## Layout

9:16 vertical dividido 50/50 horizontal:
- A-roll top (50%): cliente talking-head
- B-roll bottom (50%): asset visual

## Produção A-roll (3 modos)

### Modo 1: Real footage (recomendado)
Cliente grava no celular vertical 9:16, 15-30s, talking-head com luz boa.
- Sobe arquivo em `squads/viral-reels-seo/output/<date>/<reel-id>/a-roll-input.mp4`
- Squad video-editor recebe e processa.

### Modo 2: Soul 2.0 (quando autorizado)
Avatar Higgsfield treinado para o cliente. Custo: ~50cr treino + 12cr/reel.
- Status: aguarda autorização do cliente para ativar.

### Modo 3: Voice cloning + ator stock (último recurso)
- Voz clonada do cliente via ElevenLabs (só se o cliente autorizar).
- Ator stock genérico (ator AI sem identidade do cliente).
- Risco compliance — só para aspiracional, não testemunhal.

## Produção B-roll (mix)

- **Screen recording** (free): macOS screen capture das ferramentas/plataformas do cliente.
- **Slide rendered** (livre): squad design renderiza markdown→HTML→PNG.
- **B-roll Higgsfield** (custo): Kling 3.0 para cenas tipo "hands typing", "notebook open".

## Pipeline (manual)

1. SPLIT roteiriza A-roll + B-roll segundo a segundo.
2. Operador decide modo A-roll (real/soul/stock).
3. Se Modo 1: cliente grava e sobe.
4. Se Modo 2/3: skill higgsfield-content + elevenlabs-tts geram material.
5. Squad **video-editor** monta o split final (composição vertical + sync áudio).
6. Push pro worker (mesmo flow do dop-7s-reel).

## Custo estimado

- Modo 1 (real): ~0 cr (apenas tempo de gravação) + 5 cr B-roll Higgsfield + custo squad video-editor RunComfy (~$1).
- Modo 2 (Soul 2.0): ~12cr A-roll + 5cr B-roll = 17 cr/reel (depois do treino inicial).
- Modo 3 (stock + voice): ~12cr A-roll + 5cr B-roll = 17 cr/reel + custos ElevenLabs ($0.15).

## Output

`squads/viral-reels-seo/output/<date>/<reel-id>/split-screen/`:
- `script.md`
- `a-roll/` (mp4 ou prompt)
- `b-roll/` (assets)
- `final.mp4` (montado pela squad video-editor)
- `caption.md`
- `manifest.json`
