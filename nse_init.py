import torch
from core.nse.trainer import NSETrainer
from core.ledger import VitalisLedger
from core.free_energy import FreeEnergyEngine

def boot_nse():
    print("[SYSTEM] Initializing Neuro-Synth Engine (NSE)...")
    
    # Integrity Handshake
    ledger = VitalisLedger()
    if not ledger.verify_ledger():
        print("[!] FATAL: LEDGER INTEGRITY COMPROMISED. HALTING.")
        return

    # Initialize Components
    fe_engine = FreeEnergyEngine()
    trainer = NSETrainer()
    
    print("[SYSTEM] NSE Sovereign State: ACTIVE.")
    
    # Dummy operational cycle for validation
    sample_input = torch.randn(1, 10, 256)
    fe_stats = torch.tensor([0.5, 0.2, 0.8, 0.1])
    
    loss = trainer.train_step(sample_input, fe_stats)
    print(f"[SYSTEM] Initial Pulse: Loss={loss:.4f}")

if __name__ == "__main__":
    boot_nse()
