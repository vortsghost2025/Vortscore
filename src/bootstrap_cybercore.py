#!/usr/bin/env python3
import os
import urllib.request

def bootstrap_from_hf():
    base_url = "https://huggingface.co/FerrellSyntheticIntelligence/FSI-Vitalis-CyberCore/resolve/main"
    root_dir = os.path.expanduser("~/vitalis_core")
    
    # Core operational scripts to pull from your HF repo
    target_files = [
        "config.json",
        "fsi_main.py",
        "organism_main.py",
        "requirements.txt"
    ]
    
    print("[FSI CORE] Initializing sovereign sync from Hugging Face...")
    
    for filename in target_files:
        url = f"{base_url}/{filename}"
        target_path = os.path.join(root_dir, filename)
        
        try:
            print(f"[FETCHING] Pulling {filename} into your local space...")
            urllib.request.urlretrieve(url, target_path)
            print(f"[SUCCESS] Locked {filename}")
        except Exception as e:
            print(f"[ERROR] Could not sync {filename}: {e}")

if __name__ == "__main__":
    bootstrap_from_hf()
