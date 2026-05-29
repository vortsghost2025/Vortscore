import numpy as np
import os

class Hippocampus:
    def __init__(self, filename="vitalis_memory.bin", dim=10000, capacity=1000):
        self.filename = filename
        self.dim = dim
        self.capacity = capacity
        self.size = capacity * dim * 1
        
        self.fd = os.open(self.filename, os.O_RDWR | os.O_CREAT)
        os.ftruncate(self.fd, self.size)
        
        self.mem = np.memmap(self.filename, dtype=np.int8, mode="r+", shape=(capacity, dim))

    def store(self, index, vector):
        if index >= self.capacity:
            raise IndexError("Memory capacity exceeded")
        self.mem[index] = vector
        self.mem.flush()

    def recall(self, index):
        return self.mem[index].copy()

    def close(self):
        self.mem.flush()
