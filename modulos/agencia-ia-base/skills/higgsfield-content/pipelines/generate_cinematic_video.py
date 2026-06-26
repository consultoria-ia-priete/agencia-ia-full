#!/usr/bin/env python3
"""
generate_cinematic_video.py — Grupo A (cinematic-content). Vídeo 30s.

Uso:
    python generate_cinematic_video.py \\
      --client investbens-residencial-serraria \\
      --template apartment_hero_30s \\
      --param scene="modern Brazilian apartment building facade at sunset" \\
      --param emotional_beat="family arriving home after long day, warm smile silhouettes"

Aceita templates: apartment_hero_30s, lifestyle_resident_30s.
Modelo padrão: kling-3.0 (42 créditos por vídeo).
"""
from __future__ import annotations

import argparse

from _base import parse_common_args, run_video_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parse_common_args(parser)
    parser.add_argument("--id-prefix", default="cinematic", help="prefixo do manifest id")
    args = parser.parse_args()

    return run_video_pipeline(
        args,
        expected_playbook="cinematic-content",
        default_model="kling-3.0",
    )


if __name__ == "__main__":
    raise SystemExit(main())
