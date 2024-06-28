import pytest
import torch
import torch.nn as nn

from .utils import out_dimensions


def test_out_dimensions():
    c1 = nn.Conv2d(3, 3, kernel_size=5, stride=2)
    dims = torch.tensor([320, 160])
    assert bool((out_dimensions(dims, c1) == torch.tensor([158, 78])).all())
    assert bool((out_dimensions(dims, c1, c1) == torch.tensor([77, 37])).all())
    assert bool((out_dimensions(dims, c1, c1, c1) == torch.tensor([37, 17])).all())
