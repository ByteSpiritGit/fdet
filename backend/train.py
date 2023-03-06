import torch
import transformers
from gym import Gym_albert
from datasets import load_dataset
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")
    
    tokenizer = transformers.AlbertTokenizerFast.from_pretrained('Dzeniks/alberta_fact_checking', longest_first=False)
    model = transformers.AlbertForSequenceClassification.from_pretrained('Dzeniks/alberta_fact_checking', return_dict=True, num_labels=2)
    model.to(device)
    claim = "Albert einstein work in the field of computer science"
    evidence = "Albert Einstein (/ˈaɪnstaɪn/ EYEN-styne;[6] German: [ˈalbɛʁt ˈʔaɪnʃtaɪn] (listen); 14 March 1879 – 18 April 1955) was a German-born theoretical physicist,[7] widely acknowledged to be one of the greatest and most influential physicists of all time."
    
    model.to(device)
    x = tokenizer.encode_plus(claim, evidence, truncation="longest_first" , max_length=512, padding="max_length", return_tensors="pt")                                     
    model.eval()
    with torch.no_grad(): 
        x = x.to(device)
        inputIDs = x["input_ids"].squeeze(1)
        attention = x["attention_mask"].squeeze(1)
        typeIds = x["token_type_ids"].squeeze(1)
        prediction = model(input_ids=inputIDs, attention_mask=attention, token_type_ids=typeIds)
    
    print(f"ArgMax: {torch.argmax(prediction.logits)}\nSoftMax: {torch.softmax(prediction.logits, dim=1)}")


def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"You are using {device}")

    tokenizer = transformers.AlbertTokenizerFast.from_pretrained('albert-base-v2', longest_first=False)
    model = transformers.AlbertForSequenceClassification.from_pretrained('albert-base-v2', return_dict=True, num_labels=3)
    
    model.to(device)

    batch_size = 2
    train_dataset = load_dataset("Dzeniks/fever_3way", split="train")
    

    def collate_fn(data):
        tokens = {"input_ids":torch.zeros((len(data), 1, 512), dtype=torch.int64), "attention_mask":torch.zeros((len(data), 1, 512), dtype=torch.int64), "token_type_ids": torch.zeros((len(data), 1, 512), dtype=torch.int64)}
        labels = torch.zeros(len(data), dtype=torch.int64)
        for num, i in enumerate(data):
            token = tokenizer.encode_plus(i["claim"], i["evidence"], truncation="longest_first", max_length=512, padding="max_length", return_tensors="pt")
            tokens["input_ids"][num] = token["input_ids"]
            tokens["attention_mask"][num] = token["attention_mask"]
            tokens["token_type_ids"][num] = token["token_type_ids"]
            labels[num] = i["label"]                                       
        return tokens, labels

    loader_test = DataLoader(
        dataset= train_dataset,
        batch_size=batch_size,
        sampler=RandomSampler(train_dataset),
        collate_fn=collate_fn
        )
    
    test_dataset = load_dataset("Dzeniks/fever_3way", split="test")
    
    test_test = DataLoader(
        dataset= test_dataset,
        batch_size=1,
        sampler=SequentialSampler(test_dataset),
        collate_fn=collate_fn
        )

    optimizer = torch.optim.Adam(model.parameters(), lr = 2e-6, eps = 1e-8)
    lossFn = torch.nn.CrossEntropyLoss()

    gym_albert = Gym_albert(model, tokenizer, "TEST")

    gym_albert.train_sqce(1, loader_test, [test_test], lossFn, optimizer)


train()