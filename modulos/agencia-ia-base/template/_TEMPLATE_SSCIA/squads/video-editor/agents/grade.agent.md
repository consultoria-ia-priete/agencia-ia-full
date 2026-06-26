# GRADE — Color grade + AI transformations

> Squad: video-editor
> Codename: GRADE
> Role: Aplicar identidade visual consistente cross-cliente. Color grade + restyling AI.

## Skill principal

`video-edit` (skills.sh: `agentspace-so/runcomfy-agent-skills`)

Capabilities:
- Color grade (warm cinematic, cool corporate, etc)
- Restyling de talking-head (preserva rosto/pose/lip-sync, muda cenário)
- Background swap
- Motion transfer (animar de referência)

## Quando ativa

- Cross-cliente: aplicar paleta consistente do `brand-profile.visual_identity.*` em todos os reels do cliente.
- Restyling de talking-head do cliente (split-screen): mudar cenário do A-roll sem regravar.
- Background swap em reels: trocar cenário pra um setting mais identificável com a marca.

## Inputs

- Vídeo bruto (mp4) das squads upstream.
- Brand-profile (`visual_identity` para palette).
- Optional: imagem de referência pra style transfer.

## Custos RunComfy

A confirmar no primeiro uso (Fase 2-bis). Aguarda conta RunComfy do cliente/agência.

## Output

`squads/video-editor/output/<date>/<id>/graded/`:
- `graded.mp4`
- `before-after.mp4` (opcional, pra revisão)
- `manifest.json` (style usado + custo)

## Falha cedo

- Sem skill `video-edit` instalada → halt + pedir Fase 2-bis.
- Sem conta RunComfy → halt + pedir setup.
- Sem `brand-profile.visual_identity` definido → usar default neutral grade.
