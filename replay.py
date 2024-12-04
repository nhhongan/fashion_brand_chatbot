from collections import deque
import random

class ReplayBuffer():
    def __init__(self, max_size, seed = None):
        self.buffer = deque(maxlen=max_size)
        if seed is not None:
            random.seed(seed)

    def push(self, transition):
        self.buffer.append(transition)

    def sample(self, sample_size):
        sample_size = min(sample_size, len(self.buffer))
        return random.sample(self.buffer, sample_size)
    
    def __len__(self):
        return len(self.buffer)