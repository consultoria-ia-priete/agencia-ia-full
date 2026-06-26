"""
higgsfield_helper.py — constrói o payload que Claude vai passar pro MCP higgsfield.

Importante: a chamada MCP **é feita pelo Claude na sessão atual**, não por este script.
Esse helper só prepara o payload em formato canônico + estima créditos + valida limites.

Tools MCP esperadas (nomes a confirmar no primeiro boot do plano Higgsfield):
- mcp__claude_ai_Higgsfield__generate_video
- mcp__claude_ai_Higgsfield__generate_image
- mcp__claude_ai_Higgsfield__media_upload  (pra UGC com input do cliente)
- mcp__claude_ai_Higgsfield__media_confirm
- mcp__claude_ai_Higgsfield__job_status

Modelos disponíveis (memória 2026-04-30):
- video: dop, kling-3.0, seedance-2.0, veo-3.1, sora-2
- image: nano-banana-2k, nano-banana-pro, flux-2
- char: soul-2.0 (avatar consistency — reservado, não usar até Alex aprovar)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

MODEL_CREDITS = {
    "dop": 12,
    "kling-3.0": 42,
    "seedance-2.0": 42,
    "veo-3.1": 50,
    "sora-2": 60,
    "nano-banana-2k": 2,
    "nano-banana-pro": 4,
    "flux-2": 3,
}

VALID_ASPECT_RATIOS = {"9:16", "1:1", "4:5", "16:9", "3:4"}


@dataclass
class HiggsfieldVideoPayload:
    """Args canônicos pra mcp__claude_ai_Higgsfield__generate_video."""
    prompt: str
    model: str
    duration: int
    aspect_ratio: str
    seed: int | None = None
    reference_image_url: str | None = None
    use_soul_character: bool = False
    soul_character_id: str | None = None

    def to_mcp_args(self) -> dict[str, Any]:
        args: dict[str, Any] = {
            "prompt": self.prompt,
            "model": self.model,
            "duration": self.duration,
            "aspect_ratio": self.aspect_ratio,
        }
        if self.seed is not None:
            args["seed"] = self.seed
        if self.reference_image_url:
            args["reference_image_url"] = self.reference_image_url
        if self.use_soul_character and self.soul_character_id:
            args["soul_character_id"] = self.soul_character_id
        return args


@dataclass
class HiggsfieldImagePayload:
    """Args canônicos pra mcp__claude_ai_Higgsfield__generate_image."""
    prompt: str
    model: str
    aspect_ratio: str
    seed: int | None = None
    num_images: int = 1
    reference_image_url: str | None = None

    def to_mcp_args(self) -> dict[str, Any]:
        args: dict[str, Any] = {
            "prompt": self.prompt,
            "model": self.model,
            "aspect_ratio": self.aspect_ratio,
            "num_images": self.num_images,
        }
        if self.seed is not None:
            args["seed"] = self.seed
        if self.reference_image_url:
            args["reference_image_url"] = self.reference_image_url
        return args


def estimate_credits(model: str, count: int = 1) -> int:
    base = MODEL_CREDITS.get(model)
    if base is None:
        raise ValueError(f"Modelo Higgsfield desconhecido: {model!r}. Conhecidos: {sorted(MODEL_CREDITS)}")
    return base * count


def validate_video_request(payload: HiggsfieldVideoPayload) -> list[str]:
    issues: list[str] = []
    if payload.model not in MODEL_CREDITS:
        issues.append(f"Modelo desconhecido: {payload.model!r}")
    if payload.aspect_ratio not in VALID_ASPECT_RATIOS:
        issues.append(f"aspect_ratio inválido: {payload.aspect_ratio!r}")
    if payload.duration < 1 or payload.duration > 60:
        issues.append(f"duration fora do range razoável (1-60s): {payload.duration}")
    if payload.model == "dop" and payload.duration > 10:
        issues.append("DoP é otimizado pra 5-7s. Duration alto pode degradar qualidade.")
    if payload.use_soul_character and not payload.soul_character_id:
        issues.append("use_soul_character=True mas soul_character_id ausente")
    return issues


def build_video_payload(
    prompt: str,
    model: str,
    duration: int,
    aspect_ratio: str,
    *,
    seed: int | None = None,
    reference_image_url: str | None = None,
    use_soul_character: bool = False,
    soul_character_id: str | None = None,
) -> HiggsfieldVideoPayload:
    return HiggsfieldVideoPayload(
        prompt=prompt,
        model=model,
        duration=duration,
        aspect_ratio=aspect_ratio,
        seed=seed,
        reference_image_url=reference_image_url,
        use_soul_character=use_soul_character,
        soul_character_id=soul_character_id,
    )


def build_image_payload(
    prompt: str,
    model: str,
    aspect_ratio: str,
    *,
    seed: int | None = None,
    num_images: int = 1,
    reference_image_url: str | None = None,
) -> HiggsfieldImagePayload:
    return HiggsfieldImagePayload(
        prompt=prompt,
        model=model,
        aspect_ratio=aspect_ratio,
        seed=seed,
        num_images=num_images,
        reference_image_url=reference_image_url,
    )


def claude_call_instructions(payload: HiggsfieldVideoPayload | HiggsfieldImagePayload) -> str:
    """
    Texto que o pipeline imprime pra orientar Claude (mediador) a fazer a chamada MCP.
    Não substitui a chamada — é só uma instrução de qual tool invocar com quais args.
    """
    kind = "video" if isinstance(payload, HiggsfieldVideoPayload) else "image"
    tool = f"mcp__claude_ai_Higgsfield__generate_{kind}"
    args = payload.to_mcp_args()
    import json as _json
    return (
        f"### CLAUDE INSTRUCTION\n"
        f"Invoke MCP tool: {tool}\n"
        f"With arguments:\n```json\n{_json.dumps(args, indent=2, ensure_ascii=False)}\n```\n"
        f"After response, save resulting URL/path to the manifest.json in the output dir."
    )
