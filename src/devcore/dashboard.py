import json
import os

class FSIDashboard:
    def show(self):
        print("=================================================")
        print("    FERRELL SYNTHETIC INTELLIGENCE - DASHBOARD   ")
        print("=================================================")
        if os.path.exists("notifications.json"):
            with open("notifications.json", "r") as f:
                data = json.load(f)
                for note in data.get("updates", []):
                    print(f"[!] {note}")
        else:
            print("[+] No pending notifications. System stable.")
        print("=================================================")
