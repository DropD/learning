"""Utility functions."""
import torch
from torch import nn


def out_dimensions(in_dimensions, *args):
    """Determine the output image size after a series of convolutional layers."""
    if len(args) == 1:
        node = args[0]
        if isinstance(node, nn.Conv2d):
            inner = in_dimensions - torch.tensor(node.kernel_size, dtype=torch.long) + 1
            features = torch.tensor(inner, dtype=torch.float) / torch.tensor(node.stride, dtype=torch.float)
            return torch.tensor(features.ceil(), dtype=torch.long)
        return in_dimensions
    first_stage_dims = out_dimensions(in_dimensions, args[0])
    return out_dimensions(first_stage_dims, *args[1:])
