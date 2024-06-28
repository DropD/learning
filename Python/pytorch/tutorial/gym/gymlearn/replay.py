"""Replay memory for reinforcement learning."""
import random
from collections import namedtuple


Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory:
    """
    A cyclic buffer of bounded size.

    Holds the transitions observed recently. Also implements a .sample() method for selecting a random batch of transitions for training.
    """
    def __init__(self, capacity):
        """Initialize the memory buffer."""
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Save a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        """Draw a batch."""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
