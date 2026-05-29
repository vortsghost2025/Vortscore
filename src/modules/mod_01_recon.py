import os
import platform

def perform_recon():
    print("[RECON] Initiating environment scan...")
    data = {
        "os": platform.system(),
        "release": platform.release(),
        "node": platform.node(),
        "user": os.getlogin() if hasattr(os, 'getlogin') else "unknown"
    }
    print(f"[RECON] Data gathered: {data}")
    return data

if __name__ == "__main__":
    perform_recon()
