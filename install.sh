#!/bin/bash
echo "[*] Installing FSI Sovereign IDE..."
# Verify Python environment
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: Python3 not found. Please install Python3."
    exit 1
fi
# Set permissions
chmod +x launch_fsi.sh
echo "[+] Installation complete. Run './launch_fsi.sh' to start."
