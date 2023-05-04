from nltk.translate.bleu_score import sentence_bleu
from time import strftime, perf_counter
from gym import Gym
import torch


class Seq2seq_Gym(Gym):
    def __init__(self, model, tokenizer, name="Model", epochs=0, loss=0) -> None:
        super().__init__(model, tokenizer, name, epochs, loss)

    def calculate_acc_loss_avg(self, loss, accuracy, perplexity, bleu_score, lossFn, output, predicted, expected):
        accuracy += (predicted == expected)
        perplexity += torch.exp(lossFn(output.logits.view(-1,self.model.config.vocab_size), expected["input_ids"].view(-1))).item()
        bleu_score += sentence_bleu(predicted, expected)
        loss += lossFn(output.logits.view(-1,
                       self.model.config.vocab_size), expected["input_ids"].view(-1))
        return accuracy, perplexity, bleu_score, loss

    def train(self, train_loader, loss_fn, optimizer, scheduler) -> None:
        data_size = len(train_loader.dataset)
        train_track = {"epoch": len(self.track), "loss": [
        ], "batch_size": train_loader.batch_size, "dataset_size": data_size}
        self.model.train()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        for batch, (x, y) in enumerate(train_loader):

            x = x.to(device)
            y = y.to(device)
            output = self.model(input_ids=x["input_ids"], attention_mask=x["attention_mask"], labels=y["input_ids"])
            loss = loss_fn(
                output.logits.view(-1, self.model.config.vocab_size), y["input_ids"].view(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch % 100 == 0:
                loss, progress = loss.item(), batch * len(y["input_ids"])
                log = f"loss: {loss:>8f}, [{progress:>5f}/{data_size:>5f}]\n"
                train_track["loss"].append(loss)
                scheduler.step()
                print(log)
        self.track.append(train_track)

    def train_with_test(self, train_loader, test_loaders, loss_fn, optimizer, scheduler, test_step) -> None:
        data_size = len(train_loader.dataset)
        train_track = {"epoch": len(self.track), "loss": [
        ], "batch_size": train_loader.batch_size, "dataset_size": data_size}
        self.model.train()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        for batch, (x, y) in enumerate(train_loader):
            optimizer.zero_grad()

            x = x.to(device)
            y = y.to(device)
            output = self.model(x["input_ids"], labels=y["input_ids"])
            loss = loss_fn(output.logits.view(-1, self.model.config.vocab_size), y["input_ids"].view(-1))

            loss.backward()
            optimizer.step()
            if batch % 100 == 0:
                loss, progress = loss.item(), batch * len(y)
                log = f"loss: {loss:>8f}, [{progress:>5f}/{data_size:>5f}]\n"
                train_track["loss"].append(loss)
                scheduler.step()
                print(log)
                if batch % test_step == 0:
                    print("Testing...")
                    result = self.test(test_loaders, loss_fn)
                    acc = result[3]
                    if 0.5 < acc > self.accuracy:
                        self.accuracy = acc
                        print("Saving model...")
                        self.save_checkpoint(batch, result[3])
        self.track.append(train_track)

    def test(self, data_loader, loss_fn) -> None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        dataSize = len(data_loader.dataset)
        numBatches = len(data_loader)
        self.model.eval()
        # loss, correct are for the average loss and accuracy (Test Error)
        # loss2, correct2 are for the accuracy of the model when it predicts the correct label
        accuracy, loss, perplexity, bleu_score = 0, 0, 0, 0
        with torch.no_grad():
            for batch, (x, y) in enumerate(data_loader):

                x = x.to(device)
                y = y.to(device)
                output = self.model(x["input_ids"], labels=y["input_ids"])
                loss = loss_fn(output.logits.view(-1, self.model.config.vocab_size), y["input_ids"].view(-1))
                predicted_ids = output.logits.argmax(dim=-1)

                accuracy, perplexity, bleu_score, loss = self.calculate_acc_loss_avg(
                    loss, accuracy, perplexity, bleu_score, loss_fn, output, predicted_ids, y)

        accuracy /= numBatches
        loss /= numBatches
        perplexity /= dataSize
        bleu_score /= dataSize
        self.loss = loss
        self.acc = accuracy
        log = f"Results: \nPerplexity: {perplexity:>8f}, Bleu score, {bleu_score:>8f}  \n My Accuracy: {(100*accuracy):>0.1f}%, Avg loss: {loss:>8f}\n"
        print(log)
        return accuracy, loss, perplexity, bleu_score

    def test_sqce(self, test_loaders, lossFn):
        start_time = perf_counter()
        for i, data_loader in enumerate(test_loaders):
            EpochLog = f"\nTest {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.test(data_loader, lossFn)
            epochTime = f"--- {(perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
            end = strftime(f"Test Ended!!! %H%M-%d-%m")
            print(end)

    def train_sqce(self, epochs, train_loader, test_loaders, lossFn, optimizer, scheduler) -> None:
        start_time = perf_counter()
        for i in range(epochs):
            EpochLog = f"\nEpoch {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.train(train_loader, lossFn, optimizer, scheduler)
            epochTime = f"--- {(perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
        self.epochs += epochs
        self.save_track()
        self.save_model()
        self.test_sqce(test_loaders, lossFn)

    def train_sqce_with_test(self, epochs, train_loader, test_loader, val_loader, loss_fn, optimizer, scheduler, step_test) -> None:
        start_time = perf_counter()
        for i in range(epochs):
            EpochLog = f"\nEpoch {i + 1} \n---------------------------------\n"
            print(EpochLog)
            self.train_with_test(train_loader, test_loader,
                                 loss_fn, optimizer, scheduler, step_test)
            epochTime = f"--- {(perf_counter() - start_time)} seconds ---\n"
            print(epochTime)
        self.epochs += epochs
        self.save_track()
        self.save_model()
        self.test(val_loader, loss_fn)
