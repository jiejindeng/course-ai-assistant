#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ ! -d "$ROOT/backend/.venv" ]]; then echo "请先按 README.md 创建 backend/.venv 并安装 requirements.txt"; exit 1; fi
if [[ ! -d "$ROOT/frontend/node_modules" ]]; then echo "请先在 frontend 执行 npm install"; exit 1; fi
(cd "$ROOT/backend" && source .venv/bin/activate && uvicorn main:app --reload --port 8000) &
BACK_PID=$!
(cd "$ROOT/frontend" && npm run dev) &
FRONT_PID=$!
trap 'kill "$BACK_PID" "$FRONT_PID" 2>/dev/null || true' EXIT INT TERM
wait
