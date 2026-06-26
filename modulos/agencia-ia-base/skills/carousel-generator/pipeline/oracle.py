"""
oracle.py — Escolhe 1 pauta (cadência canônica 1/dia 14h BRT, validada em 06/05).

Lê histórico recente (últimos 14 dias) do log-publicacoes.md e do output dir,
constrói contexto e chama Claude com prompt do ORACLE.

Uso:
    python3 oracle.py 2026-04-26 > pautas.json
"""
import sys
import json
import os
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _claude import call_claude_json, load_prompt_template


PROJECT_ROOT = Path(os.environ.get("OPENSQUAD_CLIENT_DIR", os.getcwd()))
LOG_PATH = PROJECT_ROOT / "squads/conteudo-viral/output/log-publicacoes.md"
PIPELINE_OUTPUT_DIR = PROJECT_ROOT / "squads/conteudo-viral/output/pipeline-daily"


def parse_log_history() -> list[dict]:
    """Lê log-publicacoes.md e extrai temas/palavras-gatilho.
    Suporta múltiplos formatos de tabela MD usados ao longo do tempo."""
    if not LOG_PATH.exists():
        return []

    text = LOG_PATH.read_text(encoding="utf-8")
    history = []

    patterns = [
        # Formato 1: | 2026-04-23 | C01 — "Você Não Falhou" | ...
        re.compile(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(C\d+)\s*[—–-]\s*\"?([^\"|]+?)\"?\s*\|"),
        # Formato 2: | 2026-04-25 | C08 | DARK | MODELO | ...     (sem tema na 3ª coluna)
        re.compile(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\*\*)?\s*(C\d+)\s*\|"),
        # Formato 3: | **C08** "tema" | DARK | MODELO | ...        (id em bold sem data)
        re.compile(r"\|\s*\*\*(C\d+)\*\*\s*\"?([^\"|]+?)\"?\s*\|.*?(\d{2}:\d{2}|MODELO|AUTOMACAO|MERCADO|ESCALA)"),
    ]

    for line in text.split("\n"):
        for pat in patterns:
            m = pat.search(line)
            if m:
                groups = m.groups()
                if pat == patterns[0]:
                    data, cid, tema = groups
                elif pat == patterns[1]:
                    data, _, cid = groups
                    tema = ""  # tema não tá nessa linha
                else:
                    cid, tema = groups[0], groups[1]
                    data = "?"
                history.append({"data": data.strip(), "id": cid.strip(), "tema": tema.strip()[:80]})
                break  # usa só o primeiro match por linha

    # Dedup por id (mantém o mais informativo)
    by_id = {}
    for h in history:
        if h["id"] not in by_id or len(h["tema"]) > len(by_id[h["id"]]["tema"]):
            by_id[h["id"]] = h

    return sorted(by_id.values(), key=lambda x: x["id"])[-30:]


def find_last_carousel_id(history: list[dict]) -> int:
    """Retorna o número do último carrossel publicado (ex: 10 para C10)."""
    if not history:
        return 0
    nums = []
    for h in history:
        m = re.match(r"C(\d+)", h["id"])
        if m:
            nums.append(int(m.group(1)))
    return max(nums) if nums else 0


def get_output_carrosseis() -> list[dict]:
    """Escaneia output/carrossel-cXX-* dirs por carrosséis gerados fora do pipeline-daily.

    Útil pra carrosséis manuais (C41/C42 etc) que estão em output/ mas não em
    pipeline-daily/. Garante que ORACLE pega o último ID correto.
    """
    out_dir = PROJECT_ROOT / "squads/conteudo-viral/output"
    if not out_dir.exists():
        return []

    out = []
    for d in sorted(out_dir.iterdir()):
        if not d.is_dir():
            continue
        # Procura JSON canon (05-carousel.json) ou qualquer C*.json no root do dir
        candidates = list(d.glob("05-carousel.json")) + list(d.glob("C*.json"))
        for cf in candidates[:1]:  # 1 por dir é suficiente
            try:
                cdata = json.load(open(cf))
                cid = cdata.get("id", "")
                if re.match(r"^C\d+$", cid):
                    out.append({
                        "id": cid,
                        "data": cdata.get("data_publicacao", d.name),
                        "tema": cdata.get("tema", ""),
                        "pilar": cdata.get("pilar", ""),
                        "palavra_gatilho": cdata.get("palavra_gatilho", ""),
                    })
                    break
            except Exception:
                continue
    return out


def get_pautas_history_dir() -> list[dict]:
    """Lê pautas geradas previamente em pipeline-daily/ pra evitar repetir tema."""
    if not PIPELINE_OUTPUT_DIR.exists():
        return []

    out = []
    for day_dir in sorted(PIPELINE_OUTPUT_DIR.iterdir()):
        if not day_dir.is_dir():
            continue
        pautas_file = day_dir / "pautas.json"
        if pautas_file.exists():
            try:
                data = json.load(open(pautas_file))
                for p in data.get("pautas", []):
                    out.append({
                        "data": day_dir.name,
                        "id": p.get("id"),
                        "tema": p.get("tema"),
                        "pilar": p.get("pilar"),
                        "palavra_gatilho": p.get("palavra_gatilho"),
                    })
            except json.JSONDecodeError:
                pass
    return out[-30:]


def build_oracle_input(target_date: str) -> dict:
    """Monta o JSON que vai pro prompt do ORACLE."""
    log_history = parse_log_history()
    pipeline_history = get_pautas_history_dir()
    output_history = get_output_carrosseis()  # 2026-05-08: pega carrosséis manuais (C41/C42)
    all_history = log_history + pipeline_history + output_history
    last_id = find_last_carousel_id(all_history)
    # Cadência canônica 1/dia 14h BRT (decisão 06/05) — gera apenas 1 pauta
    next_ids = [f"C{last_id + 1}"]

    return {
        "data_publicacao": target_date,
        "proximos_ids": next_ids,
        "historico_recente": all_history,
    }


def run_oracle(target_date: str, save_dir: Path | None = None) -> dict:
    system_prompt = load_prompt_template("oracle")
    user_input = build_oracle_input(target_date)

    full_prompt = (
        f"{system_prompt}\n\n"
        f"---\n\n"
        f"## Input do dia\n\n"
        f"```json\n{json.dumps(user_input, ensure_ascii=False, indent=2)}\n```"
    )

    print(f"[ORACLE] Chamando Claude... (input: {len(user_input['historico_recente'])} históricos)", file=sys.stderr)
    result = call_claude_json(full_prompt)

    # Validações básicas (cadência 1/dia)
    if "pautas" not in result or len(result["pautas"]) != 1:
        raise ValueError(f"ORACLE retornou {len(result.get('pautas', []))} pautas, esperado 1")

    # Garante que IDs batem com proximos_ids + slot canon 14h00
    for i, p in enumerate(result["pautas"]):
        p["id"] = user_input["proximos_ids"][i]
        p["data_publicacao"] = target_date
        p["slot_brt"] = "14h00"  # cadência canônica
        # Seeding fica opcional (com 1 pauta/dia, alterna por critério editorial — não regra fixa)
        p.setdefault("tem_seeding_crm_funnels", False)

    if save_dir:
        save_dir.mkdir(parents=True, exist_ok=True)
        (save_dir / "pautas.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"[ORACLE] Salvo em {save_dir / 'pautas.json'}", file=sys.stderr)

    return result


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    save_dir = PIPELINE_OUTPUT_DIR / target
    out = run_oracle(target, save_dir=save_dir)
    print(json.dumps(out, ensure_ascii=False, indent=2))
