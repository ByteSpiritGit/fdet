import time
from time import strftime
import torch


class Gym_albert():
    def __init__(self, model, tokenizer, name="Model") -> None:
        self.name = name
        self.model = model
        self.tokenizer = tokenizer
        self.modelPath = f"{name}.pth"
        self.loss = None
        self.acc = None

    def train(self, data_loader, loss_fn, optimizer) -> None:
        dataSize = len(data_loader.dataset)
        self.model.train()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        for batch, (x, y) in enumerate(data_loader):

            inputIDs = x["input_ids"].squeeze(1).to(device)
            attention = x["attention_mask"].squeeze(1).to(device)
            typeIds = x["token_type_ids"].squeeze(1).to(device)

            y = y.to(device)

            prediction = self.model(
                input_ids=inputIDs, attention_mask=attention, token_type_ids=typeIds)
            loss = loss_fn(prediction.logits, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch % 100 == 0:
                loss, progress = loss.item(), batch * len(y)
                log = f"loss: {loss:>8f}, [{progress:>5f}/{dataSize:>5f}]\n"
                print(log)

    def calculate_acc_loss_avg(self, corrects, loss, batch_num, lossFn, prediction, label):
        loss += lossFn(prediction.logits, label)
        corrects += ((1 / (batch_num + 1)) * (loss.item() - corrects))
        return corrects, loss

    def calculate_acc_loss_press(self, corrects, loss, lossFn, prediction, label, id):
        if torch.argmax(prediction.logits) == label:
            corrects += 1
        else:
            with open("errors.txt", "a") as f:
                f.write(f"{id}\n")
        loss += lossFn(prediction.logits, label)
        return corrects, loss

    def test(self, dataLoader, loss_fn) -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        dataSize = len(dataLoader.dataset)
        numBatches = len(dataLoader)
        self.model.eval()
        loss, correct, correct2, loss2 = 0, 0, 0, 0
        with torch.no_grad():
            for batch, x in enumerate(dataLoader):

                evidence = x["evidence"]
                claim = x["claim"]
                y = x["label"]
                x = self.tokenizer.encode_plus(
                    claim, evidence, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")

                # x = x.to(device)
                # y = y.to(device)

                inputIDs = x["input_ids"].squeeze(1).to(device)
                attention = x["attention_mask"].squeeze(1).to(device)
                typeIds = x["token_type_ids"].squeeze(1).to(device)


                prediction = self.model(
                    input_ids=inputIDs, attention_mask=attention, token_type_ids=typeIds)
                correct, loss = self.calculateAccLoss(
                    correct, loss, batch, loss_fn, prediction, y)
                correct2, loss2 = self.calculateAccLossPress(
                    correct2, loss2, loss_fn, prediction, y, batch)

        loss /= numBatches
        loss2 /= numBatches
        correct /= dataSize
        correct2 /= dataSize
        self.loss = loss
        self.acc = correct
        log = f"Results: \n Test Error: {(100*correct):>0.1f}%, Avg loss: {loss:>8f} \n My Accuracy: {(100*correct2):>0.1f}%, Avg loss: {loss2:>8f}\n"
        print(log)

    def test_sqce(self, model, data_loaders, lossFn):
        start_time = time.perf_counter()
        for i, data_loader in enumerate(data_loaders):
            EpochLog = f"\nTest {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.test(model, data_loader, lossFn)
            epochTime = f"--- {(time.perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
            end = strftime(f"Test Ended!!! %H%M-%d-%m")
            print(end)

    def train_sqce(self, epochs, train_data_loader, test_data_loaders, lossFn, optimizer) -> None:
        start_time = time.perf_counter()
        for i in range(epochs):
            EpochLog = f"\nEpoch {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.train(train_data_loader, lossFn, optimizer)
            epochTime = f"--- {(time.perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
            torch.save(self.model.state_dict(), "LastBackUp.pth")
            end = strftime(f"LastBackUp{i} saved!!! %H%M-%d-%m")
            print(end)
        self.test_sqce(self.model, test_data_loaders, lossFn)
        self.saveModel(model=self.model, Epochs=epochs)

    def saveModel(self, Epochs, loss=None, acc=None) -> None:
        torch.save(self.model.state_dict(), "LastBackUp.pth")
        if loss == None:
            try:
                loss = self.loss
            except:
                pass
        if acc == None:
            try:
                acc = self.acc
            except:
                pass
        torch.save(
            {
                'epoch': Epochs,
                'model_state_dict': self.model.state_dict(),
                'loss': loss,
                'accuracy': acc
            }, self.modelPath)
        log = strftime(f"{self.name} saved!!! %H%M-%d-%m")
        print(log)
