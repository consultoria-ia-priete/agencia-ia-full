"""
prompt_builder.py — monta o prompt final a partir de um template YAML + brand-profile.

Template YAML típico:
    name: dop_top_down
    playbook: viral-reels-seo
    sub_playbook: dop-7s-reel
    duration: 7
    aspect_ratio: "9:16"
    model: dop
    prompt_template: |
      Top-down aerial view of {subject} {action},
      camera directly overhead {camera_feel},
      {lighting}, {texture}, no face no person visible, authentic work feel.
    required_params: [subject, action]
    defaults:
      camera_feel: locked-off
      lighting: warm indoor light
      texture: satisfying motion detail
    validators:
      - no_face_no_person

Uso:
    from prompt_builder import build
    out = build(template_path, brand, params={"subject": "vacuum on plush carpet", "action": "moving in straight lines"})
    print(out.final_prompt)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

try:
    from .brand_loader import BrandProfile  # type: ignore[import-not-found]
except ImportError:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from brand_loader import BrandProfile  # type: ignore[no-redef]

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

DOP_FORBIDDEN_TERMS = ["face", "smiling", "smile", "person standing", "person walking", "human face", "selfie"]
DOP_VALID_ANGLES = {"top-down", "floor-level", "extreme-closeup", "top-down aerial", "floor-level POV", "extreme close-up"}


class PromptBuildError(RuntimeError):
    pass


@dataclass
class PromptBundle:
    template_name: str
    template_path: Path
    final_prompt: str
    duration: int | None
    aspect_ratio: str
    model: str
    raw_template: dict[str, Any]
    params_used: dict[str, str]
    validations_applied: list[str] = field(default_factory=list)


def load_template(template_path: Path) -> dict[str, Any]:
    if not template_path.exists():
        raise PromptBuildError(f"Template não existe: {template_path}")
    raw = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise PromptBuildError(f"Template inválido (não é dict): {template_path}")
    return raw


def resolve_template(template_name: str) -> Path:
    """Aceita 'dop_top_down' (procura em subdirs) ou path absoluto."""
    p = Path(template_name)
    if p.is_absolute() and p.exists():
        return p

    for subdir in ("cinematic", "viral_reels", "ads", "ugc"):
        candidate = TEMPLATES_DIR / subdir / f"{template_name}.yaml"
        if candidate.exists():
            return candidate

    raise PromptBuildError(
        f"Template {template_name!r} não encontrado em {TEMPLATES_DIR}. "
        f"Subdirs verificados: cinematic/, viral_reels/, ads/, ugc/."
    )


def fill_placeholders(text: str, vars: dict[str, str]) -> tuple[str, set[str]]:
    """Retorna (filled, unresolved). Placeholders são {nome}."""
    pattern = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
    unresolved: set[str] = set()

    def repl(m: re.Match[str]) -> str:
        key = m.group(1)
        if key in vars and vars[key] is not None:
            return str(vars[key])
        unresolved.add(key)
        return m.group(0)

    return pattern.sub(repl, text), unresolved


NEGATION_PREFIXES = ("no ", "without ", "free of ", "no visible ", "not show ", "hide ", "n't ")


def _strip_negations(text: str) -> str:
    """Remove negações tipo 'no face no person'. Preserva afirmações."""
    out = text.lower()
    for prefix in NEGATION_PREFIXES:
        idx = 0
        while True:
            i = out.find(prefix, idx)
            if i < 0:
                break
            # Apaga o prefix + 1-3 palavras seguintes (cobre 'no face no person visible')
            end = i + len(prefix)
            words_eaten = 0
            while end < len(out) and words_eaten < 3:
                if out[end] in " ,.;:!?":
                    words_eaten += 1
                end += 1
            out = out[:i] + " " + out[end:]
            idx = i
    return out


def validate_no_face(prompt: str) -> list[str]:
    """Para Grupo B DoP. Retorna lista de termos proibidos encontrados (ignora negações)."""
    cleaned = _strip_negations(prompt)
    return [t for t in DOP_FORBIDDEN_TERMS if t in cleaned]


def validate_angle(prompt: str) -> bool:
    lower = prompt.lower()
    return any(angle.lower() in lower for angle in DOP_VALID_ANGLES)


def build(
    template_name: str,
    brand: BrandProfile,
    params: dict[str, str] | None = None,
) -> PromptBundle:
    template_path = resolve_template(template_name)
    tpl = load_template(template_path)

    expected_playbook = tpl.get("playbook")
    if expected_playbook and expected_playbook != brand.content_engine.playbook:
        raise PromptBuildError(
            f"Template playbook ({expected_playbook!r}) não bate com brand playbook ({brand.content_engine.playbook!r})"
        )

    defaults = dict(tpl.get("defaults", {}) or {})
    vars_for_template = dict(defaults)
    vars_for_template.update(params or {})

    vars_for_template.setdefault("brand_main", brand.raw.get("brand", {}).get("main", ""))
    vars_for_template.setdefault("voice_tone", brand.voice_tone)
    if brand.cities_primary:
        vars_for_template.setdefault("primary_city", brand.cities_primary[0])
    if brand.primary_keywords:
        vars_for_template.setdefault("primary_keyword", brand.primary_keywords[0])

    raw_prompt = tpl.get("prompt_template") or tpl.get("prompt")
    if not raw_prompt:
        raise PromptBuildError(f"Template {template_name!r} sem campo prompt_template/prompt")

    filled, unresolved = fill_placeholders(raw_prompt, {k: str(v) for k, v in vars_for_template.items()})

    required = set(tpl.get("required_params", []) or [])
    missing = required - {k for k, v in vars_for_template.items() if v not in (None, "")}
    if missing:
        raise PromptBuildError(f"Parâmetros obrigatórios faltando: {sorted(missing)}")

    if unresolved - required:
        leftover = sorted(unresolved - required)
        if leftover:
            raise PromptBuildError(f"Placeholders não resolvidos no prompt final: {leftover}")

    validations_applied: list[str] = []
    validators = tpl.get("validators", []) or []
    if "no_face_no_person" in validators:
        bad = validate_no_face(filled)
        if bad:
            raise PromptBuildError(
                f"DoP rule violation: prompt contém termos proibidos {bad}. "
                "Grupo B raw shots NUNCA mostram rosto/pessoa."
            )
        validations_applied.append("no_face_no_person")

    if "dop_valid_angle" in validators:
        if not validate_angle(filled):
            raise PromptBuildError(
                f"DoP rule violation: prompt não contém ângulo canônico ({sorted(DOP_VALID_ANGLES)}). "
                "Use top-down / floor-level / extreme close-up."
            )
        validations_applied.append("dop_valid_angle")

    return PromptBundle(
        template_name=tpl.get("name", template_path.stem),
        template_path=template_path,
        final_prompt=filled.strip(),
        duration=tpl.get("duration"),
        aspect_ratio=str(tpl.get("aspect_ratio", "9:16")),
        model=tpl.get("model", brand.content_engine.higgsfield_default_video_model),
        raw_template=tpl,
        params_used={k: str(v) for k, v in vars_for_template.items()},
        validations_applied=validations_applied,
    )


def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Monta um prompt Higgsfield a partir de template + brand")
    parser.add_argument("--client", required=True)
    parser.add_argument("--template", required=True, help="nome (sem .yaml) ou path absoluto")
    parser.add_argument("--param", action="append", default=[], help="key=value (pode repetir)")
    args = parser.parse_args()

    try:
        from .brand_loader import load_brand, BrandLoadError  # type: ignore[import-not-found]
    except ImportError:
        from brand_loader import load_brand, BrandLoadError  # type: ignore[no-redef]

    try:
        brand = load_brand(args.client)
    except BrandLoadError as e:
        print(f"[ERRO] brand: {e}", file=sys.stderr)
        return 1

    params: dict[str, str] = {}
    for kv in args.param:
        if "=" not in kv:
            print(f"[ERRO] --param malformado: {kv!r} (use key=value)", file=sys.stderr)
            return 1
        k, v = kv.split("=", 1)
        params[k.strip()] = v.strip()

    try:
        out = build(args.template, brand, params=params)
    except PromptBuildError as e:
        print(f"[ERRO] build: {e}", file=sys.stderr)
        return 2

    print(f"Template:   {out.template_name} ({out.template_path})")
    print(f"Model:      higgsfield/{out.model}")
    print(f"Duration:   {out.duration}s")
    print(f"Aspect:     {out.aspect_ratio}")
    print(f"Validations:{out.validations_applied}")
    print(f"\n--- PROMPT FINAL ---\n{out.final_prompt}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
