import torch
import transformers
import sys
from mlm_gym import MLM_Gym
from datasets import load_dataset
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler


def example():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")

    tokenizer = transformers.AlbertTokenizerFast.from_pretrained(
        'Dzeniks/alberta_fact_checking', longest_first=False)
    model = transformers.AlbertForSequenceClassification.from_pretrained(
        'Dzeniks/alberta_fact_checking', return_dict=True, num_labels=2)
    model.to(device)
    claim = "Albert einstein work in the field of computer science"
    evidence = "Albert Einstein (/ˈaɪnstaɪn/ EYEN-styne;[6] German: [ˈalbɛʁt ˈʔaɪnʃtaɪn] (listen); 14 March 1879 – 18 April 1955) was a German-born theoretical physicist,[7] widely acknowledged to be one of the greatest and most influential physicists of all time."

    model.to(device)
    x = tokenizer.encode_plus(claim, evidence, truncation="longest_first",
                              max_length=512, padding="max_length", return_tensors="pt")
    model.eval()
    with torch.no_grad():
        x = x.to(device)
        inputIDs = x["input_ids"].squeeze(1)
        attention = x["attention_mask"].squeeze(1)
        typeIds = x["token_type_ids"].squeeze(1)
        prediction = model(input_ids=inputIDs,
                           attention_mask=attention, token_type_ids=typeIds)

    print(
        f"ArgMax: {torch.argmax(prediction.logits)}\nSoftMax: {torch.softmax(prediction.logits, dim=1)}")


def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")

    name = "albert-base-v2"
    tokenizer = transformers.AlbertTokenizerFast.from_pretrained(
        name, longest_first=False)
    model = transformers.AlbertForSequenceClassification.from_pretrained(
        name, return_dict=True, num_labels=3)
    # model.load_state_dict(torch.load("albert.pth")["model_state_dict"])
    model.to(device)

    def collate_fn(data):
        claims, evidences, labels = zip(
            *[(d['claim'], d['evidence'], d['label']) for d in data])
        labels = torch.tensor(labels)
        texts = [f"{c} {tokenizer.sep_token} {e}" for c,
                 e in zip(claims, evidences)]
        toks = tokenizer.batch_encode_plus(
            texts, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
        return toks, labels

    test_dataset = load_dataset("Dzeniks/fever_3way", split="test")
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=1,
        sampler=SequentialSampler(test_dataset),
        collate_fn=collate_fn
    )

    val_dataset = load_dataset("Dzeniks/fever_3way", split="validation")
    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=1,
        sampler=SequentialSampler(val_dataset),
        collate_fn=collate_fn
    )

    gym = MLM_Gym(model, tokenizer, name)

    gym.test_sqce([test_dataset, test_loader], test_loader, val_loader)


def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")

    name = "albert-base-v2"
    tokenizer = transformers.AlbertTokenizerFast.from_pretrained(
        name, longest_first=False)
    model = transformers.AlbertForSequenceClassification.from_pretrained(
        name, return_dict=True, num_labels=3)
    # model.load_state_dict(torch.load("albert.pth")["model_state_dict"])
    model.to(device)

    batch_size = 3

    def collate_fn(data):
        claims, evidences, labels = zip(
            *[(d['claim'], d['evidence'], d['label']) for d in data])
        labels = torch.tensor(labels)
        texts = [f"{c} {tokenizer.sep_token} {e}" for c,
                 e in zip(claims, evidences)]
        toks = tokenizer.batch_encode_plus(
            texts, truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
        return toks, labels

    train_dataset = load_dataset("Dzeniks/FactFusion", split="train")
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        sampler=RandomSampler(train_dataset),
        collate_fn=collate_fn,
    )

    test_dataset = load_dataset("Dzeniks/fever_3way", split="test")
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=1,
        sampler=SequentialSampler(test_dataset),
        collate_fn=collate_fn
    )

    val_dataset = load_dataset("Dzeniks/fever_3way", split="validation")
    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=1,
        sampler=SequentialSampler(val_dataset),
        collate_fn=collate_fn
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-6, eps=1e-8)
    loss_fn = torch.nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.5)

    gym = MLM_Gym(model, tokenizer, name)
    gym.train_sqce_with_test(1, train_loader, test_loader,
                             val_loader, loss_fn, optimizer, scheduler, 4)


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "--train":
            train()
        elif args[1] == "--test":
            test()
        elif args[1] == "--example":
            example()
