import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Net(nn.Module):
    """Neural Net from the tutorial."""

    def __init__(self):
        """
        Initiate the net.

        Structure:

            * 1 input image channel
            * 6 output channels
            * 5x5 square convolution kernel
        """
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        ## an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

        self.optimizer = optim.SGD(self.parameters(), lr=0.01)
        self.loss_criterion = nn.MSELoss()

    def forward(self, x):
        """Forward prop?"""
        ## Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        ## If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimesions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


    def train_minibatch(self, minibatch, target):
        """Train a minibatch using SGD optimizer from torch.optim."""
        self.optimizer.zero_grad()
        output = self(minibatch)
        loss = loss_criterion(output, target)
        loss.backward()
        optimizer.step()


if __name__ == '__main__':
    net = Net()
    print(net)
