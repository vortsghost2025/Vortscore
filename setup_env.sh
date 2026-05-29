#!/bin/bash
pip install pydantic==2.7.1 pytest==8.2.0 ruff==0.4.0 mypy==1.10.0
# Ensure local paths are discoverable
export PYTHONPATH=$PYTHONPATH:.
echo "[+] Environment secured."
