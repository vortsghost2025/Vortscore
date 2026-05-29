#!/usr/bin/env python3
import os
import urllib.request
import json

def fetch_sovereign_assets():
    # Targeted directly at your FerrellSyntheticIntelligence organization
    base_url = "https://huggingface.co/FerrellSyntheticIntelligence/Vitalis_Core/resolve/main"
    target_dir = os.path.expanduser("~/vitalis_core/storage")
    os.makedirs(target_dir, exist_ok=True)
    
    # Files to synchronize from your HF repository
    assets = ["config.json"] 
    
    print("[FSI INITIALIZATION] Synchronizing assets from Hugging Face...")
    
    for asset in assets:
        url = f"{base_url}/{asset}"
        target_path = os.path.join(target_dir, asset)
        
        try:
            print(f"[FETCHING] Pulling {asset} from your repository...")
            urllib.request.urlretrieve(url, target_path)
            print(f"[SUCCESS] {asset} locked into storage.")
        except Exception as e:
            print(f"[ERROR] Failed to fetch {asset}: {e}")

if __name__ == "__main__":
    fetch_sovereign_assets()
