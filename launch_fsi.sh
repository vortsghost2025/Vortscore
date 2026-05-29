#!/bin/bash
if [ "$1" == "--background" ]; then
    echo "[*] Launching FSI Guardian Daemon..."
    python3 -c "from src.devcore.guardian import GuardianDaemon; GuardianDaemon().run_background_cycle()"
else
    echo "[*] Initializing Interactive Sovereign IDE..."
    python3 bootstrap.py
fi
