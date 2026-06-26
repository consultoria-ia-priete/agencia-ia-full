#!/usr/bin/env python3
"""Generate high-quality blank tombstone bases via fal.ai (flux-pro)."""
import json, sys, importlib.util

spec = importlib.util.spec_from_file_location(
    "cf_fal", "$HOME/.claude/skills/creative-factory/core/fal_client.py")
cf = importlib.util.module_from_spec(spec)
sys.modules["cf_fal"] = cf  # py3.14: dataclass needs the module registered
spec.loader.exec_module(cf)

OUT = "$PROJECTS_ROOT/ALEX_SSCIA/Funis de Vendas/Funil ConsultorIA/public/assets/_work"

COMMON = (
    "a single weathered granite tombstone, rounded-top headstone with a small "
    "carved cross near the top, realistic rough carved stone texture with chips "
    "and moss stains, dramatic moody side lighting, deep shadows, dark cemetery "
    "atmosphere, a patch of detailed dark green grass tufts and dirt mound at the "
    "base, soft ground shadow cast on the earth, the large lower face of the stone "
    "is BLANK and SMOOTH ready for an inscription, no text, no letters, "
    "professional digital illustration, highly detailed, centered composition, "
    "isolated on a plain pure white background"
)
NEG = ("text, letters, words, inscription, writing, watermark, signature, "
       "flat shading, cartoon, low detail, blurry, multiple tombstones")

JOBS = [
    ("base-afiliado", COMMON),
    ("base-drop", COMMON.replace(
        "at the base,",
        "at the base, a worn brown cardboard delivery box sitting on the ground "
        "in front of the stone,")),
    ("base-info", COMMON.replace(
        "at the base,",
        "at the base, an old vintage computer monitor with a cracked screen "
        "resting on the ground in front of the stone,")),
]

reqs = [dict(prompt=p + ". Negative: " + NEG, slide_id=s, model="flux-pro",
             image_size="portrait_4_3", num_inference_steps=40,
             guidance_scale=4.0, seed=778899) for s, p in JOBS]

print("Generating", len(reqs), "bases via flux-pro ...")
results = cf.generate_batch(reqs, max_parallel=3)
manifest = {}
for r in results:
    print(f"[{r.slide_id}] ok={r.ok} elapsed={r.elapsed_s}s err={r.error}")
    if r.ok:
        manifest[r.slide_id] = r.image_url
with open(OUT + "/bases_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print("manifest:", json.dumps(manifest, indent=2))
