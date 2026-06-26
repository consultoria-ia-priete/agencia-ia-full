"""
publish_from_pipeline.py — Wrapper persistente para publicar carrosseis do daily-pipeline
em IG + LI imediato. Usado por plists launchd em vez de scripts /tmp (que somem).

Uso:
    python3 publish_from_pipeline.py <pipeline-dir> <C##>

Exemplo:
    python3 publish_from_pipeline.py /path/.../pipeline-daily/2026-04-29 C20

Le:
- <pipeline-dir>/C##.json   -> caption (campo "caption")
- <pipeline-dir>/cdn-urls.json -> URLs CDN do carrossel (8 slides)

Publica em IG + LI usando create_immediate_post (status=published, sem bug platform=google).
"""
import sys
import json
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from create_post import create_immediate_post


def publish(pipeline_dir: str, carousel: str) -> int:
    cdn_path = os.path.join(pipeline_dir, "cdn-urls.json")
    json_path = os.path.join(pipeline_dir, f"{carousel}.json")

    if not os.path.exists(cdn_path):
        print(f"ERRO: cdn-urls.json nao encontrado em {cdn_path}", file=sys.stderr)
        return 2
    if not os.path.exists(json_path):
        print(f"ERRO: {carousel}.json nao encontrado em {json_path}", file=sys.stderr)
        return 2

    cdn = json.load(open(cdn_path))
    if carousel not in cdn or len(cdn[carousel]) != 8:
        print(f"ERRO: {carousel} nao tem 8 URLs em cdn-urls.json", file=sys.stderr)
        return 3

    cdata = json.load(open(json_path))
    caption = cdata.get("caption", "").strip()
    if not caption:
        print(f"ERRO: caption vazia em {json_path}", file=sys.stderr)
        return 4

    urls = cdn[carousel]
    print(f"=== Publicando {carousel} ({len(urls)} slides) ===")

    failures = 0
    for platform in ["instagram", "linkedin"]:
        try:
            res = create_immediate_post(platform, urls, caption)
            print(f"  OK {carousel}-{platform}: criado")
            time.sleep(1.5)
        except Exception as e:
            print(f"  FAIL {carousel}-{platform}: {e}", file=sys.stderr)
            failures += 1

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 publish_from_pipeline.py <pipeline-dir> <C##>", file=sys.stderr)
        sys.exit(1)
    sys.exit(publish(sys.argv[1], sys.argv[2].upper()))
