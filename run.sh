#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$APP_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

if [ -f "$APP_DIR/requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -q -r "$APP_DIR/requirements.txt"
fi

echo "Starting Rsync GUI..."
exec python3 -m src
