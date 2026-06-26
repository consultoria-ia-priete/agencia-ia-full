# LOGO — Watermark / logo overlay

> Squad: video-editor
> Codename: LOGO
> Role: Adicionar logo/watermark subtle no canto + CRECI/rodapé legal pra clientes regulados.

## Inputs

- `brand-profile.visual_identity.logo_url` (path relativo ao client_dir)
- `brand-profile.visual_identity.logo_dark_url` (se houver, pra vídeos escuros)
- `brand-profile.client.creci` (se imobiliário — obrigatório no rodapé)
- `brand-profile.publishing.post_signature` (rodapé legal)

## Posicionamento padrão

- **Reels 9:16**: logo canto inferior direito, 80×80px, opacity 70%.
- **TV spot 16:9**: logo + CRECI rodapé inferior central nos últimos 3s.
- **Cinematic 30s**: NO logo durante o vídeo (mantém clean), CRECI aparece nos últimos 2s.

## Compliance imobiliário (Ballarin, Investbens)

Rodapé OBRIGATÓRIO nos últimos 3-5s:
```
Ballarin Imóveis | CRECI J 011.419-9
Construído por Sousa Araújo | Matrícula 84.141 | Alvará 17/2026
```

Renderizado via Remotion com fonte serif white + outline preto.

## Output

`squads/video-editor/output/<date>/<id>/with-logo.mp4` (vai pro CUT pro render final)
