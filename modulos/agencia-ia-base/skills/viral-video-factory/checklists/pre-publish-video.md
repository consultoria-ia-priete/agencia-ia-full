# Pre-publish checklist — vídeo viral

Roda **antes** de qualquer publicação via ghl-publisher (extensão futura pra vídeo).

## 1. Coerência de marca
- [ ] Cores predominantes batem com `brand-profile.json` → `visual_identity.primary_color/secondary_color`
- [ ] Fonts das legendas: Inter Bold (default Remotion)
- [ ] Logo overlay (se houver) coerente com `brand.logo_url`
- [ ] Voz coerente com `voice.elevenlabs_default_voice_label`

## 2. Coerência geográfica
- [ ] Setting visual condiz com `geo.country` e `geo.state`
- [ ] Idioma do voiceover bate com `language.publication`
- [ ] Idioma das legendas bate com voiceover (Whisper transcreve do áudio)
- [ ] CTA condizente com mercado (ex: "Get a free quote" pra US, "Solicite seu orçamento" pra BR)

## 3. Conteúdo
- [ ] Hook impactante nos primeiros 3 segundos (algoritmo IG/TikTok premia retenção early)
- [ ] Sem rostos identificáveis sem permissão
- [ ] Sem música com copyright (usar royalty-free ou trilha do ElevenLabs Music se disponível)
- [ ] Sem texto distorcido nas legendas burned-in
- [ ] Duração condizente com plataforma:
  - Reels/Shorts: 30-60s ideal
  - GMB: máx 30s (hard limit plataforma)
  - TikTok: 15-90s ideal

## 4. Restrições do cliente (compliance)
- [ ] Nenhum item de `compliance.do_not_mention` aparece (verbal ou visual)
- [ ] Claims usados estão em `compliance.approved_claims`
- [ ] Geo de exclusão respeitado (ex: FTC NÃO mostra cenários PA)

## 5. Qualidade técnica
- [ ] Resolução ≥ 1080×1920 (Reels) ou 1080×1080 (Feed/GMB)
- [ ] Bitrate ≥ 6 Mbps pra IG (recomendação)
- [ ] FPS 30 ou 60 (não 24)
- [ ] Áudio normalizado (não muito alto/baixo)
- [ ] Legendas legíveis em mobile (font ≥ 56px)

## 6. Aprovação humana
- [ ] preview MP4 enviado pro operador
- [ ] Operador deu OK explícito (não inferir)

## 7. Plataformas de destino
- [ ] Versão 1080x1920 pra Reels/Shorts/TikTok
- [ ] Versão 1080x1080 pra Feed (com legendas reposicionadas)
- [ ] Versão 30s cropped pro GMB (se aplicável)
- [ ] `media[].type = "video/mp4"` (suporte do ghl-publisher pra vídeo TBD)

## Se algum item falhar
- Re-render Remotion com prop diferente (mais rápido que regenerar tudo)
- Re-gerar 1 slide específico via creative-factory (sem refazer voiceover)
- Em caso de dúvida → escala pro operador antes de publicar
