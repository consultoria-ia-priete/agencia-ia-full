# Pre-publish checklist — peça visual

Roda **antes** de qualquer publicação via ghl-publisher (regra do ecossistema, ver memória `feedback_preview_html_obrigatorio.md`).

## 1. Coerência de marca
- [ ] Cores predominantes batem com `brand-profile.json` → `visual_identity.primary_color/secondary_color`
- [ ] Estilo visual condiz com `voice.tone` (warm-professional ≠ cyberpunk-edgy)
- [ ] Logo NÃO aparece dentro da imagem (sempre overlay externo, nunca queimado)

## 2. Coerência geográfica
- [ ] Setting/casa/ambiente coerente com `geo.country` e `geo.state`
  - Ex: cleaning USA → casa estilo americano, não favela brasileira nem chalé europeu
  - Ex: imobiliário SP → arquitetura tropical/moderna, não cottage inglês

## 3. Coerência de idioma
- [ ] Caption no idioma de `language.publication`
- [ ] Texto on-image (se houver) no idioma de `language.publication`
- [ ] CTA condizente com mercado (ex: "Get a free quote" pra US, "Solicite seu orçamento" pra BR)

## 4. Conteúdo
- [ ] Sem rostos identificáveis de pessoas reais sem permissão
- [ ] Sem logos de terceiros (Coca-Cola, marcas etc.)
- [ ] Sem texto distorcido/ilegível (artefato comum do Flux Dev → trocar pra Ideogram)
- [ ] Sem dedos extras / anatomia quebrada (re-gerar com nova seed)

## 5. Restrições do cliente (compliance)
- [ ] Nenhum item de `compliance.do_not_mention` aparece
- [ ] Claims usados estão em `compliance.approved_claims`
- [ ] Geo de exclusão respeitado (ex: Floor to Ceiling NÃO mostra cenários PA)

## 6. Aprovação humana
- [ ] preview.html gerado e enviado ao operador
- [ ] Operador deu OK explícito (não inferir)

## 7. Plataformas de destino
- [ ] Aspect ratio correto pra cada plataforma:
  - Feed IG/FB: 1:1 (1080×1080) ou 4:5 (1080×1350)
  - Reels/Shorts/TikTok: 9:16 (1080×1920)
  - GMB post: 1:1 ou 16:9
  - LinkedIn: 1:1 ou 1.91:1
- [ ] `media[].type = "image/jpeg"` (não PNG — restrição CRM Funnels ghl-publisher)
- [ ] Imagens convertidas pra JPEG via `sips` se necessário

## Se algum item falhar
- Re-gerar slide específico (mantendo seed pra variação controlada) OU trocar de modelo (texto ruim → Ideogram)
- Avaliar se o template precisa de revisão (problema sistemático)
- Em caso de dúvida → escala pra operador antes de publicar
