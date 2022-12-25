import  torch
from torch.utils.data import DataLoader

class Framework:
    def __init__(self,mydataset=None, train_dataset=None,number_of_train=None, valid_dataset=None,number_of_valid=None, test_dataset=None, number_of_test=None, arg=None):
        self.mydataset = mydataset
        self.train_dataset = train_dataset
        self.valid_dataset = valid_dataset
        self.test_dataset = test_dataset
        self.number_of_train = number_of_train
        self.number_of_valid = number_of_valid
        self.number_of_test = number_of_test
        self.arg = arg
        print("init Framework")

    def run(self, my_model,optimizer, loss_function):

        start_epoch_number = 0

        """"""" --------------------------- try to load model -------------------------------------------------- """""""
        try:
            print("loading checkpoint ....")
            loaded_checkpoint = torch.load("checkpoint0.pth")
            my_model.load_state_dict(loaded_checkpoint["model_state"])
            optimizer.load_state_dict(loaded_checkpoint["optim_state"])
            start_epoch_number = loaded_checkpoint["epoch"]
            print('continue form epoch [%d] ' % (start_epoch_number))
        except:
            print("failed loading")

        # ------------------------------------ start: train & validation & test-----------------------------------------
        dataloader = DataLoader(self.train_dataset, batch_size=self.arg.batch_size, shuffle=True)

        for epoch in range(start_epoch_number, self.arg.number_of_epoch):

            loss=self.train(my_model,optimizer, loss_function,dataloader)
            """"""" ---------------------------------------- save model -----------------------------------------"""""""
            checkpoint = {"epoch": epoch, "model_state": my_model.state_dict(), "optim_state": optimizer.state_dict(),
                          "lr": self.arg.lr,"number_of_features":self.arg.number_of_features,"number_of_out":self.arg.number_of_out}
            torch.save(checkpoint, "checkpoint.pth")

            if (epoch) % 5 == 0:
                self.validation(my_model, loss_function, loss, epoch)

        self.test(my_model)



    def train(self, my_model,optimizer, loss_function,dataloader):
        for data_batch, label_batch in dataloader:
            optimizer.zero_grad()
            out = my_model(data_batch)
            loss = loss_function(out, label_batch)
            loss.backward()
            optimizer.step()
            return loss


    def validation(self, my_model, loss_function, loss, epoch):

        my_model = my_model.eval()
        out = my_model(self.mydataset.x[self.valid_dataset.indices, :self.arg.number_of_features])
        _, predicted = torch.max(out.data, 1)
        label_v = self.mydataset.y[self.valid_dataset.indices]
        loss_v = loss_function(out, label_v)
        print('Epoch [%d/%d] Train Loss: %.4f' % (epoch + 1, self.arg.number_of_epoch, loss.item()))
        print('Epoch [%d/%d] Valid Loss: %.4f' % (epoch + 1, self.arg.number_of_epoch, loss_v.item()))
        acc = (100 * torch.sum(label_v == predicted) /self.number_of_valid)
        print('Accuracy of the network in Validation %.4f %%' %acc)
        return


    def test(self, my_model):
        my_model = my_model.eval()
        X = self.mydataset.x[self.test_dataset.indices]
        Y = self.mydataset.y[self.test_dataset.indices]
        # calculate out
        out = my_model(X)
        _, predicted = torch.max(out.data, 1)
        # get accuration
        print('Accuracy of the network in Test %.4f %%' % (100 * torch.sum(Y == predicted) / self.number_of_test))
        return
