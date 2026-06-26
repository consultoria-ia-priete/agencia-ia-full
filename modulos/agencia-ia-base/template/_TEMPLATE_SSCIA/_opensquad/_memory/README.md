# Memória central do cliente (`_opensquad/_memory/`)

Este diretório contém os arquivos de configuração e contexto **deste cliente** — usados pelo NEXUS, pelas 6 squads operacionais e pelas skills globais (`creative-factory`, `viral-video-factory`, `ghl-publisher`).

## Arquivos canônicos

| Arquivo | Conteúdo | Quem mantém |
|---|---|---|
| `company.md` | Perfil narrativo da empresa: setor, área de atuação, USPs, tom de voz, política operacional, restrições | Operador (preenche no provisionamento, atualiza conforme cliente evolui) |
| `brand-profile.json` | **Schema estruturado** que alimenta automaticamente geradores: cores, vozes, modelos default, accountIds CRM Funnels, keywords SEO, etc. | Operador (preenche no provisionamento) + sscia-sync (mantém schema_version atualizado) |
| `brand-kit.md` | Kit de marca enxuto em markdown: paleta, fontes, logos, exemplos visuais (referência humana) | Operador |
| `preferences.md` | Preferências do operador: idioma de chat, idioma de publicação, política de aprovação | Operador |

## Diferença `company.md` × `brand-profile.json`

- **`company.md`** = narrativa humana, lida pelos agentes em prosa, contexto rico.
- **`brand-profile.json`** = dados estruturados, lidos por scripts/skills programaticamente. Ex: `creative-factory` lê `visual_identity.primary_color` pra colorir slides; `ghl-publisher` lê `publishing.ghl_account_ids.tiktok` pra postar.

Os dois devem estar coerentes (mesmo cliente). Quando um campo do `brand-profile.json` for descoberto/alterado, atualizar `company.md` também (ou vice-versa).

## Não confundir com squads/_memory/

- `_opensquad/_memory/` (este aqui) = **identidade do cliente** — estável, edição manual.
- `squads/<squad>/_memory/` = **memória operacional do squad** — construída pelo CHRONICLER ao longo das execuções.

## Ao provisionar cliente novo (sscia-sync --new-client)

Os placeholders `{{...}}` em todos os arquivos são substituídos automaticamente pelos valores informados no provisionamento (CLIENTE_NOME, MARCA_PRINCIPAL, CLIENTE_IG, etc.). Após provisionamento, o operador completa os campos vazios do `brand-profile.json` (cores, CRM Funnels accountIds, keywords SEO, etc.) antes de rodar o primeiro NEXUS.
