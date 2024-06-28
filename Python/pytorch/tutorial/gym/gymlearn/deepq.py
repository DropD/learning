"""Deep Q Network."""
import torch
from torch import nn
import torch.nn.functional as F

from .utils import out_dimensions


class DQN(nn.Module):
    """Deep Q Network for reinforcement learning."""

    def __init__(self):
        super().__init__()
        self.image_size = torch.tensor([40, 80])
        self.conv = []
        self.bnorm = []
        self.conv.append(nn.Conv2d(3, 16, kernel_size=5, stride=2))
        self.bnorm.append(nn.BatchNorm2d(self.conv[0].out_channels))
        self.conv.append(nn.Conv2d(self.conv[0].out_channels, 32, kernel_size=5, stride=2))
        self.bnorm.append(nn.BatchNorm2d(self.conv[1].out_channels))
        self.conv.append(nn.Conv2d(self.conv[1].out_channels, 32, kernel_size=5, stride=2))
        self.bnorm.append(nn.BatchNorm2d(self.conv[2].out_channels))

        self.c2_size = out_dimensions(self.image_size, *self.conv)
        self.head = nn.Linear(self.c2_size.prod().item() * self.conv[2].out_channels, 2)


    def forward(self, *inputs):
        data = inputs[0]
        data = F.relu(self.bnorm[0](self.conv[0](data)))
        data = F.relu(self.bnorm[1](self.conv[1](data)))
        data = F.relu(self.bnorm[2](self.conv[2](data)))
        return self.head(data.view(data.size(0), -1))
