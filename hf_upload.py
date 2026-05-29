#!/usr/bin/env python3
import os
import sys
from huggingface_hub import HfApi, login

def deploy():
    print("[*] Initiating Ferrell Synthetic Intelligence Hugging Face Deployment Sequence...")
    
    token = input("Enter your Hugging Face Write Access Token: ").strip()
    if not token:
        print("[-] Absolute token signature required. Deployment aborted.")
        sys.exit(1)
        
    repo_id = input("Enter target Repository ID (e.g., 'your-username/vitalis-core'): ").strip()
    if not repo_id:
        print("[-] Target repository layout specification mismatch.")
        sys.exit(1)

    try:
        login(token=token)
        api = HfApi()
        
        print(f"[*] Creating repository context mapping for: {repo_id}")
        api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
        
        print("[*] Uploading core architecture tree structures safely to Hugging Face...")
        target_paths = ["core", "src", "extensions", "app.py", "run_vitalis.py", "requirements.txt", "README.md"]
        
        for item in target_paths:
            local_path = os.path.expanduser(f"~/vitalis_core/{item}")
            if os.path.exists(local_path):
                print(f"[+] Syncing item: {item}")
                if os.path.isdir(local_path):
                    api.upload_folder(
                        folder_path=local_path,
                        path_in_repo=item,
                        repo_id=repo_id,
                        repo_type="model"
                    )
                else:
                    api.upload_file(
                        path_or_fileobj=local_path,
                        path_in_repo=item,
                        repo_id=repo_id,
                        repo_type="model"
                    )
                    
        print(f"\n[+] Production Deployment Complete. Model package accessible at: https://huggingface.co/{repo_id}")
    except Exception as e:
        print(f"[-] Critical failure during asset transmission: {e}")

if __name__ == "__main__":
    deploy()
