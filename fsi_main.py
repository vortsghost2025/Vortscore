from core.vitalis_engine import VitalisEngine
from core.vitalis_brain import VitalisBrain
from core.sovereign_shield import monitor_integrity
import sys

def boot_sequence():
    print("[SYSTEM] Booting Sovereign Shield...")
    status = monitor_integrity("Initial_Environment_Check")
    print(status)
    if "SECURE" not in status:
        raise SystemExit("[!] CRITICAL: System integrity compromised. Halting.")

def main():
    boot_sequence()
    print("--- FSI: Vitalis Core Sovereign Intelligence ---")
    engine = VitalisEngine()
    engine.wake_up()
    brain = VitalisBrain()
    
    print("Vitalis is ready. System Online.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit": break
        response = brain.process(user_input)
        print(f"Vitalis: {response.status}")

if __name__ == "__main__":
    main()
