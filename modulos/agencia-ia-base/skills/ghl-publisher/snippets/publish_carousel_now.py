"""
publish_carousel_now.py — Publica um carrossel (C08, C09 ou C10) imediato
em Instagram + LinkedIn via skill ghl-publisher.

Uso:
    python publish_carousel_now.py C08
    python publish_carousel_now.py C09
    python publish_carousel_now.py C10

Lê URLs do CDN de /tmp/c08-c10-ghl-urls.json (gerado pelo upload_media).
"""
import sys
import os
import json
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from create_post import create_immediate_post
from list_posts import list_posts, get_post

# Captions hardcoded (auto-contido, evita parsing do MD)
CAPTIONS = {
    "C08": """O modelo que o guru te ensinou já foi abandonado por ele.

Pensa comigo:

→ Quem vende curso de afiliação ganha dinheiro vendendo o CURSO. Não fazendo afiliação.
→ Quem vende mentoria de drop não tem mais loja. Tem produto digital.
→ Quem vende método de tráfego não vive de cliente — vive de aluno.

A operação que enriqueceu eles não é a operação que eles te ensinam.

E o que sobra pra você?

Sobra o modelo que eles ABANDONARAM porque dá trabalho:
servir empresa com IA, na recorrência, entregando resultado real.

CNPJ paga.
CNPJ paga todo mês.
CNPJ não vai embora se você entregar.

Esse é o caminho. Esse é o consultor de IA.

——

Comenta MODELO aqui e eu te mando o link do meu Treinamento Grátis de como criar sua ConsultorIA.

#ConsultorIA #IAparaNegocios #MarketingDigital #NDE #AlexPriete""",
    "C09": """Empresário CNPJ não te paga por "IA".

Ele te paga por RESULTADO mensurável que ele consegue ver na primeira semana.

E pra entregar isso, basta dominar 3 automações que qualquer consultor monta:

1. ATENDIMENTO WHATSAPP 24/7
   Bot qualifica lead, marca reunião, reduz custo de SDR em 70%. Setup: 4h.

2. TRIAGEM E CLASSIFICAÇÃO DE LEADS
   IA lê leads que entram e dispara workflow. Aumento de conversão: 25–40%. Setup: 6h.

3. RESUMO AUTOMÁTICO DE REUNIÃO
   Grava, transcreve, gera ata, cria tarefa no CRM. Vendedor para de perder follow-up. Setup: 2h.

12 horas de setup.
R$1.500/mês de fee recorrente.
Operação do cliente economizando R$3K+ por mês.

É matemática. Não é mágica.

——

Comenta AUTOMACAO aqui e eu te mando o link do meu Treinamento Grátis de como criar sua ConsultorIA.

#ConsultorIA #AutomacaoIA #N8N #NDE #AlexPriete""",
    "C10": """O empresário não tem tempo de aprender IA.

Ele tem clínica pra tocar, equipe pra gerenciar, margem caindo, concorrente usando ChatGPT.

Ele SABE que precisa.
Ele NÃO SABE o que fazer.

E está procurando alguém.

Olha o tamanho do que está em jogo:

→ 21 milhões de CNPJs ativos no Brasil
→ 6,5 milhões com mais de R$ 360K/ano de faturamento
→ Menos de 1% usando IA de verdade na operação
→ Demanda crescendo 38% ao ano (FGV 2026)

Não é falta de mercado.
É falta de consultor preparado pra atender o mercado.

Você não precisa inventar demanda.
A demanda já existe. Falta você se posicionar como o consultor.

——

Comenta MERCADO aqui e eu te mando o link do meu Treinamento Grátis de como criar sua ConsultorIA.

#ConsultorIA #MercadoB2B #IAparaEmpresas #NDE #AlexPriete""",
}


def publish(carousel: str):
    """Publica o carrossel em IG + LI imediato."""
    urls_data = json.load(open("/tmp/c08-c10-ghl-urls.json"))
    if carousel not in urls_data:
        raise ValueError(f"Carrossel {carousel} não encontrado em /tmp/c08-c10-ghl-urls.json")

    urls = urls_data[carousel]
    caption = CAPTIONS[carousel]

    print(f"\n=== Publicando {carousel} ({len(urls)} slides) ===")
    results = {}
    for platform in ["instagram", "linkedin"]:
        try:
            res = create_immediate_post(platform, urls, caption)
            print(f"  ✓ {carousel}-{platform}: criado")
            results[platform] = res
            time.sleep(1.5)
        except Exception as e:
            print(f"  ✗ {carousel}-{platform}: {e}")
            results[platform] = {"error": str(e)}

    # Verificar 12s depois
    print(f"\n  Aguardando 12s para verificar...")
    time.sleep(12)

    posts = list_posts(
        "2026-04-24T00:00:00.000Z",
        "2026-04-27T00:00:00.000Z",
        limit=30
    )
    target = caption[:40]
    for p in posts:
        if p.get("summary", "").startswith(target[:30]):
            det = get_post(p["_id"])
            plat = det.get("platform")
            media = len(det.get("media", []))
            status = det.get("status")
            err = det.get("error")
            ok = plat in ("instagram", "linkedin") and media == 8 and not err
            mark = "✓" if ok else "✗"
            print(f"  {mark} {p['_id']} | {plat:10} | status={status} | media={media}")
            if err:
                print(f"      ERROR: {err[:100]}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python publish_carousel_now.py {C08|C09|C10}")
        sys.exit(1)
    publish(sys.argv[1].upper())
