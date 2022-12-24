from torch.utils.data.dataset import Dataset
import torch
import pandas as pd

class custom_dataset_Data_for_UCI_named(Dataset):
    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path)
        self.data.loc[self.data['stabf'] == 'unstable', 'stabf'] = 1
        self.data.loc[self.data['stabf'] == 'stable', 'stabf'] = 0
        # change string value to numeric
        self.data = self.data.apply(pd.to_numeric)
        # change dataframe to array
        self.data = self.data.values
        self.x = torch.Tensor(self.data[:, :13]).float()
        self.y = torch.Tensor(self.data[:,  13]).long()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = (self.x[idx,:], self.y[idx])
        return sample


class btcDataset(Dataset):
    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path)
        self.data = self.data.values
        self.x = torch.Tensor(self.data[:, 1:13]).float()
        self.y = torch.Tensor(self.data[:,  13]).long()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = (self.x[idx,:], self.y[idx])
        return sample
