import time
from src.devcore.auto_developer import AutoDeveloper

class GuardianDaemon:
    def __init__(self):
        self.auto_dev = AutoDeveloper()

    def run_background_cycle(self, iterations=3):
        print(f"\n[*] VITALIS GUARDIAN: Entering deep autonomous cycle ({iterations} iterations)...")
        
        for i in range(iterations):
            print(f"\n[=================================================]")
            print(f"[*] GUARDIAN: Initiating iteration {i+1}/{iterations}")
            self.auto_dev.execute_synthetic_mission()
            time.sleep(2)  # Simulating processing cooldown between synthesis generations
            
        print("\n[+] VITALIS GUARDIAN: Background cycles complete. Entering standby.")
        print("[+] Awaiting User Directives.")
