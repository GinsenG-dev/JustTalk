#!/usr/bin/env sh

set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

cleanup() {
  if [ -n "${BACKEND_PID:-}" ]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
  if [ -n "${FRONTEND_PID:-}" ]; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

if [ ! -d "$BACKEND_DIR/.venv" ]; then
  python3 -m venv "$BACKEND_DIR/.venv"
fi

. "$BACKEND_DIR/.venv/bin/activate"
pip install -r "$BACKEND_DIR/requirements.txt"

export DATABASE_URL="sqlite:///./justtalk.db"
cd "$BACKEND_DIR"
python -c "from app.db.database import Base, engine; from app.models import user; Base.metadata.create_all(bind=engine)"
alembic upgrade head
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

cd "$FRONTEND_DIR"
npm install
npm run dev -- --host 127.0.0.1 --port 5173 &
FRONTEND_PID=$!

wait "$BACKEND_PID" "$FRONTEND_PID"
