import os
import random
import questionary


print(' '.join(random.choice(["♥", '♠', '♣', '♦']) for _ in range(30)))

def play():
    qa = [] # 问答列表
    j = 0   # 题目编号
    notes = os.listdir('./notes/')
    notes.append('exit')
    notes_file = [item.split('.')[0] for item in notes]
    note = questionary.select(
        "select",
        choices=notes_file,
    ).ask()
    # 退出
    if note == 'exit': return
    # 读取文件
    with open(f'./notes/{note}.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            two_col = line.strip().split('|', maxsplit=1)
            qa.append([two_col[0].strip(), two_col[1].strip()])
    # 打乱顺序
    random.shuffle(qa)
    for ql, al in qa:
        i = 0
        j += 1
        ql = str(j) + '/' + str(len(qa)) + ') ' + ql
        while True:
            i += 1
            if i == 3: ql += f'({al})'
            a = questionary.text(ql).ask()
            if a.strip() == al.strip():
                break
    # 返回菜单
    play()

# 开始
play()