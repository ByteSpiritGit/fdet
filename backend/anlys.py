import json
import re
import matplotlib.pyplot as plt
import random
import requests
import re
import openai
import asyncio
import time

STOP_WORDS = ["a", "an", "the", "o"]
def remove_stop_words(text):
    text = text.split()
    text = " ".join([i for i in text if i not in STOP_WORDS])
    return text


def load(path):
    file = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            file.append(json.loads(line))
    return file



def load_from_url(url):
    request = requests.get(url)
    new_file = []
    for line in request.text.splitlines():
        data = json.loads(line)
        new_file.append(data)
    return new_file


def save(file, path):
    with open(path, 'w', encoding="utf-8") as f:
        for line in file:
            json.dump(line, f)
            f.write('\n')


def show_loss(load_track):
    loss = []
    progress = []
    for i in load_track:
        loss += i["loss"]
    for i in range(len(loss)):
        progress.append(i * load_track[0]["batch_size"] * 100)
    plt.plot(progress, loss)
    plt.xlabel('Progress')
    plt.ylabel('Loss')
    plt.title('Graph')
    plt.show()


def analyze(file):
    SUP, REF, NEI, EI = 0, 0, 0, 0
    for i in file:
        if i["label"] == "SUPPORTS" or i["label"] == 0:
            SUP += 1
        elif i["label"] == "REFUTES" or i["label"] == 1:
            REF += 1
        elif i["label"] == "NOT ENOUGH INFO" or i["label"] == 2:
            NEI += 1
        elif i["label"] == "ENOUGH INFO" or i["label"] == 2:
            EI += 1
    print(
        f"Support {SUP}\nRefutes {REF}\nNot enough info {NEI}\n")
    return SUP, REF, NEI


def divide(file, max=None, sup=True, ref=True, nei=True):
    if max == None:
        max = len(file)
    SUP, REF, NEI = 0, 0, 0
    out_file = []
    for i in file:
        if i["label"] == 0 and SUP < max and sup:
            out_file.append(i)
            SUP += 1
        if i["label"] == 1 and REF < max and ref:
            out_file.append(i)
            REF += 1
        if i["label"] == 2 and NEI < max and nei:
            out_file.append(i)
            NEI += 1
    print(f"Support {SUP}\nRefutes {REF}\nNot enough info {NEI}")
    return out_file


def delete(file, max=None, sup=True, ref=True, nei=True):
    if max == None:
        max = len(file)
    SUP, REF, NEI = analyze(file)
    for i in file:
        if i["label"] == 0 and SUP > max and sup:
            file.remove(i)
            SUP -= 1
        if i["label"] == 1 and REF > max and ref:
            file.remove(i)
            REF -= 1
        if i["label"] == 2 and NEI > max and nei:
            file.remove(i)
            NEI -= 1
    print(f"Support {SUP}\nRefutes {REF}\nNot enough info {NEI}")
    return file


def change_ID(file) -> list:
    n = 2_500_000
    for i in file:
        try:
            if type(i["id"]) == str:
                i["id"] = n
                n -= 1
        except KeyError:
            i["id"] = n
            n -= 1
    return file


def encode_to_utf16(file):
    for i in file:
        i["claim"] = i["claim"].encode('utf-16').decode('unicode_escape')
        i["evidence"] = i["evidence"].encode('utf-16').decode('unicode_escape')
    return file


def convert_to_ASCII(text):
    return "".join([char for char in text if ord(char) < 128])


def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    return text.lower()


def clean(file):
    for i in file:
        i["claim"] = preprocess_text(i["claim"])
        i["evidence"] = preprocess_text(i["evidence"])
        i["claim"] = convert_to_ASCII(i["claim"])
        i["evidence"] = convert_to_ASCII(i["evidence"])
    return file


def combine(file1, file2):
    newFile = file1 + file2
    random.shuffle(newFile)
    return newFile


def split(file, train=0.8, test=0.1, val=0.1):
    train = int(len(file) * train)
    test = int(len(file) * test)
    val = int(len(file) * val)
    train_file = file[:train]
    test_file = file[train:train + test]
    val_file = file[train + test:train + test + val]
    return train_file, test_file, val_file

async def request(claim, label) -> str:
    prompt_template = f"claim: {claim} label: {label}"
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens=100,
    messages=[
            {"role": "system", "content": "You are a fact checking specialist. I will provide claim and label and you will justify why the claim is supports, not enough info or refutes."},
            {"role": "user", "content": prompt_template},
        ]
    )
    justify = response["choices"][0]["message"]["content"]
    return justify

def make_request(i):
    try:
        label_map = {0: "SUPPORTS", 1: "REFUTES", 2: "NOT ENOUGH INFO"}
        label = label_map[i["label"]] if i["label"] in label_map else i["label"]
        out = asyncio.run(request(i["claim"], label))
        return out
    except:
        print("sleeping")
        time.sleep(30)
        make_request(i)
    

if __name__ == "__main__":
    print("Anlys.py")
    ok = load("v3/track0.jsonl")
    show_loss(ok)

