from torch.optim.optimizer import Optimizer

class AccSGD(Optimizer):
    def __init__(self):
        super(AccSGD, self).__init__()

    def step(self):
        pass