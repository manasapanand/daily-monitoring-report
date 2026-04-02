#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if [ ! -f "$VENV_DIR/.deps_installed" ] || [ "$SCRIPT_DIR/requirements.txt" -nt "$VENV_DIR/.deps_installed" ]; then
  echo "Installing dependencies..."
  python -m pip install --upgrade pip
  pip install -r "$SCRIPT_DIR/requirements.txt"
  touch "$VENV_DIR/.deps_installed"
fi

exec streamlit run "$SCRIPT_DIR/app.py"
