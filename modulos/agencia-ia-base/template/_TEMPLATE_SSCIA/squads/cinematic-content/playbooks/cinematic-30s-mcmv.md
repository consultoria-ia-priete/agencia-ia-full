# Playbook — Cinematic 30s MCMV (Grupo A)

Vídeo 30s vertical 9:16 pra empreendimento MCMV.

## Quando usar

- Cliente com `content_engine.group == "A"` (Ballarin Sou Viver Milão, Investbens Residencial Serraria).
- Cadência: 3 vídeos por semana.
- Output target: Instagram Reels, Facebook Reels, Google Business Profile, eventualmente TikTok.

## Templates Higgsfield disponíveis

| Template | Quando usar | Créditos |
|---|---|---|
| `apartment_hero_30s` | 1 por semana — fachada/portaria/lobby. Aspiração desejo de compra. | 42 (Kling 3.0) |
| `lifestyle_resident_30s` | 2 por semana — uso interno (sala/cozinha/quarto/varanda) ou área comum (lazer/piscina). | 42 (Kling 3.0) |

## Fluxo (semanal)

1. **Briefing** (CINE com operador): tema da semana
   - Ex: "Esta semana mostramos a área de lazer + chegada da família + cozinha de manhã"

2. **Storyboard** (AURA): 3 storyboards × 30s
   - Storyboard 1 (hero): fachada golden hour
   - Storyboard 2 (lifestyle interno): cozinha matinal
   - Storyboard 3 (lifestyle externo): piscina família

3. **Geração** (CINE chama skill):
   ```bash
   python ~/.claude/skills/higgsfield-content/pipelines/generate_cinematic_video.py \
     --client investbens-residencial-serraria \
     --template apartment_hero_30s \
     --param scene="modern Brazilian MCMV apartment building Diadema golden hour" \
     --param emotional_beat="silhouette of family approaching entrance with shopping bags"
   ```
   Claude pega o output, chama `mcp__claude_ai_Higgsfield__generate_video`, salva mp4.

4. **Caption** (ECHO-MCMV): pt-BR + disclaimer Lei 4.591/64 obrigatório

5. **Push pro worker** (`POST /admin/queue` com `media_type: video/mp4`)
   - Worker grava no KV STATE com `status: pending`
   - Dashboard `{{SEO_WORKER_DOMAIN}}/<slug>` mostra preview

6. **Aprovação operador** → worker publica via CRM Funnels nas plataformas:
   - `instagram`, `facebook`, `google_business_profile`

## Custos estimados/sem por cliente

3 vídeos × 42cr (Kling) = **126 créditos/sem por cliente Grupo A**
+ 5 imagens × 2cr (Nano Banana 2K) = 10cr
**Total: 136 créditos/sem/cliente** (~ 272 cr × 2 clientes = 544 cr/sem só Grupo A)

## Compliance checklist (rodar antes de aprovar)

- [ ] Sem rosto identificável em nenhuma peça
- [ ] Disclaimer Lei 4.591/64 presente em peças com valores
- [ ] Construtora aparece como texto rodapé, NÃO logo
- [ ] CRECI do cliente no rodapé
- [ ] Não cita concorrentes
- [ ] Não usa urgência fake ("últimas unidades")
- [ ] CTA aponta pra canal certo (WhatsApp do cliente / formulário oficial)
