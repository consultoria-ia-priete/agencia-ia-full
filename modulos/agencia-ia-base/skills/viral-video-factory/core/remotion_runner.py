"""
remotion_runner.py — wrapper pra rodar Remotion render via Node.js.

Premissa: o projeto Remotion mora em ~/.claude/skills/viral-video-factory/remotion-project/
e precisa ser instalado UMA VEZ (`npm install`). Depois renders são fast.

Fluxo:
  1. Garantir node_modules instalado (1ª execução = 5min, depois cacheado)
  2. Escrever input.json com {audio, slides, captions, brand} no remotion-project/data/
  3. Rodar: npx remotion render src/index.ts ViralShort out.mp4 --props=data/input.json
  4. Retornar path do MP4 gerado
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

REMOTION_DIR = Path(__file__).parent.parent / "remotion-project"


@dataclass
class RenderResult:
    output_path: str = ""
    width: int = 0
    height: int = 0
    duration_s: float = 0.0
    elapsed_s: float = 0.0
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and Path(self.output_path).is_file()


def ensure_remotion_installed() -> tuple[bool, str]:
    """Verifica se node_modules existe; se não, sugere `npm install`."""
    if not (REMOTION_DIR / "node_modules").is_dir():
        return False, (
            f"Remotion não instalado. Rodar 1x:\n"
            f"  cd {REMOTION_DIR} && npm install\n"
            f"(~5 min de download, depois renders são instantâneos)"
        )
    return True, "Remotion instalado"


def render(
    *,
    composition_id: str = "ViralShort",
    props: dict,
    output_path: str | Path,
    width: int = 1080,
    height: int = 1920,
    fps: int = 30,
) -> RenderResult:
    """
    Renderiza vídeo Remotion.

    Args:
        composition_id: nome da composition em src/Root.tsx
        props: dict que vai ser passado como --props (slides, audio, captions, brand)
        output_path: path do MP4 final
        width, height: dimensões (default 9:16 Reels)
        fps: 30 (default), 60 pra mais fluido (mais custo)
    """
    result = RenderResult()

    ok, msg = ensure_remotion_installed()
    if not ok:
        result.error = msg
        return result

    if not shutil.which("npx"):
        result.error = "npx não está no PATH — instalar Node.js (recomendo via brew install node)"
        return result

    output_path = Path(output_path).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Salva props como input.json
    props_path = REMOTION_DIR / "data" / "input.json"
    props_path.parent.mkdir(parents=True, exist_ok=True)
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2))

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts",
        composition_id,
        str(output_path),
        f"--props={props_path}",
        f"--width={width}",
        f"--height={height}",
        f"--fps={fps}",
        "--codec=h264",
    ]

    try:
        import time
        start = time.time()
        proc = subprocess.run(
            cmd,
            cwd=str(REMOTION_DIR),
            capture_output=True,
            text=True,
            timeout=600,  # 10 min hard cap
        )
        result.elapsed_s = round(time.time() - start, 2)
        if proc.returncode != 0:
            result.error = f"Remotion falhou (exit {proc.returncode}): {proc.stderr[-500:]}"
            return result
        result.output_path = str(output_path)
        result.width = width
        result.height = height
    except subprocess.TimeoutExpired:
        result.error = "Remotion render timed out (>10min)"
    except Exception as exc:
        result.error = f"{type(exc).__name__}: {exc}"

    return result


if __name__ == "__main__":
    import sys
    ok, msg = ensure_remotion_installed()
    print(f"{'✓' if ok else '✗'} {msg}")
    sys.exit(0 if ok else 1)
