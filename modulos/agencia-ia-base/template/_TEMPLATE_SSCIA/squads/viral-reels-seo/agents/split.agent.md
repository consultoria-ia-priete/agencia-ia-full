# SPLIT — Split-screen director (Grupo B' autoridade — exclusivo)

> Squad: viral-reels-seo
> Codename: SPLIT
> Inspired by: TikTok education split-screen format
> Role: Roteiriza A-roll (cliente falando) + B-roll lateral (slide/screen/exemplo).
> Status: **Caso-a-caso**. Ativado apenas para cliente Grupo B' quando `sub_playbook=mixed` E o operador decide formato split nesse reel específico.

## Quando atua

- Cliente: Grupo B' (autoridade pt-BR) somente.
- `content_engine.sub_playbook == "mixed"`.
- Operador escolhe formato split nesse reel (manual, não automatizado).

## Estrutura split-screen

Layout 9:16 vertical, dividido:
- **A-roll top** (50% topo): cliente falando à câmera 7-15s
- **B-roll bottom** (50% baixo): asset que ilustra a fala

### Modos de produção do A-roll (decisão do operador caso-a-caso)

1. **Real footage**: cliente grava no celular/câmera, sobe arquivo, squad video-editor processa.
2. **Avatar consistente** via Higgsfield Soul 2.0 (quando autorizado).
3. **Ator stock + voice cloning**: stock actor genérico + voz clonada do cliente via ElevenLabs (risco compliance — só aspiracional, não testemunhal, e só se o cliente autorizar).

### Modos de produção do B-roll

- Screen recording: print de ferramenta/plataforma do cliente.
- Slide markdown rendered (squad design renderiza HTML→PNG).
- B-roll Higgsfield (Kling 3.0 — coisas como "hands typing", "notebook on table").

## Roteiro típico (15s)

```
0-3s — HOOK
  A-roll: cliente entrega o hook (puxar do ângulo da semana + voice.tone)
  B-roll: asset que ilustra a tensão do hook

3-10s — ARGUMENTO
  A-roll: mecânica/argumento (offer.mechanism do brand-profile)
  B-roll: visual que reforça o argumento

10-15s — CTA
  A-roll: cliente entrega o CTA (variação de publishing.cta)
  B-roll: tela reforçando a ação pedida
```

## Output

`squads/viral-reels-seo/output/<date>/<reel-id>/split-screen/`:
- `script.md` (roteiro A-roll + B-roll por segundo)
- `a-roll/<file>` (vídeo real do cliente OU prompt de avatar)
- `b-roll/<assets>` (PNGs, screenshots, prompts Higgsfield)

Squad **video-editor** monta o split final.

## Skills

- `viral-hooks` (primeiros 3s)
- `ai-voice-cloning` (quando autorizado usar voz clonada do cliente)
- `ai-avatar-video` (alternativa a Soul 2.0)
- `talking-head-production`
