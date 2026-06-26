#!/usr/bin/env python3
"""
generate_viral_reel.py — Grupo B (viral-reels-seo). Reel 7s vertical DoP.

Uso:
    python generate_viral_reel.py \\
      --client floor-to-ceiling \\
      --template dop_top_down \\
      --param subject="vacuum on plush carpet" \\
      --param action="moving in slow rhythmic lines"

Aceita os 3 templates: dop_top_down, dop_floor_level, dop_extreme_closeup.
Imprime instruções pra Claude chamar `mcp__claude_ai_Higgsfield__generate_video`.
"""
from __future__ import annotations

import argparse

from _base import parse_common_args, run_video_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parse_common_args(parser)
    parser.add_argument("--id-prefix", default="reel", help="prefixo do manifest id")
    args = parser.parse_args()

    return run_video_pipeline(
        args,
        expected_playbook="viral-reels-seo",
        default_model="dop",
    )


if __name__ == "__main__":
    raise SystemExit(main())
