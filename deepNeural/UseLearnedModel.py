import torch
from CustomDataset import custom_dataset_Data_for_UCI_named
from CustomModel import Net
from torch.utils.data import DataLoader

#--------------------------------------------------load data------------------------------------------------------------

mydataset = custom_dataset_Data_for_UCI_named('Datasets/Data_for_UCI_named.csv')
dataloader = DataLoader(mydataset, batch_size=1)

#--------------------------------------------------load model-----------------------------------------------------------

try:
    print("loading checkpoint ....")
    loaded_checkpoint = torch.load("checkpoint.pth")

    my_model = Net(loaded_checkpoint["number_of_features"],loaded_checkpoint["number_of_out"])
    my_model.load_state_dict(loaded_checkpoint["model_state"])

    optimizer = torch.optim.Adam(my_model.parameters(), lr=loaded_checkpoint["lr"])
    optimizer.load_state_dict(loaded_checkpoint["optim_state"])

    start_epoch_number = loaded_checkpoint["epoch"]
    print('continue form epoch [%d] ' % (start_epoch_number))
except:
    print("failed loading")

#------------------------------------------------use learned model------------------------------------------------------
for data_batch, label_batch in dataloader:
    out = my_model(data_batch)
    _, predicted = torch.max(out.data, 1)# "return [max value],[max value index] of data" , "1 is for return max value index" (for each row in tensor)
    print(predicted,label_batch)
    print('predicted:[%d] , label:[%d]' % (predicted.data,label_batch.data))
