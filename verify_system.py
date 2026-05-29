from brain import get_ripple_payload
import json

print("[*] Performing Depth-Charge reasoning test (Depth=3)...")
payload = get_ripple_payload("Why is the architecture sovereign?", max_depth=3)
print(f"[+] Reasoning steps generated: {len(payload['steps'])}")
print(f"[+] Final conclusion: {payload['final_conclusion']['label']}")

# Validate graph structure
for step in payload['steps']:
    print(f" -> Node {step['id']} | FE: {step['free_energy']:.4f}")
