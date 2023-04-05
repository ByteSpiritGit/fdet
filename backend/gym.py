import torch
import json
import os


class Gym:
    def __init__(self, model, tokenizer, name="Model", epochs=0, loss=0) -> None:
        self.name = name.split("/")[0]
        self.model = model
        self.epochs = epochs
        self.tokenizer = tokenizer
        self.track = []
        self.loss = loss
        self.accuracy = 0

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

    def save_track(self):
        n = 0
        filename = f"track{n}.jsonl"
        while (os.path.exists(filename)):
            n += 1
            filename = f"track{n}.jsonl"
            print(n)
        print(f"Track file saved as {filename}")
        with open(filename, "w") as f:
            for i in self.track:
                json.dump(i, f)
                f.write("\n")

    def save_model(self) -> None:
        torch.save(self.model.state_dict(), "BackUp.pth")
        torch.save(
            {
                'epoch': self.epochs,
                'model_state_dict': self.model.state_dict(),
                'loss': self.loss
            }, self.name + ".pth")
        log = f"{self.name} saved!!!"
        print(log)

    def save_checkpoint(self, checkpoint, accuracy) -> None:
        torch.save(
            {
                'epoch': self.epochs,
                'accuracy': accuracy,
                'model_state_dict': self.model.state_dict(),
                'loss': self.loss
            }, f"checkpoint-{checkpoint}.pth")
        log = f"{self.name} saved!!!"
        print(log)
