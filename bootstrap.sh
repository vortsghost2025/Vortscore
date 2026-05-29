#!/bin/bash
# FSI Vitalis_Core Native Bootstrap

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "[+] Initializing localized virtual environment..."
    python3 -m venv "$PROJECT_ROOT/.venv"
fi

source "$PROJECT_ROOT/.venv/bin/activate"

if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo "[+] Synchronizing framework dependencies..."
    pip install -r "$PROJECT_ROOT/requirements.txt"
fi

echo "[+] FSI Sovereign Core Environment Active."
