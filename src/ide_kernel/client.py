import sys
import requests
import json

def dispatch(intent, payload):
    url = "http://127.0.0.1:5001/execute"
    data = {"intent": intent}
    data.update(payload)
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 202:
            print(f"[+] Command Accepted: {intent}")
        else:
            print(f"[!] Error: {response.text}")
    except Exception as e:
        print(f"[!] Gateway Connection Failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m src.ide_kernel.client <intent> [args...]")
        sys.exit(1)
        
    intent = sys.argv[1]
    # Simple mapping for demo
    if intent == "scaffold":
        dispatch("scaffold", {"module_name": sys.argv[2]})
    elif intent == "write":
        dispatch("write", {"file": sys.argv[2], "code": sys.argv[3]})
