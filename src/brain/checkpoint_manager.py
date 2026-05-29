import torch
import os

def save_vitalis_weights(model, path="checkpoints/vitalis_v1.pt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path)
    print(f"Weights saved to {path}")
