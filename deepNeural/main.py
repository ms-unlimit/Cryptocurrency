import torch
import torch.nn as nn
from torch.utils.data import random_split
from CustomDataset import custom_dataset_Data_for_UCI_named, btcDataset
from CustomModel import Net
import argparse
import config
from Framework import Framework


if __name__ == "__main__":
#--------------------------------------------------hyperparameter-------------------------------------------------------

    """init parser"""
    parser = argparse.ArgumentParser()

    """add argument to parser"""
    parser.add_argument('-l','--lr', default=config.lr, type=int, help='learning_rate')
    parser.add_argument('-e','--number_of_epoch', default=config.number_of_epoch, type=int, help='number_of_epoch')
    parser.add_argument('-f','--number_of_features', default=config.number_of_features, type=int, help='number_of_features')
    parser.add_argument('-o','--number_of_out', default=config.number_of_out, type=int, help='number_of_out')
    parser.add_argument('-b','--batch_size', default=config.batch_size, type=int, help='batch_size')

    """parser the argument"""
    arg= parser.parse_args()

#--------------------------------------------------load data------------------------------------------------------------

    # mydataset = custom_dataset_Data_for_UCI_named('Datasets/Data_for_UCI_named.csv')
    mydataset = btcDataset('Datasets/btc.csv')
    number_of_train=(0.7*len(mydataset)).__int__()
    number_of_test=(0.2*len(mydataset)).__int__()
    number_of_valid=(0.1*len(mydataset)).__int__()

    train_dataset, valid_dataset, test_dataset = random_split(mydataset, [number_of_train, number_of_valid, number_of_test])

#------------------------------------------------ model & loss & optimizer ---------------------------------------------

    """model"""
    my_model = Net(arg.number_of_features,arg.number_of_out)
    """loss"""
    loss_function = nn.CrossEntropyLoss()
    """optimizer"""
    optimizer = torch.optim.Adam(my_model.parameters(), lr=arg.lr)

#------------------------------------- train & validation & test whit checkpoint ---------------------------------------

    """set dataset"""
    Framework=Framework(mydataset, train_dataset,number_of_train, valid_dataset,
                        number_of_valid, test_dataset, number_of_test, arg)
    """run network"""
    Framework.run(my_model,optimizer,loss_function)
