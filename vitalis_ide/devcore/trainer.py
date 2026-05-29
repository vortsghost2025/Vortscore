import torch
from torch import nn, optim
import json
import time
from pathlib import Path

class TinyTrainer:
    def __init__(self, model, lr=1e-5):
        self.model = model
        self.model.train()
        self.optimizer = optim.AdamW(self.model.parameters(), lr=lr)
        self.criterion = nn.CrossEntropyLoss()
        self.step = 0

    def train_step(self, input_ids, target_ids):
        self.optimizer.zero_grad()
        logits = self.model(input_ids)
        loss = self.criterion(logits.view(-1, logits.size(-1)), target_ids.view(-1))
        loss.backward()
        self.optimizer.step()
        self.step += 1
        return loss.item()
