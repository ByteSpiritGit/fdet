import json
from datasets import load_dataset
import matplotlib.pyplot as plt
import random
import requests


def load(path):
    file = []
    with open(path, 'r') as f:
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
        f"Support {SUP}\nRefutes {REF}\nNot enough info {NEI}\nEnough info {EI}")
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


def combine(file1, file2):
    newFile = file1 + file2
    random.shuffle(newFile)
    return newFile
