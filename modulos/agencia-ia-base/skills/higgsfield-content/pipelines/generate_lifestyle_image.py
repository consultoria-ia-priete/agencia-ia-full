#!/usr/bin/env python3
"""
generate_lifestyle_image.py — Grupo A (cinematic-content). Imagem lifestyle 2K.

Uso:
    python generate_lifestyle_image.py \\
      --client ballarin-sou-viver-milao \\
      --template nano_banana_2k_image \\
      --param subject="modern kitchen counter with fresh flowers, morning light" \\
      --param mood="warm, lived-in, family kitchen"

Cadência típica: 5/sem por cliente Grupo A.
Modelo padrão: nano-banana-2k (2 créditos por imagem).
"""
from __future__ import annotations

import argparse

from _base import parse_common_args, run_image_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parse_common_args(parser)
    parser.add_argument("--num-images", type=int, default=1, help="quantas imagens gerar (default 1)")
    parser.add_argument("--id-prefix", default="lifestyle", help="prefixo do manifest id")
    args = parser.parse_args()

    return run_image_pipeline(
        args,
        expected_playbook="cinematic-content",
        default_model="nano-banana-2k",
        num_images=args.num_images,
    )


if __name__ == "__main__":
    raise SystemExit(main())
