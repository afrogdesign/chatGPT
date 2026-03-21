#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MARKER_FILE="$ROOT_DIR/.setup_done"

cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

if [ ! -f "$MARKER_FILE" ]; then
  pip install -q -r requirements.txt
  python -m playwright install chromium
  touch "$MARKER_FILE"
fi

python src/main.py
