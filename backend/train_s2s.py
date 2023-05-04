import torch
import transformers
import sys
import anlys
import pandas as pd
from s2s_gym import Seq2seq_Gym
from datasets import load_dataset
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler


def example():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")
    name = "roberta-base"
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        name, longest_first=True)
    model = transformers.AutoModelForSequenceClassification.from_pretrained(
        name, return_dict=True, num_labels=2)
    model.load_state_dict(torch.load(r"../roberta-NEI-fever.pth")["model_state_dict"])
    
    # model.load_state_dict(torch.load("checkpoint-100.pth")["model_state_dict"])
    model.to(device)
    # claim = "Albert Einstein work in the field of computer science"
    # claim = "Albert Einstein was theoretical physicist"
    # evidence = "Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist, widely acknowledged to be one of the greatest and most influential physicists of all time."

    # claim = "Germany won world war II."
    # claim = "Germany lost world war II."
    # claim = "Hitler was gay."
    claim = "What the fuck"
    evidence = "Following Hitler's suicide during the Battle of Berlin, Germany signed the surrender document on 8 May 1945, ending World War II in Europe and Nazi Germany\n"
    model.to(device)
    x = tokenizer.encode_plus(claim, evidence, truncation="longest_first",
                              max_length=512, padding="max_length", return_tensors="pt")
    model.save_pretrained("../roberta-nei-fever")
    tokenizer.save_pretrained("../roberta-nei-fever")

    model.eval()
    with torch.no_grad():
        x = x.to(device)
        prediction = model(**x)
    print(
        f"ArgMax: {torch.argmax(prediction.logits)}\nSoftMax: {torch.softmax(prediction.logits, dim=1)}")


def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")

    name = "gpt2"
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        name, longest_first=True)
    
    tokenizer.add_special_tokens({'pad_token': '[PAD]',
                                  "sep_token": "[SEP]",
                                  "cls_token": "[CLS]",
                                  "mask_token": "[MASK]",
                                  })
    model = transformers.GPT2LMHeadModel.from_pretrained(
        name, return_dict=True)
    model.resize_token_embeddings(len(tokenizer))
    model.load_state_dict(torch.load("gpt2.pth")["model_state_dict"])
    model.to(device)


    def collate_fn(data):
        question, context, answers = zip(
            *[(d['question'], d['context'], d['answers']) for d in data])
        answers = [a["text"][0] if a["text"] else " " for a in answers]
        answers = tokenizer(
            answers, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
        toks = tokenizer(
            question, context, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
        return toks, answers

    quick_dataset = load_dataset("squad_v2", split="validation")
    quick_loader = DataLoader(
        dataset=quick_dataset,
        batch_size=1,
        sampler=SequentialSampler(quick_dataset),
        collate_fn=collate_fn
    )

    test_dataset = load_dataset("Dzeniks/FactFusion", split="test")
    # test_dataset = anlys.clean(test_dataset)
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=1,
        sampler=SequentialSampler(test_dataset),
        collate_fn=collate_fn
    )

    # val_dataset = load_dataset("Dzeniks/FactFusion", split="validation")
    # # val_dataset = anlys.clean(val_dataset)
    # val_loader = DataLoader(
    #     dataset=val_dataset,
    #     batch_size=1,
    #     sampler=SequentialSampler(val_dataset),
    #     collate_fn=collate_fn
    # )

    gym = Seq2seq_Gym(model, tokenizer, name)
    loss_fn = torch.nn.CrossEntropyLoss()
    gym.test_sqce([quick_loader, test_loader], loss_fn)


def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")

    tokenizer = transformers.RobertaForCausalLM.from_pretrained('facebook/bart-base')
    model = transformers.RobertaForCausalLM.from_pretrained('facebook/bart-base')


    batch_size = 1

    def collate_fn(data):
        question, context, answers = zip(
            *[(d['question'], d['context'], d['answers']) for d in data])
        answers = [a["text"][0] if a["text"] else " " for a in answers]
        answers = tokenizer(
            answers, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
        toks = tokenizer(
            question, context, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
        return toks, answers

    train_dataset = load_dataset("squad_v2", split="train")
    train_dataset = list(train_dataset)
    train_dataset = train_dataset[:40_000]
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        sampler=RandomSampler(train_dataset),
        collate_fn=collate_fn,
    )

    test_dataset = load_dataset("squad_v2", split="validation")
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=1,
        sampler=SequentialSampler(test_dataset),
        collate_fn=collate_fn
    )

    optimizer = torch.optim.Adagrad(model.parameters(), lr=2e-4, eps=1e-8, weight_decay=9e-9)
    loss_fn = torch.nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=8 ,gamma=0.1)

    print(len(train_dataset))
    print(test_dataset)

    name = "gpt2"
    gym = Seq2seq_Gym(model, tokenizer, name)
    gym.train_sqce(1, train_loader, [test_loader],
                             loss_fn, optimizer, scheduler)


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "train":
            train()
        elif args[1] == "test":
            test()
        elif args[1] == "example":
            example()
    else:
        train()
