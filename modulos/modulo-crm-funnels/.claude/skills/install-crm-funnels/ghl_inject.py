#!/usr/bin/env python3
"""ghl_inject.py — Injeta (ou remove) o bloco `gohighlevel` no .mcp.json de uma agência.

Idempotente: cria o bloco se não existe, atualiza se já existe (não duplica), preserva
os outros MCPs (playwright, higgsfield). Sempre faz backup .mcp.json.bak antes de mexer.

Uso:
    python3 ghl_inject.py --client-dir DIR --api-key "pit-..." --location "LOC"
    python3 ghl_inject.py --client-dir DIR --remove

NUNCA chame este script sem antes validar com ghl_validate.py.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

BASE_URL = "https://services.leadconnectorhq.com"


def load_mcp(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            print(f"✗ {path} existe mas não é JSON válido. Conserte antes.", file=sys.stderr)
            sys.exit(2)
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-dir", required=True)
    ap.add_argument("--api-key")
    ap.add_argument("--location")
    ap.add_argument("--remove", action="store_true")
    args = ap.parse_args()

    client_dir = Path(args.client_dir).expanduser()
    mcp_path = client_dir / ".mcp.json"

    if not client_dir.is_dir():
        print(f"✗ Pasta não encontrada: {client_dir}", file=sys.stderr)
        return 2

    data = load_mcp(mcp_path)
    data.setdefault("mcpServers", {})

    # Backup antes de qualquer escrita.
    if mcp_path.exists():
        shutil.copy(mcp_path, mcp_path.with_suffix(".json.bak"))

    if args.remove:
        if "gohighlevel" in data["mcpServers"]:
            del data["mcpServers"]["gohighlevel"]
            mcp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            print("✓ Bloco gohighlevel removido. (backup em .mcp.json.bak)")
        else:
            print("(nada a remover — não havia bloco gohighlevel)")
        return 0

    if not args.api_key or not args.location:
        print("✗ Faltou --api-key e/ou --location.", file=sys.stderr)
        return 2

    # Cria/atualiza o bloco (idempotente).
    data["mcpServers"]["gohighlevel"] = {
        "command": "npx",
        "args": ["-y", "ghl-mcp-server-casewegner"],
        "env": {
            "GHL_API_KEY": args.api_key,
            "GHL_BASE_URL": BASE_URL,
            "GHL_LOCATION_ID": args.location,
        },
    }
    mcp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"✓ Bloco gohighlevel gravado em {mcp_path}")
    print("  Reabra o Claude Code na pasta da agência pra carregar o MCP.")
    print("  Lembrete: .mcp.json está no .gitignore — a chave não vai pro GitHub.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
