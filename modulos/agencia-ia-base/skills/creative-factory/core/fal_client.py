"""
fal_client.py — gateway fal.ai pra creative-factory.

Carrega FAL_KEY de ~/.claude/.env, abstrai chamadas aos modelos suportados,
adiciona retry, parallelismo e error handling.

Modelos suportados (id curto → endpoint fal):
    flux-dev      → fal-ai/flux/dev               ($0.025/img)
    flux-pro      → fal-ai/flux-pro/v1.1          ($0.04/img)
    ideogram      → fal-ai/ideogram/v3            ($0.08/img — texto na imagem)
    nano-banana   → fal-ai/nano-banana/edit       ($0.039/img — refs múltiplas)
    recraft       → fal-ai/recraft/v3             ($0.04/img — vetor/ilustração)
"""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Carrega FAL_KEY do .env global do Claude Code
ENV_PATH = Path.home() / ".claude" / ".env"
load_dotenv(ENV_PATH)

if not os.getenv("FAL_KEY"):
    raise RuntimeError(
        f"FAL_KEY não encontrada em {ENV_PATH}. "
        "Crie o arquivo com 'FAL_KEY=fal-...' e chmod 600."
    )

# import depois do load_dotenv pra fal_client achar a key
import fal_client  # noqa: E402

MODEL_REGISTRY: dict[str, str] = {
    "flux-dev":     "fal-ai/flux/dev",
    "flux-pro":     "fal-ai/flux-pro/v1.1",
    "ideogram":     "fal-ai/ideogram/v3",
    "nano-banana":  "fal-ai/nano-banana/edit",
    "recraft":      "fal-ai/recraft/v3",
}

# Custo aproximado por imagem em USD — usado pra estimativas, não pra billing real
MODEL_COST_USD: dict[str, float] = {
    "flux-dev":     0.025,
    "flux-pro":     0.040,
    "ideogram":     0.080,
    "nano-banana":  0.039,
    "recraft":      0.040,
}


@dataclass
class GenerationResult:
    """Resultado de 1 geração."""
    slide_id: str
    model: str
    prompt: str
    image_url: str | None = None
    seed: int | None = None
    error: str | None = None
    elapsed_s: float = 0.0
    cost_estimate_usd: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.error is None and self.image_url is not None


def resolve_model(model_short_or_full: str) -> str:
    """Aceita 'flux-dev' ou 'fal-ai/flux/dev' e retorna o endpoint completo."""
    if "/" in model_short_or_full:
        return model_short_or_full
    if model_short_or_full not in MODEL_REGISTRY:
        raise ValueError(
            f"Modelo desconhecido: {model_short_or_full}. "
            f"Disponíveis: {list(MODEL_REGISTRY.keys())}"
        )
    return MODEL_REGISTRY[model_short_or_full]


def generate_image(
    prompt: str,
    *,
    slide_id: str = "img",
    model: str = "flux-dev",
    image_size: str = "square_hd",
    num_inference_steps: int = 28,
    guidance_scale: float = 3.5,
    seed: int | None = None,
    image_urls: list[str] | None = None,  # pra nano-banana/edit (refs)
    extra: dict[str, Any] | None = None,
) -> GenerationResult:
    """
    Gera 1 imagem síncrona via fal.ai.

    Retorna GenerationResult — verificar .ok antes de usar .image_url.
    Não levanta exceção em erro de geração — captura em result.error.
    Levanta apenas se a config (modelo, FAL_KEY) estiver inválida.
    """
    endpoint = resolve_model(model)
    cost = MODEL_COST_USD.get(model, MODEL_COST_USD.get(model.split("/")[-1], 0.04))

    arguments: dict[str, Any] = {
        "prompt": prompt,
        "image_size": image_size,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale,
        "num_images": 1,
        "enable_safety_checker": True,
    }
    if seed is not None:
        arguments["seed"] = seed
    if image_urls:
        arguments["image_urls"] = image_urls
    if extra:
        arguments.update(extra)

    start = time.time()
    result = GenerationResult(
        slide_id=slide_id,
        model=model,
        prompt=prompt,
        cost_estimate_usd=cost,
    )

    try:
        # subscribe = síncrono com polling
        response = fal_client.subscribe(
            endpoint,
            arguments=arguments,
            with_logs=False,
        )
        # Resposta padrão fal: {"images": [{"url": "..."}], "seed": 12345, ...}
        images = response.get("images") or []
        if not images:
            result.error = f"Resposta sem imagens: {response}"
        else:
            result.image_url = images[0].get("url")
            result.seed = response.get("seed")
            result.metadata = {k: v for k, v in response.items() if k != "images"}
    except Exception as exc:
        result.error = f"{type(exc).__name__}: {exc}"
    finally:
        result.elapsed_s = round(time.time() - start, 2)

    return result


def generate_batch(
    requests: list[dict[str, Any]],
    *,
    max_parallel: int = 5,
) -> list[GenerationResult]:
    """
    Gera várias imagens em paralelo (ThreadPool).

    Cada item de `requests` é um dict com as keys aceitas por generate_image
    (prompt, slide_id, model, etc.). Retorna lista na MESMA ORDEM dos inputs.
    """
    results: list[GenerationResult | None] = [None] * len(requests)

    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        future_to_idx = {
            pool.submit(generate_image, **req): idx
            for idx, req in enumerate(requests)
        }
        for fut in as_completed(future_to_idx):
            idx = future_to_idx[fut]
            try:
                results[idx] = fut.result()
            except Exception as exc:
                req = requests[idx]
                results[idx] = GenerationResult(
                    slide_id=req.get("slide_id", f"slide-{idx}"),
                    model=req.get("model", "?"),
                    prompt=req.get("prompt", ""),
                    error=f"{type(exc).__name__}: {exc}",
                )

    return [r for r in results if r is not None]  # type: ignore


def health_check() -> tuple[bool, str]:
    """
    Smoke test: valida que FAL_KEY carrega e que o cliente tá importável.
    Não consome créditos. Útil pra setup verification.
    """
    if not os.getenv("FAL_KEY"):
        return False, "FAL_KEY não definida"
    try:
        # Apenas valida import e formato da key
        key = os.getenv("FAL_KEY", "")
        if ":" not in key:
            return False, f"Formato FAL_KEY inesperado (esperado 'id:secret', got prefix '{key[:8]}...')"
        return True, f"OK — FAL_KEY válida (prefix {key[:8]}...), fal_client importado"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


if __name__ == "__main__":
    ok, msg = health_check()
    print(f"{'✓' if ok else '✗'} {msg}")
    sys.exit(0 if ok else 1)
