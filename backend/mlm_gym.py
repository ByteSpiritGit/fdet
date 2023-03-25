from time import strftime, perf_counter
from gym import Gym
import torch

class MLM_Gym(Gym):
    def __init__(self, model, tokenizer, name="Model", epochs = 0, loss = 0) -> None:
        super().__init__(model, tokenizer, name, epochs, loss)

    def train(self, data_loader, loss_fn, optimizer) -> None:
        data_size = len(data_loader.dataset)
        train_track = {"epoch": len(self.track), "loss": [], "batch_size" : data_loader.batch_size, "dataset_size": data_size}
        self.model.train()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        for batch, (x, y) in enumerate(data_loader):

            x = x.to(device)
            y = y.to(device)
            prediction = self.model(**x)

            loss = loss_fn(prediction.logits, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch % 100 == 0:
                loss, progress = loss.item(), batch * len(y)
                log = f"loss: {loss:>8f}, [{progress:>5f}/{data_size:>5f}]\n"
                train_track["loss"].append(loss)
                print(log)
        self.track.append(train_track)

    def test(self, data_loader, loss_fn) -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        dataSize = len(data_loader.dataset)
        numBatches = len(data_loader)
        self.model.eval()
        # loss, correct are for the average loss and accuracy (Test Error)
        # loss2, correct2 are for the accuracy of the model when it predicts the correct label
        loss, correct, loss2, correct2  = 0, 0, 0, 0
        with torch.no_grad():
            for batch, (x, y) in enumerate(data_loader):

                inputIDs = x["input_ids"].squeeze(1).to(device)
                attention = x["attention_mask"].squeeze(1).to(device)
                typeIds = x["token_type_ids"].squeeze(1).to(device)

                y = y.to(device)

                prediction = self.model(
                    input_ids=inputIDs, attention_mask=attention, token_type_ids=typeIds)

                correct, loss = self.calculate_acc_loss_avg(
                    correct, loss, batch, loss_fn, prediction, y)
                correct2, loss2 = self.calculate_acc_loss_press(
                    correct2, loss2, loss_fn, prediction, y, batch)

        loss /= numBatches
        loss2 /= numBatches
        correct /= dataSize
        correct2 /= dataSize
        self.loss = loss
        self.acc = correct
        log = f"Results: \n Test Error: {(100*correct):>0.1f}%, Avg loss: {loss:>8f} \n My Accuracy: {(100*correct2):>0.1f}%, Avg loss: {loss2:>8f}\n"
        print(log)

    def test_sqce(self, data_loaders, lossFn):
        start_time = perf_counter()
        for i, data_loader in enumerate(data_loaders):
            EpochLog = f"\nTest {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.test(data_loader, lossFn)
            epochTime = f"--- {(perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
            end = strftime(f"Test Ended!!! %H%M-%d-%m")
            print(end)

    def train_sqce(self, epochs, train_data_loader, test_data_loaders, lossFn, optimizer) -> None:
        start_time = perf_counter()
        for i in range(epochs):
            EpochLog = f"\nEpoch {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.train(train_data_loader, lossFn, optimizer)
            epochTime = f"--- {(perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
        self.epochs += epochs
        self.save_track()
        self.save_model()
        self.test_sqce(test_data_loaders, lossFn)