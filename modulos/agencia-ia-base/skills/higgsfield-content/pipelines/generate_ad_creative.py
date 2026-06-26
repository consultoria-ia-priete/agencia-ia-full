#!/usr/bin/env python3
"""
generate_ad_creative.py — Ads creative pra Meta Ads. Invocado pela squad meta-ads-copy.

Uso (vídeo UGC vertical):
    python generate_ad_creative.py \\
      --client ballarin-sou-viver-milao \\
      --template meta_ugc_vertical_9_16 \\
      --kind video \\
      --param hook_visual="hands holding apartment keys close-up" \\
      --param product_or_service="2-bedroom apartment Sou Viver Milão" \\
      --param cta_visual="WhatsApp QR code on phone screen"

Uso (imagem estática 1:1):
    python generate_ad_creative.py \\
      --client alex-sscia \\
      --template meta_static_1_1 \\
      --kind image \\
      --param subject="Alex working with laptop, focused expression" \\
      --param headline_visual_concept="33K em 90 dias"

Requer brand-profile.content_engine.ads_enabled == true. Falha cedo se não.
"""
from __future__ import annotations

import argparse
import sys

from _base import (
    load_brand_safe,
    parse_common_args,
    run_image_pipeline,
    run_video_pipeline,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parse_common_args(parser)
    parser.add_argument(
        "--kind",
        choices=["video", "image"],
        required=True,
        help="vídeo (UGC, TV spot) ou imagem (static, carousel)",
    )
    parser.add_argument("--num-images", type=int, default=1, help="só pra --kind=image")
    parser.add_argument("--id-prefix", default="ad", help="prefixo do manifest id")
    args = parser.parse_args()

    brand = load_brand_safe(args.client, expected_playbook=None)
    if not brand.content_engine.ads_enabled:
        print(
            f"[ERRO] {brand.slug} tem content_engine.ads_enabled=false. "
            f"Esse cliente não está habilitado pra ads. Atualize o brand-profile primeiro.",
            file=sys.stderr,
        )
        return 5

    if args.kind == "video":
        return run_video_pipeline(args, expected_playbook=None)
    return run_image_pipeline(
        args,
        expected_playbook=None,
        num_images=args.num_images,
    )


if __name__ == "__main__":
    raise SystemExit(main())
