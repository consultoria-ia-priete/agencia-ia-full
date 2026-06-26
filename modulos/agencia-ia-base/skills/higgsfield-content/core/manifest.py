"""
manifest.py — grava audit log de cada geração Higgsfield.

Cada geração produz um diretório `<CLIENT_DIR>/squads/<squad>/output/<date>/<id>/`
com:
- prompt.json      (prompt completo + template usado + params)
- manifest.json    (modelo, seed, duração, créditos, hash brand-profile, timestamps)
- output.mp4 / .jpg (asset gerado — preenchido depois do MCP retornar)
- push-payload.json (payload enviado ao worker /admin/queue)
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJETOS_ROOT = Path.home() / "Documents" / "PROJETOS_CLAUDE_CODE"


@dataclass
class Manifest:
    id: str
    slug: str
    squad: str
    date: str
    playbook: str
    sub_playbook: str
    template_name: str
    model: str
    duration_s: int | None
    aspect_ratio: str
    prompt_final: str
    params_used: dict[str, str]
    validations_applied: list[str]
    brand_profile_hash: str
    created_at: str
    credits_estimate: int | None = None
    credits_actual: int | None = None
    output_url: str | None = None
    output_local_path: str | None = None
    higgsfield_job_id: str | None = None
    seed: int | str | None = None
    status: str = "draft"  # draft | generated | pushed | published | failed
    push_payload_path: str | None = None
    error: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


def make_id(prefix: str) -> str:
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{ts}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def output_dir(client_dir: str, squad: str, date: str | None = None, manifest_id: str | None = None) -> Path:
    date = date or datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    manifest_id = manifest_id or make_id("gen")
    p = PROJETOS_ROOT / client_dir / "squads" / squad / "output" / date / manifest_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_prompt(out_dir: Path, prompt_bundle_dict: dict[str, Any]) -> Path:
    path = out_dir / "prompt.json"
    path.write_text(json.dumps(prompt_bundle_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def save_manifest(out_dir: Path, manifest: Manifest) -> Path:
    path = out_dir / "manifest.json"
    payload = asdict(manifest)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_manifest(out_dir: Path) -> Manifest:
    path = out_dir / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return Manifest(**data)


def update_manifest(out_dir: Path, **kwargs: Any) -> Manifest:
    m = load_manifest(out_dir)
    for k, v in kwargs.items():
        if hasattr(m, k):
            setattr(m, k, v)
        else:
            m.extra[k] = v
    save_manifest(out_dir, m)
    return m


def save_push_payload(out_dir: Path, payload: dict[str, Any]) -> Path:
    path = out_dir / "push-payload.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
