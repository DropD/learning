import pytest
import torch

from .deepq import DQN


def test_dqn_dimensions():
    """Test that dimensions work for input image size (80, 40)."""
    net = DQN()
    inp = torch.randn(1, 3, 80, 40)
    net(inp)
