import torch
import torch.nn as nn
import torch.nn.functional as F

#hyperparameters
hl1 = 256
hl2 = 64
hl3 = 16
#build model
class Net(nn.Module):

    def __init__(self, unmber_of_features,number_of_out):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(unmber_of_features, hl1)
        self.fc2 = nn.Linear(hl1, hl2)
        self.fc3 = nn.Linear(hl2, hl3)
        self.fc4 = nn.Linear(hl3, number_of_out)
        self.do1 = nn.Dropout(0.5)

    def forward(self, x):
        x = F.sigmoid(self.fc1(x))
        x = self.do1(x)
        x = F.relu(self.fc2(x))
        x = self.do1(x)
        x = F.sigmoid(self.fc3(x))
        x = self.fc4(x)

        return x

    def save_model(self, checkpoint, path):
        torch.save(checkpoint,path)

    def load_model(self, path):
        loaded_checkpoint=torch.load(path)
        return Net.load_state_dict(loaded_checkpoint["model_state"])
