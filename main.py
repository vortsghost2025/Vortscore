import sys
import os
import threading
from flask import Flask, request, jsonify
# Using absolute imports from the current project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ide_kernel.daemon import KernelDaemon
from src.ide_kernel.gateway import app

def start_daemon():
    print("[*] Starting Daemon Thread...")
    daemon = KernelDaemon(os.getcwd())
    daemon.start()

if __name__ == "__main__":
    print("[*] Booting Unified FSI Kernel...")
    
    # Start Daemon as a background thread
    daemon_thread = threading.Thread(target=start_daemon, daemon=True)
    daemon_thread.start()
    
    # Run Gateway in the main thread
    print("[+] System Operational. Gateway at http://127.0.0.1:5001")
    app.run(port=5001, debug=False, use_reloader=False)
