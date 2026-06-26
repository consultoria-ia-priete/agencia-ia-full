#!/usr/bin/env python3
"""
sscia-sync — Propagação template → clientes da agência ConsultorIA.

Substitui o `novo-cliente.sh` legado e adiciona propagação seletiva de updates
(squads, agentes, playbooks) com proteção hardcoded de arquivos exclusivos.

Uso (resumido):
    sscia-sync --status
    sscia-sync --new-client JRS_FLOORING [--operator "Alex" --brand-main "JRS Flooring" ...]
    sscia-sync --propagate-all [--dry-run] [--skip-customized]
    sscia-sync --propagate-squad nexus [--client X]
    sscia-sync --propagate-agent NAME --in-squad SQUAD [--client X]

Contrato de proteção: ver PROTECTED_PATHS.md (na mesma skill).
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# ── Configuração default (caminhos do ecossistema Alex) ────────────────────
PROJECTS_ROOT_DEFAULT = Path.home() / "Documents" / "PROJETOS_CLAUDE_CODE"
TEMPLATE_DIR_NAME = "_TEMPLATE_SSCIA"
SKILL_DIR = Path(__file__).resolve().parent

# ── Paths PROTEGIDOS (NUNCA tocar) ────────────────────────────────────────
PROTECTED_DIRS = [
    "_opensquad/_memory",
    "_opensquad/chief",
    ".claude",
    ".sscia-backup",
    ".vscode",
    ".idea",
    ".git",
    "node_modules",
]
PROTECTED_DIRS_GLOB = [   # padrões dentro de squads/
    "squads/*/_memory",
    "squads/*/output",
]
PROTECTED_FILES = [
    ".mcp.json",
    ".sscia-state.json",
    ".env",
    ".gitignore",
    ".DS_Store",
]
PROTECTED_PATTERNS = [    # fnmatch contra qualquer caminho relativo
    "**/credentials*",
    "**/ghl-credentials*",
    "**/*-secret*",
    "**/*.local.*",
    "**/*.env",
    "**/*.env.*",
]

# ── Paths PROPAGÁVEIS (template → cliente) ────────────────────────────────
PROPAGABLE_GLOBS = [
    "VERSION",
    "squads/*/squad.yaml",
    "squads/*/squad-party.csv",
    "squads/*/agents/*.md",
    "squads/*/playbooks/*.md",
    "squads/*/tasks/*.md",
]

# ── Mapa de placeholders → caminho no brand-profile.json ───────────────────
# Cada entrada: (placeholder, dot_path, fallback)
PLACEHOLDER_MAP: list[tuple[str, str, str]] = [
    ("{{CLIENT_ID}}",            "client.id",                   ""),
    ("{{CLIENTE_NOME}}",         "client.operator",             ""),
    ("{{EMAIL_OPERADOR}}",       "client.owner_email",          ""),
    ("{{MARCA_PRINCIPAL}}",      "brand.main",                  ""),
    ("{{COMUNIDADE}}",           "brand.community",             ""),
    ("{{PRODUTO_RECORRENTE}}",   "brand.saas_recurring",        ""),
    ("{{NICHO_PRINCIPAL}}",      "brand.industry",              ""),
    ("{{CLIENTE_IG}}",           "social.instagram_handle",     ""),
    ("{{SITE_PRINCIPAL}}",       "websites.primary",            ""),
    ("{{SITE_LOWTICKET}}",       "websites.lp_low_ticket",      ""),
    ("{{SITE_QUIZ}}",            "websites.quiz",               ""),
    ("{{TRACKING_DOMAIN}}",      "websites.tracking",           ""),
    ("{{DOMINIO_PRINCIPAL}}",    "websites.domain_root",        ""),
    ("{{IDIOMA_PUBLICACAO}}",    "language.publication",        "pt-BR"),
    ("{{RESULTADO_PROMETIDO}}",  "audience.promise",            ""),
    ("{{GHL_LOCATION_ID}}",      "publishing.ghl_location_id",  ""),
    ("{{NICHO_BUSCA}}",          "brand.industry",              ""),
    ("{{TICKET_RECORRENTE}}",    "brand.saas_recurring",        ""),
    ("{{REFERENCIAS_MERCADO}}",  "audience.niche",              ""),
    ("{{CONTENT_GROUP}}",        "content_engine.group",        ""),
    ("{{CONTENT_PLAYBOOK}}",     "content_engine.playbook",     ""),
    ("{{CONTENT_SUB_PLAYBOOK}}", "content_engine.sub_playbook", ""),
    ("{{VIDEO_EDITOR_PIPELINE}}", "content_engine.video_editor_pipeline", "default"),
    ("{{CLIENTE_NICHO}}",        "brand.industry",              ""),
    ("{{COPY_AGENT}}",           "",                            "AUTO (GRIP decide em runtime: INK-SEO pra Grupo B local, INK-AUTHORITY pra B-prime Alex)"),
    # ── Identidade / posicionamento (adicionados 2026-05-30 após limpeza do template) ──
    ("{{CLIENT_NAME}}",          "client.name",                 ""),
    ("{{BRAND_MAIN}}",           "brand.main",                  ""),
    ("{{CLIENTE_SLUG}}",         "client.id",                   ""),
    ("{{AVATAR_PRINCIPAL}}",     "audience.primary",            ""),
    ("{{POSICIONAMENTO}}",       "brand.positioning",           ""),
    ("{{ESTADO}}",               "geo.state",                   ""),
    ("{{SITE}}",                 "websites.primary",            ""),
    ("{{GHL_WORKFLOW_ID}}",      "publishing.ghl_workflow_id",  ""),
    ("{{FUNNEL_SLUG}}",          "websites.funnel_slug",        ""),
    ("{{TRACKING_PAGES_PROJECT}}", "websites.tracking_pages_project", ""),
]

# Placeholders de CONTENT-TIME: preenchidos pelo agente por-post (ex: nº de anos,
# nº de cidades, tema de autoridade num exemplo de playbook). NÃO são de
# provisionamento — ficam como {{...}} de propósito e não geram warning.
CONTENT_TIME_PLACEHOLDERS = {"{{N}}", "{{ANOS}}", "{{TEMA_AUTORIDADE}}"}

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")

# ── Cores ANSI ─────────────────────────────────────────────────────────────
class C:
    RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
    RED = "\033[31m"; GREEN = "\033[32m"; YELLOW = "\033[33m"
    BLUE = "\033[34m"; CYAN = "\033[36m"; GRAY = "\033[90m"


# ════════════════════════════════════════════════════════════════════════════
# Modelo de dados
# ════════════════════════════════════════════════════════════════════════════

@dataclass
class Client:
    name: str          # nome da pasta (FLOOR_TO_CEILING)
    path: Path
    has_brand_profile: bool = False
    brand: dict[str, Any] = field(default_factory=dict)
    template_version_synced: str | None = None
    state: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileChange:
    rel_path: str
    template_path: Path
    client_path: Path
    status: str         # "new" | "updated" | "customized" | "unchanged" | "missing-in-template"
    template_hash: str
    client_hash: str | None
    state_hash: str | None  # hash registrado em .sscia-state.json


# ════════════════════════════════════════════════════════════════════════════
# Helpers
# ════════════════════════════════════════════════════════════════════════════

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def get_dot(d: dict, dotpath: str, default: Any = "") -> Any:
    cur: Any = d
    for k in dotpath.split("."):
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def is_protected(rel_path: str) -> bool:
    """rel_path é relativo à raiz do cliente (ex: 'squads/branding/_memory/foo.md')."""
    rp = rel_path.replace("\\", "/")
    parts = rp.split("/")

    # Diretórios fixos
    for prot_dir in PROTECTED_DIRS:
        if rp == prot_dir or rp.startswith(prot_dir + "/"):
            return True

    # Padrões em squads/*/X
    for glob_pat in PROTECTED_DIRS_GLOB:
        if fnmatch.fnmatchcase(rp, glob_pat) or fnmatch.fnmatchcase(rp, glob_pat + "/*") or any(
            fnmatch.fnmatchcase("/".join(parts[:i+1]), glob_pat) for i in range(len(parts))
        ):
            return True

    # Arquivos fixos (basename)
    base = parts[-1]
    if base in PROTECTED_FILES:
        return True

    # Patterns globais
    for pat in PROTECTED_PATTERNS:
        if fnmatch.fnmatch(rp, pat) or fnmatch.fnmatch(base, pat.split("/")[-1]):
            return True

    return False


def is_propagable(rel_path: str) -> bool:
    rp = rel_path.replace("\\", "/")
    for pat in PROPAGABLE_GLOBS:
        if fnmatch.fnmatchcase(rp, pat):
            return True
    return False


def list_propagable_files(template_dir: Path) -> list[Path]:
    """Retorna lista de Paths absolutos no template que são propagáveis."""
    found: list[Path] = []
    for pat in PROPAGABLE_GLOBS:
        for p in sorted(template_dir.glob(pat)):
            if p.is_file():
                found.append(p)
    return found


# ════════════════════════════════════════════════════════════════════════════
# Substituição de placeholders
# ════════════════════════════════════════════════════════════════════════════

def build_substitutions(brand: dict[str, Any]) -> dict[str, str]:
    """Resolve PLACEHOLDER_MAP usando brand-profile.json do cliente."""
    subs: dict[str, str] = {}
    for placeholder, dotpath, fallback in PLACEHOLDER_MAP:
        val = get_dot(brand, dotpath, fallback)
        subs[placeholder] = str(val) if val is not None else fallback

    # Geo restriçao: derivada de geo.exclusions[0]
    excl = get_dot(brand, "geo.exclusions", [])
    if isinstance(excl, list) and excl:
        subs["{{GEO_RESTRICAO}}"] = str(excl[0])
    else:
        subs["{{GEO_RESTRICAO}}"] = ""

    # Geo cidades (de geo.cities_primary) — usadas em playbooks de SEO local
    cities = get_dot(brand, "geo.cities_primary", [])
    if isinstance(cities, list) and cities:
        subs["{{CIDADE}}"] = str(cities[0])
        subs["{{CIDADES_PRIMARIAS}}"] = ", ".join(str(c) for c in cities)
    else:
        subs["{{CIDADE}}"] = ""
        subs["{{CIDADES_PRIMARIAS}}"] = ""
    # Região = estado (fallback pro geo SEO)
    subs["{{REGIAO}}"] = str(get_dot(brand, "geo.state", "") or "")

    # Datas dinâmicas
    today = datetime.now().strftime("%Y-%m-%d")
    subs["{{CREATED_AT}}"] = today
    subs["{{LAST_UPDATED}}"] = today

    return subs


def substitute(content: str, subs: dict[str, str]) -> str:
    """Aplica substituições no texto. Logs warning pra placeholders não resolvidos."""
    out = content
    for placeholder, value in subs.items():
        out = out.replace(placeholder, value)
    return out


def find_unresolved(content: str) -> list[str]:
    return [p for p in PLACEHOLDER_RE.findall(content)
            if p not in CONTENT_TIME_PLACEHOLDERS]


# ════════════════════════════════════════════════════════════════════════════
# Discovery de clientes
# ════════════════════════════════════════════════════════════════════════════

def discover_clients(projects_root: Path) -> list[Client]:
    """Encontra pastas de cliente em projects_root/."""
    clients: list[Client] = []
    if not projects_root.is_dir():
        return clients
    for entry in sorted(projects_root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_") or entry.name.startswith("."):
            continue  # _TEMPLATE_SSCIA, .git, etc.
        # Cliente válido = tem _opensquad/ E squads/
        if (entry / "_opensquad").is_dir() and (entry / "squads").is_dir():
            c = Client(name=entry.name, path=entry)
            bp = entry / "_opensquad" / "_memory" / "brand-profile.json"
            if bp.is_file():
                c.has_brand_profile = True
                try:
                    c.brand = json.loads(bp.read_text())
                except Exception:
                    pass
            sf = entry / ".sscia-state.json"
            if sf.is_file():
                try:
                    c.state = json.loads(sf.read_text())
                    c.template_version_synced = c.state.get("template_version_synced")
                except Exception:
                    pass
            clients.append(c)
    return clients


def get_template_version(template_dir: Path) -> str:
    vf = template_dir / "VERSION"
    if vf.is_file():
        return vf.read_text().strip()
    return "unknown"


# ════════════════════════════════════════════════════════════════════════════
# Diff entre template ↔ cliente ↔ estado
# ════════════════════════════════════════════════════════════════════════════

def compute_diff(client: Client, template_dir: Path, *, only_squad: str | None = None) -> list[FileChange]:
    """Pra cada arquivo PROPAGÁVEL no template, computa o status no cliente."""
    changes: list[FileChange] = []
    state_files = (client.state.get("files") or {}) if client.state else {}

    for tpl_file in list_propagable_files(template_dir):
        rel = tpl_file.relative_to(template_dir).as_posix()
        if only_squad and not (
            rel == "VERSION" or rel.startswith(f"squads/{only_squad}/")
        ):
            continue

        client_file = client.path / rel
        tpl_hash = sha256_file(tpl_file)
        cli_hash = sha256_file(client_file) if client_file.is_file() else None
        state_hash = state_files.get(rel)

        if cli_hash is None:
            status = "new"
        elif cli_hash == tpl_hash:
            status = "unchanged"
        elif state_hash is None:
            # cliente tem o arquivo, mas nunca passou por sscia-sync
            # -> trata como "customized" pra ser conservador
            status = "customized"
        elif cli_hash == state_hash and tpl_hash != state_hash:
            # cliente nunca editou após última sync; template avançou
            status = "updated"
        elif cli_hash != state_hash:
            status = "customized"
        else:
            status = "unchanged"

        changes.append(FileChange(
            rel_path=rel,
            template_path=tpl_file,
            client_path=client_file,
            status=status,
            template_hash=tpl_hash,
            client_hash=cli_hash,
            state_hash=state_hash,
        ))

    return changes


# ════════════════════════════════════════════════════════════════════════════
# Backup + escrita atômica
# ════════════════════════════════════════════════════════════════════════════

def backup_file(client_path: Path, rel_path: str, ts: str) -> None:
    src = client_path / rel_path
    if not src.is_file():
        return
    dst = client_path / ".sscia-backup" / ts / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_with_substitutions(tpl_path: Path, client_path: Path, rel_path: str, subs: dict[str, str]) -> list[str]:
    """Lê template, substitui placeholders, escreve no cliente. Retorna lista de placeholders não resolvidos."""
    content = tpl_path.read_text(encoding="utf-8")
    new_content = substitute(content, subs)
    unresolved = find_unresolved(new_content)
    dst = client_path / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(new_content, encoding="utf-8")
    return unresolved


def update_state(client: Client, applied_changes: list[FileChange], template_version: str) -> None:
    """Atualiza .sscia-state.json com hashes do template (não do cliente, porque substituições mudam o conteúdo)."""
    files = client.state.get("files", {}) if client.state else {}
    for ch in applied_changes:
        # Hash que importa pra detectar futuras mudanças no template é o hash do template ANTES da substituição.
        # Mas como aqui o cliente terá conteúdo POST-substituição, o hash dele será diferente.
        # Solução: armazenar o hash POS-substituição (do que ficou no cliente).
        new_cli_hash = sha256_file(ch.client_path)
        files[ch.rel_path] = new_cli_hash
    from datetime import timezone
    state = {
        "last_sync": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "template_version_synced": template_version,
        "files": files,
    }
    (client.path / ".sscia-state.json").write_text(json.dumps(state, indent=2))
    client.state = state


# ════════════════════════════════════════════════════════════════════════════
# UI helpers
# ════════════════════════════════════════════════════════════════════════════

def confirm(prompt: str, default_no: bool = True) -> bool:
    sfx = " [y/N]" if default_no else " [Y/n]"
    try:
        ans = input(prompt + sfx + " ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    if not ans:
        return not default_no
    return ans in ("y", "yes", "s", "sim")


def confirm_with_skip(prompt: str) -> str:
    """Retorna 'yes' | 'no' | 'skip-customized' | 'details'."""
    while True:
        try:
            ans = input(prompt + " [y/n/skip-customized/details] ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return "no"
        if ans in ("y", "yes"): return "yes"
        if ans in ("n", "no"): return "no"
        if ans in ("s", "skip", "skip-customized"): return "skip-customized"
        if ans in ("d", "details"): return "details"


def print_change_summary(client: Client, changes: list[FileChange]) -> dict[str, list[FileChange]]:
    buckets: dict[str, list[FileChange]] = {"new": [], "updated": [], "customized": [], "unchanged": []}
    for ch in changes:
        buckets.setdefault(ch.status, []).append(ch)

    print(f"\n{C.BOLD}── {client.name} ──{C.RESET}")
    print(f"  {C.GREEN}✓ Sem mudanças:{C.RESET} {len(buckets['unchanged'])} arquivos")
    print(f"  {C.CYAN}＋ Novos no template:{C.RESET} {len(buckets['new'])} arquivos")
    print(f"  {C.BLUE}↻ Atualizados no template:{C.RESET} {len(buckets['updated'])} arquivos")
    print(f"  {C.YELLOW}⚠️  Customizados no cliente:{C.RESET} {len(buckets['customized'])} arquivos")
    return buckets


def print_change_details(buckets: dict[str, list[FileChange]]) -> None:
    if buckets.get("new"):
        print(f"\n  {C.CYAN}＋ Novos:{C.RESET}")
        for ch in buckets["new"]:
            print(f"      {ch.rel_path}")
    if buckets.get("updated"):
        print(f"\n  {C.BLUE}↻ Atualizados:{C.RESET}")
        for ch in buckets["updated"]:
            print(f"      {ch.rel_path}")
    if buckets.get("customized"):
        print(f"\n  {C.YELLOW}⚠️  Customizados (sobrescrever?):{C.RESET}")
        for ch in buckets["customized"]:
            print(f"      {ch.rel_path}")


# ════════════════════════════════════════════════════════════════════════════
# Operações
# ════════════════════════════════════════════════════════════════════════════

def cmd_status(args, projects_root: Path, template_dir: Path) -> int:
    tpl_v = get_template_version(template_dir)
    print(f"{C.BOLD}sscia-sync — status{C.RESET}")
    print(f"  Projects root: {projects_root}")
    print(f"  Template:      {template_dir} (v{tpl_v})")
    print()

    clients = discover_clients(projects_root)
    if not clients:
        print(f"{C.YELLOW}  Nenhum cliente encontrado.{C.RESET}")
        return 0

    print(f"  {'CLIENTE':<28} {'BRAND':<8} {'TEMPLATE v':<12} {'STATE':<10}")
    print(f"  {'─'*28} {'─'*8} {'─'*12} {'─'*10}")
    for c in clients:
        bp = "✓" if c.has_brand_profile else "✗"
        sv = c.template_version_synced or "-"
        st = "synced" if c.state else "no-state"
        print(f"  {c.name:<28} {bp:<8} {sv:<12} {st:<10}")

    return 0


def cmd_propagate(
    args, projects_root: Path, template_dir: Path,
    *, only_squad: str | None = None, only_clients: list[str] | None = None,
) -> int:
    tpl_v = get_template_version(template_dir)
    clients = discover_clients(projects_root)
    if only_clients:
        wanted = set(only_clients)
        clients = [c for c in clients if c.name in wanted]
    if not clients:
        print(f"{C.RED}Nenhum cliente encontrado pra propagar.{C.RESET}")
        return 1

    print(f"{C.BOLD}sscia-sync — propagate{' --squad ' + only_squad if only_squad else '-all'}{C.RESET}")
    print(f"  Template v{tpl_v} → {len(clients)} cliente(s)")
    if args.dry_run:
        print(f"  {C.DIM}(dry-run — nenhuma mudança será aplicada){C.RESET}")
    print()

    total_applied = 0
    for client in clients:
        if not client.has_brand_profile:
            print(f"{C.YELLOW}⚠️  {client.name} não tem brand-profile.json — pulando.{C.RESET}")
            continue

        changes = compute_diff(client, template_dir, only_squad=only_squad)
        actionable = [c for c in changes if c.status in ("new", "updated", "customized")]
        if not actionable:
            print(f"{C.GREEN}✓ {client.name}: já em sync com template{C.RESET}")
            continue

        buckets = print_change_summary(client, changes)

        if args.dry_run:
            print_change_details(buckets)
            continue

        decision = "yes"
        if buckets.get("customized") or len(actionable) > 0:
            print_change_details(buckets) if (buckets.get("customized") and not args.skip_customized) else None
            if args.skip_customized:
                # Só pergunta se há new/updated. Customized fica de fora.
                if not (buckets.get("new") or buckets.get("updated")):
                    print(f"  {C.DIM}Só há customizados; --skip-customized → pulando cliente.{C.RESET}")
                    continue
                decision = "yes-skip"
            else:
                while True:
                    decision = confirm_with_skip(f"  Aplicar em {client.name}?")
                    if decision == "details":
                        print_change_details(buckets)
                        continue
                    break

        if decision == "no":
            print(f"  {C.GRAY}↩ pulado pelo operador.{C.RESET}")
            continue

        # Aplica
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        subs = build_substitutions(client.brand)
        applied: list[FileChange] = []
        skipped: list[FileChange] = []
        unresolved_log: dict[str, list[str]] = {}

        for ch in actionable:
            if ch.status == "customized" and decision in ("skip-customized", "yes-skip"):
                skipped.append(ch)
                continue
            # backup antes de tocar (só se já existe no cliente)
            if ch.client_path.is_file():
                backup_file(client.path, ch.rel_path, ts)
            try:
                un = write_with_substitutions(ch.template_path, client.path, ch.rel_path, subs)
                applied.append(ch)
                if un:
                    unresolved_log[ch.rel_path] = un
            except Exception as exc:
                print(f"    {C.RED}✗ falha em {ch.rel_path}: {exc}{C.RESET}")

        if applied:
            update_state(client, applied, tpl_v)
            total_applied += len(applied)
            print(f"  {C.GREEN}✓ Aplicado:{C.RESET} {len(applied)} arquivos")
            print(f"  {C.DIM}  Backup em: {client.path}/.sscia-backup/{ts}/{C.RESET}")
        if skipped:
            print(f"  {C.YELLOW}↩ Pulados (customizados):{C.RESET} {len(skipped)} arquivos")
        if unresolved_log:
            print(f"  {C.YELLOW}⚠️  Placeholders não resolvidos:{C.RESET}")
            for f, lst in unresolved_log.items():
                print(f"      {f}: {', '.join(set(lst))}")

    print(f"\n{C.BOLD}Total aplicado:{C.RESET} {total_applied} arquivos em {len(clients)} cliente(s)")
    return 0


def cmd_new_client(args, projects_root: Path, template_dir: Path) -> int:
    name = args.new_client
    target = projects_root / name
    if target.exists():
        print(f"{C.RED}✗ {target} já existe. Use --propagate-all pra atualizar cliente existente.{C.RESET}")
        return 1

    print(f"{C.BOLD}sscia-sync — provisioning {name}{C.RESET}")
    print(f"  Template:  {template_dir}")
    print(f"  Destino:   {target}")
    print()

    # Coleta dados (interativo + flags)
    def ask(label: str, flag_val: str | None, default: str = "") -> str:
        if flag_val:
            return flag_val
        try:
            ans = input(f"  {label}{f' [{default}]' if default else ''}: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return default
        return ans or default

    operator     = ask("Operador (ex: Alex Priete)",        args.operator,    "Alex Priete")
    brand_main   = ask("Marca principal",                    args.brand_main,  "")
    instagram    = ask("Instagram handle (com @)",           args.instagram,   "")
    industry     = ask("Indústria/nicho",                    args.industry,    "")
    country      = ask("Country code (BR/US)",               args.country,     "BR")
    state        = ask("Estado (sigla)",                     args.state,       "")
    language     = ask("Idioma de publicação (pt-BR/en-US)", args.language,    "pt-BR")
    ghl_key      = ask("CRM Funnels API key (pit-...)",              args.ghl_key,     "")
    ghl_loc      = ask("CRM Funnels Location ID",                    args.ghl_location,"")
    operator_email = ask("Email do operador",                None,             "{{EMAIL_OPERADOR}}")

    if not brand_main:
        print(f"{C.RED}Marca principal é obrigatória.{C.RESET}")
        return 1

    # Confirma
    print(f"\n  Provisionar {C.BOLD}{name}{C.RESET}?")
    print(f"    Operador:  {operator}")
    print(f"    Marca:     {brand_main}")
    print(f"    Instagram: {instagram}")
    print(f"    Geo:       {country}/{state}")
    print(f"    Idioma:    {language}")
    print(f"    CRM Funnels key:   {'(definida)' if ghl_key else '(VAZIA — você completa depois)'}")
    if not confirm("  Confirmar?", default_no=False):
        print("  Cancelado.")
        return 0

    # Copia estrutura template inteira (exceto pastas internas como .git)
    print(f"\n  ➜ Copiando estrutura...")
    shutil.copytree(template_dir, target, dirs_exist_ok=False, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", ".DS_Store"
    ))

    # Slug canônico (lowercase-hifen) = id do cliente = slug do seocontent dashboard
    slug = name.lower().replace("_", "-")

    # Cria brand-profile.json mínimo (overwrite o template)
    bp_path = target / "_opensquad" / "_memory" / "brand-profile.json"
    bp = json.loads(bp_path.read_text())
    bp["client"]["id"] = slug
    bp["client"]["name"] = brand_main
    bp["client"]["operator"] = operator
    bp["client"]["owner_email"] = operator_email
    bp["brand"]["main"] = brand_main
    bp["brand"]["industry"] = industry
    bp["social"]["instagram_handle"] = instagram
    bp["geo"]["country"] = country
    bp["geo"]["state"] = state
    bp["language"]["interface_chat"] = "pt-BR"
    bp["language"]["publication"] = language
    bp["publishing"]["ghl_location_id"] = ghl_loc
    bp["_metadata"]["created_at"] = datetime.now().strftime("%Y-%m-%d")
    bp["_metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    bp_path.write_text(json.dumps(bp, indent=2, ensure_ascii=False))
    print(f"  ✓ brand-profile.json preenchido")

    # Cria .mcp.json com CRM Funnels credentials se passou
    if ghl_key and ghl_loc:
        mcp = {
            "mcpServers": {
                "gohighlevel": {
                    "command": "npx",
                    "args": ["-y", "ghl-mcp-server-casewegner"],
                    "env": {
                        "GHL_API_KEY": ghl_key,
                        "GHL_BASE_URL": "https://services.leadconnectorhq.com",
                        "GHL_LOCATION_ID": ghl_loc,
                    },
                }
            }
        }
        (target / ".mcp.json").write_text(json.dumps(mcp, indent=2))
        print(f"  ✓ .mcp.json criado com CRM Funnels")
    else:
        print(f"  {C.YELLOW}⚠️  .mcp.json não criado (faltou CRM Funnels key/location). Crie manualmente quando tiver.{C.RESET}")

    # Roda propagate-all silenciosamente nesse cliente pra resolver placeholders dos squads
    print(f"\n  ➜ Aplicando substituições nos squads...")
    client = Client(name=name, path=target, has_brand_profile=True, brand=bp)
    subs = build_substitutions(bp)
    tpl_v = get_template_version(template_dir)
    propagable = list_propagable_files(template_dir)
    applied_changes: list[FileChange] = []
    for tpl_file in propagable:
        rel = tpl_file.relative_to(template_dir).as_posix()
        try:
            write_with_substitutions(tpl_file, target, rel, subs)
            applied_changes.append(FileChange(
                rel_path=rel, template_path=tpl_file, client_path=target / rel,
                status="new", template_hash=sha256_file(tpl_file), client_hash=None, state_hash=None,
            ))
        except Exception as exc:
            print(f"    {C.YELLOW}⚠️  {rel}: {exc}{C.RESET}")
    update_state(client, applied_changes, tpl_v)
    print(f"  ✓ {len(applied_changes)} arquivos parametrizados")

    # ── Provisiona o SEO content dashboard no worker {{SEO_WORKER_DOMAIN}} ──
    # Best-effort: precisa de wrangler login + rede. Falha não aborta o onboarding.
    print(f"\n  ➜ Provisionando SEO content dashboard ({slug})...")
    provision_script = projects_root / "_AGENCY" / "seocontent-worker" / "scripts" / "provision-client.py"
    if provision_script.exists():
        try:
            r = subprocess.run(
                ["python3", str(provision_script), slug],
                capture_output=True, text=True, timeout=120,
                cwd=str(provision_script.parent.parent),
            )
            if r.returncode == 0:
                # Repassa as URLs que o script imprime (dashboard interna/externa)
                for line in r.stdout.splitlines():
                    if "{{SEO_WORKER_DOMAIN}}" in line or "✓ Provisionado" in line:
                        print(f"    {line.strip()}")
                print(f"  {C.GREEN}✓ Dashboard provisionado{C.RESET}")
            else:
                print(f"  {C.YELLOW}⚠️  Dashboard não provisionado (rode manualmente depois):{C.RESET}")
                print(f"     python3 {provision_script} {slug}")
                if r.stderr.strip():
                    print(f"     {C.GRAY}{r.stderr.strip().splitlines()[-1]}{C.RESET}")
        except Exception as exc:
            print(f"  {C.YELLOW}⚠️  Dashboard não provisionado ({exc}). Rode: python3 {provision_script} {slug}{C.RESET}")
    else:
        print(f"  {C.GRAY}(provision-client.py não encontrado — pulando dashboard){C.RESET}")

    print(f"\n{C.GREEN}✓ Cliente {name} provisionado em {target}{C.RESET}")
    print(f"\n  {C.BOLD}Próximos passos:{C.RESET}")
    print(f"    1. cd {target}")
    print(f"    2. Editar _opensquad/_memory/brand-profile.json (cores, voice, CRM Funnels accountIds, etc.)")
    print(f"    3. Conectar IG/FB do cliente no CRM Funnels → preencher accountIds → re-rodar provision-client.py")
    print(f"    4. /opensquad run nexus")
    return 0


# ════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="sscia-sync",
        description="Propagação template → clientes da agência ConsultorIA. Skill em ~/.claude/skills/sscia-sync/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--projects-root", default=str(PROJECTS_ROOT_DEFAULT),
                   help=f"raiz dos projetos (default: {PROJECTS_ROOT_DEFAULT})")

    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--status", action="store_true", help="lista clientes e estado de sync")
    g.add_argument("--new-client", metavar="NAME", help="provisiona cliente novo (substitui novo-cliente.sh)")
    g.add_argument("--propagate-all", action="store_true", help="propaga TODOS arquivos propagáveis pra TODOS os clientes (com confirmação)")
    g.add_argument("--propagate-squad", metavar="SQUAD_NAME", help="propaga só 1 squad")

    p.add_argument("--client", action="append", help="restringe a propagação a 1 ou mais clientes (use múltiplas vezes)")
    p.add_argument("--dry-run", action="store_true", help="só mostra o que mudaria, não aplica")
    p.add_argument("--skip-customized", action="store_true", help="pula arquivos customizados sem perguntar")

    # Flags pra --new-client
    p.add_argument("--operator")
    p.add_argument("--brand-main")
    p.add_argument("--instagram")
    p.add_argument("--industry")
    p.add_argument("--country")
    p.add_argument("--state")
    p.add_argument("--language")
    p.add_argument("--ghl-key")
    p.add_argument("--ghl-location")

    return p.parse_args()


def main() -> int:
    args = parse_args()
    projects_root = Path(args.projects_root).expanduser().resolve()
    template_dir = projects_root / TEMPLATE_DIR_NAME

    if not template_dir.is_dir():
        print(f"{C.RED}✗ Template não encontrado: {template_dir}{C.RESET}")
        return 1

    if args.status:
        return cmd_status(args, projects_root, template_dir)
    if args.new_client:
        return cmd_new_client(args, projects_root, template_dir)
    if args.propagate_all:
        return cmd_propagate(args, projects_root, template_dir, only_clients=args.client)
    if args.propagate_squad:
        return cmd_propagate(
            args, projects_root, template_dir,
            only_squad=args.propagate_squad, only_clients=args.client,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
