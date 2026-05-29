#!/bin/bash
# Vitalis Intelligence Sovereign Bootstrapper

echo "[BOOT] Initializing Ferrell Synthetic Intelligence..."

# 1. Environment Verification
if [ ! -f "env.json" ]; then
    echo "{\"status\": \"initialized\"}" > env.json
fi

# 2. Integrity Check (Pre-Flight)
# Ensure the ledger exists and core files are present
if [ ! -d "core" ]; then
    echo "[!] CRITICAL: Core architecture missing."
    exit 1
fi

echo "[BOOT] Integrity Verified. Launching NSE..."

# 3. Execution
python3 nse_init.py
