#!/usr/bin/env python3
import argparse
from core.brain import VitalisBrain
from app import main as run_repl

def run_training():
    print("[*] Initiating Synaptic Matrix Optimization...")
    brain = VitalisBrain()
    # Mock stream for training if data_path missing
    data = [{"prompt": "status", "response": "nominal"}, {"prompt": "init", "response": "ready"}]
    
    for epoch in range(1, 6):
        for entry in data:
            brain.execute_teacher_forcing(entry["prompt"], entry["response"])
        print(f"   -> Epoch {epoch}/5 Complete.")
    print("[+] Optimization complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    args = parser.parse_args()
    
    if args.train:
        run_training()
    else:
        run_repl()
