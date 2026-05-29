import json, os

def run_diagnostics():
    ledger_path = "project_ledger.json"
    if os.path.exists(ledger_path):
        with open(ledger_path, 'r') as f:
            data = json.load(f)
            print("[DIAGNOSTICS] Current Ledger State:")
            print(json.dumps(data, indent=2))
    else:
        print("[DIAGNOSTICS] No ledger found. System idle.")

if __name__ == "__main__":
    run_diagnostics()
