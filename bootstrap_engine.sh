#!/usr/bin/env bash
echo "[*] Initializing Vitalis Engine..."
pip install -r requirements.txt
python -c "from src.graph.builder import GraphBuilder; GraphBuilder().build()"
echo "[+] Vitalis Engine fully initialized."
