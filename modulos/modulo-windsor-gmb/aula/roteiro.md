# 🎬 Aula — Windsor.ai + Google My Business

> Aula CURTA (alvo 7–9 min). Alex grava conectando o Windsor e puxando reviews de uma ficha real.
> **Pré-produção:** conta Windsor; conta Google que administra uma ficha do GMB com reviews.

## Cena 0 — Gancho (0:00–0:30)
"Suas avaliações do Google viram prova social, SEO local e resposta automática — tudo pela IA.
E o melhor: sem instalar nada, é tudo na nuvem."

## Cena 1 — Conectar Windsor no claude.ai (0:30–2:30)
- claude.ai → Connectors → adicionar **Windsor.ai** → OAuth. "Conexão na nuvem, sem chave local."

## Cena 2 — Autorizar o GMB no Windsor (2:30–4:30)
- Windsor → conector **Google My Business** → autorizar com a conta Google → escolher a localização.

## Cena 3 — Primeiro pull (4:30–7:00)
- Achar o `locations/<ID>` (frisar: não é o place_id do Maps).
- Pedir ao Claude as reviews dos últimos 2 anos → mostrar a tabela (nota, comentário, autor, data).

## Cena 4 — Ação de escrita (bônus) (7:00–8:30)
- `list_actions` → mostrar que dá pra responder review / postar no GMB (com confirmação).

## Cena 5 — Fechamento
- "Dados do Google Meu Negócio nas mãos da IA." Encaixe: prova social + SEO local. CTA rotativo.

---
### Erros ao vivo
- Usou `place_id` → trocar pelo `locations/...`.
- Conta Google sem permissão na ficha → autorizar a conta certa.
