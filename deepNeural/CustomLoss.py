import torch
import torch.nn as nn

class msel_loss(nn.Module):
    def __init__(self, a=0.5, b=0.5):
        super(msel_loss, self).__init__()
        self.w1 = a
        self.w2 = b
    def forward(self, x, y):
        d = torch.sum((self.w1 * torch.max(x, 1)[1] - self.w2 * y) ** 2)
        return d