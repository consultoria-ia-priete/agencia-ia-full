"""
elevenlabs_client.py — TTS via ElevenLabs (preferencialmente via fal.ai gateway).

Estratégia:
  • Usa fal.ai/elevenlabs/tts (custos no FAL_KEY existente, sem 2ª chave)
  • Fallback: ELEVENLABS_API_KEY direto se passada via env

Vozes default por idioma (override via brand-profile):
  EN-US feminina warm   → Rachel
  EN-US masculina       → Antoni
  PT-BR feminina        → (a definir após sample test)
  PT-BR masculina       → (a definir após sample test)
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv(Path.home() / ".claude" / ".env")

DEFAULT_VOICES = {
    "en-US-female-warm":      "21m00Tcm4TlvDq8ikWAM",  # Rachel
    "en-US-male-technical":   "ErXwobaYiN019PkySvjV",  # Antoni
    "en-US-male-confident":   "TxGEqnHWrfWFTfGW9XjX",  # Josh
    "pt-BR-female":           "",                       # TBD
    "pt-BR-male":             "",                       # TBD
}


@dataclass
class TTSResult:
    audio_url: str | None = None
    audio_local_path: str | None = None
    duration_s: float = 0.0
    voice_id: str = ""
    text: str = ""
    cost_estimate_usd: float = 0.0
    elapsed_s: float = 0.0
    error: str | None = None
    metadata: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.error is None and self.audio_url is not None


def estimate_cost(text: str) -> float:
    """ElevenLabs cobra ~ $0.30 / 1k caracteres no plano standard.
    Via fal.ai pode variar. Ajustar quando confirmado."""
    chars = len(text)
    return round((chars / 1000) * 0.30, 4)


def synthesize(
    text: str,
    *,
    voice_id: str,
    model_id: str = "eleven_multilingual_v2",
    out_path: str | Path | None = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> TTSResult:
    """
    Gera voiceover via fal.ai/elevenlabs/tts.

    Args:
        text: roteiro pra falar (até ~5000 chars)
        voice_id: ElevenLabs voice ID
        model_id: 'eleven_multilingual_v2' (PT/EN), 'eleven_turbo_v2' (mais rápido)
        out_path: se passado, baixa o MP3 pra esse path
        stability: 0-1, 0.5 default (mais alto = mais consistente, menos expressivo)
        similarity_boost: 0-1

    Returns:
        TTSResult — verificar .ok antes de usar .audio_url
    """
    result = TTSResult(text=text, voice_id=voice_id, cost_estimate_usd=estimate_cost(text))
    start = time.time()

    if not os.getenv("FAL_KEY"):
        result.error = "FAL_KEY não definida em ~/.claude/.env"
        return result

    if not voice_id:
        result.error = "voice_id vazio — preencher brand-profile.voice.elevenlabs_default_voice_id"
        return result

    try:
        import fal_client
        response = fal_client.subscribe(
            "fal-ai/elevenlabs/tts/multilingual-v2",
            arguments={
                "text": text,
                "voice": voice_id,
                "stability": stability,
                "similarity_boost": similarity_boost,
            },
            with_logs=False,
        )
        # Resposta padrão: {"audio": {"url": "..."}}
        audio = response.get("audio", {})
        result.audio_url = audio.get("url") or response.get("audio_url")
        result.metadata = {k: v for k, v in response.items() if k != "audio"}

        if result.audio_url and out_path:
            import urllib.request
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(result.audio_url, str(out_path))
            result.audio_local_path = str(out_path)
    except Exception as exc:
        result.error = f"{type(exc).__name__}: {exc}"
    finally:
        result.elapsed_s = round(time.time() - start, 2)

    return result


def health_check() -> tuple[bool, str]:
    if not os.getenv("FAL_KEY"):
        return False, "FAL_KEY não definida"
    try:
        import fal_client  # noqa: F401
        return True, "OK — fal_client importável, FAL_KEY presente. Smoke real só com saldo."
    except ImportError as exc:
        return False, f"fal-client não instalado: {exc}"


if __name__ == "__main__":
    import sys
    ok, msg = health_check()
    print(f"{'✓' if ok else '✗'} {msg}")
    sys.exit(0 if ok else 1)
