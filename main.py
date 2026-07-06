import re
import os
import random
import questionary


print(' '.join(random.choice(["♥", '♠', '♣', '♦']) for _ in range(30)))

def play():
    qa = []
    j = 0
    notes = os.listdir('./notes/') + ['exit'],
    note = questionary.select(
        "select",
        choices=notes[0],
    ).ask()
    if note == 'exit': return
    # 读取文件
    with open(f'./notes/{note}', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            two_col = line.strip().split('|', maxsplit=1)
            qa.append([two_col[0].strip(), two_col[1].strip()])
    for ql, al in qa:
        i = 0
        j += 1
        ql = str(j) + '/' + str(len(qa)) + ') ' + ql
        while True:
            i += 1
            if i == 3: ql += f'({al})'
            a = questionary.text(ql).ask()
            if a == al:
                break
    play()

play()