#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  echo "[info] creating .venv"
  python3 -m venv .venv
fi

source .venv/bin/activate

python -m pip install -q -U pip
python -m pip install -q -e . pytest
python -m playwright install chromium

echo "[info] running syntax coverage test"
pytest -q tests/test_diagram_syntax_coverage.py

OUT_DIR="artifacts/all-diagrams"
mkdir -p "$OUT_DIR"

echo "[info] rendering all diagrams (svg/png/pdf) -> $OUT_DIR"
python - <<'PY'
import asyncio
from pathlib import Path
from tests.test_diagram_syntax_coverage import DIAGRAMS
from mermaid_cli import render_mermaid

out = Path("artifacts/all-diagrams")
out.mkdir(parents=True, exist_ok=True)

async def main():
    count = 0
    for name, definition in DIAGRAMS.items():
        for fmt in ("svg", "png", "pdf"):
            _, _, data = await render_mermaid(definition, output_format=fmt, quiet=True)
            (out / f"{name}.{fmt}").write_bytes(data)
            count += 1
    print(f"generated {count} files in {out}")

asyncio.run(main())
PY

echo "[done] open artifacts with: open $OUT_DIR"
