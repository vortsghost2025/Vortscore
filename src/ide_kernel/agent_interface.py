import json
import os
import sys

def submit_task(intent, file_path, code_content):
    workspace = os.getcwd()
    task_file = os.path.join(workspace, "workspace_tasks.json")
    
    task = {
        "intent": intent,
        "file": file_path,
        "code": code_content
    }
    
    with open(task_file, 'w') as f:
        json.dump(task, f)
    
    print(f"[+] Task '{intent}' sent to FSI Kernel for synthesis.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 -m src.ide_kernel.agent_interface <intent> <file> <code>")
    else:
        submit_task(sys.argv[1], sys.argv[2], sys.argv[3])
