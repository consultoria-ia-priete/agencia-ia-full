#!/usr/bin/env python3
"""
generate_ugc_broll.py — STUB. UGC voiceover + B-roll.

RESERVADO — decisão Alex 2026-05-14: ativar caso-a-caso.

Quando ativar:
1. Definir voz por cliente (ElevenLabs voice_id em brand-profile.voice.elevenlabs_default_voice_id)
   - alex-sscia: voz clonada do Alex (pendente clone)
   - Outros pt-BR: voz genérica pt-BR
   - Outros en-US: voz genérica en-US
2. Renomear `templates/ugc/broll_narration_15s.yaml.RESERVED` → `broll_narration_15s.yaml`
3. Implementar:
   - Geração 3-5 B-roll via Higgsfield (DoP ou Kling 3.0)
   - Voiceover via ElevenLabs TTS
   - Push pra squad video-editor (sync áudio + B-roll + legendas SRT)
"""
from __future__ import annotations

import sys


def main() -> int:
    print("[STUB] generate_ugc_broll.py — não implementado ainda.", file=sys.stderr)
    print(
        "Plano de ativação caso-a-caso. Veja templates/ugc/broll_narration_15s.yaml.RESERVED.",
        file=sys.stderr,
    )
    return 99


if __name__ == "__main__":
    raise SystemExit(main())
