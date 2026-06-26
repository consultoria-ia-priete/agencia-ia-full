"""
whisper_client.py — STT via fal.ai/whisper-large-v3 com word-level timestamps.

Saída padrão: SRT com timing preciso pra legendas burned-in via Remotion.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.home() / ".claude" / ".env")


@dataclass
class TranscribeResult:
    text: str = ""
    srt: str = ""
    chunks: list = field(default_factory=list)  # [{start, end, text}]
    language: str = ""
    duration_s: float = 0.0
    elapsed_s: float = 0.0
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.text != ""


def _format_srt_timestamp(seconds: float) -> str:
    """Converte segundos pra formato SRT (HH:MM:SS,mmm)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunks_to_srt(chunks: list) -> str:
    """Converte chunks [{start, end, text}] pra string SRT."""
    lines = []
    for i, chunk in enumerate(chunks, 1):
        start = chunk.get("start") or chunk.get("timestamp", [0, 0])[0] or 0
        end = chunk.get("end") or chunk.get("timestamp", [0, 0])[1] or 0
        text = chunk.get("text", "").strip()
        if not text:
            continue
        lines.append(f"{i}")
        lines.append(f"{_format_srt_timestamp(start)} --> {_format_srt_timestamp(end)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def transcribe(
    audio_url_or_path: str | Path,
    *,
    language: str = "auto",
    chunk_level: str = "word",  # "word" | "segment"
) -> TranscribeResult:
    """
    Transcreve áudio com timestamps via fal.ai whisper-large-v3.

    Args:
        audio_url_or_path: URL pública OU path local (subido como base64 / multipart)
        language: 'pt' | 'en' | 'auto'
        chunk_level: 'word' (preferred pra legendas word-by-word) ou 'segment'

    Returns:
        TranscribeResult com .text, .srt, .chunks
    """
    result = TranscribeResult()
    start = time.time()

    if not os.getenv("FAL_KEY"):
        result.error = "FAL_KEY não definida"
        return result

    audio_input = str(audio_url_or_path)
    # Se for path local, fal_client tem helper de upload
    is_local = not (audio_input.startswith("http://") or audio_input.startswith("https://"))

    try:
        import fal_client
        if is_local:
            audio_input = fal_client.upload_file(audio_input)

        args = {
            "audio_url": audio_input,
            "task": "transcribe",
            "chunk_level": chunk_level,
            "version": "3",
        }
        if language and language != "auto":
            args["language"] = language

        response = fal_client.subscribe(
            "fal-ai/whisper",
            arguments=args,
            with_logs=False,
        )

        result.text = response.get("text", "")
        result.chunks = response.get("chunks", [])
        result.language = response.get("inferred_languages", [language])[0] if response.get("inferred_languages") else language
        result.srt = chunks_to_srt(result.chunks)
    except Exception as exc:
        result.error = f"{type(exc).__name__}: {exc}"
    finally:
        result.elapsed_s = round(time.time() - start, 2)

    return result


if __name__ == "__main__":
    import sys
    print("✓ whisper_client OK (smoke test real precisa de áudio + FAL_KEY com saldo)")
    sys.exit(0)
