import json
import matplotlib.pyplot as plt
import random


def load(path):
    file = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            file.append(json.loads(line))
    return file

def save(file, path):
    with open(path, 'w', encoding="utf-8") as f:
        for line in file:
            json.dump(line, f)
            f.write('\n')

def show_grap_XY(X,Y):
    plt.plot(X, Y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graph')
    plt.show()

def analyze(file):
    SUP,REF,NEI = 0, 0, 0
    for j, i in enumerate(file):
        if i["label"] == "SUPPORTS" or i["label"] == 0 :
            SUP += 1
        elif i["label"] == "REFUTES" or i["label"] == 1:
            REF += 1
        elif i["label"] == "NOT ENOUGH INFO" or i["label"] == 2:
            NEI += 1
    print(f"Support {SUP}\nRefutes {REF}\nNot enough info {NEI}")

def divide(file, out_file):
    SUP,REF,NEI = 0,0,0
    for j, i in enumerate(file):
        if i["label"] == 0 and SUP < 7148:
            json.dump(i, out_file)
            out_file.write("\n")
            SUP += 1
        if i["label"] == 1 and REF < 7148:
            json.dump(i, out_file)
            out_file.write("\n")
            REF += 1
        if i["label"] == 2:
            json.dump(i, out_file)
            out_file.write("\n")
            NEI += 1
    print(f"Support {SUP}\nRefutes {REF}\nNot enough info {NEI}")

def combine(file1, file2):
    newFile = file1 + file2
    random.shuffle(newFile)
    return newFile
