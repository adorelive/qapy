import os
import random
import json
import questionary
import textdistance
import re


# 主程序
def play():
    qa = [] # 问答列表
    q_nu = 0   # 题目编号
    mode = '=' # 改卷模式
    right_flag = False # 是否出现提示

    # 选择考题
    notes_file = load_config(config)
    note = questionary.select(
        "select",
        choices=notes_file,
    ).ask()

    # 退出
    if note == 'Exit': return

    # 读取文件
    note = re.sub(r'\(\d+/\d+\)', '', note)
    with open(f'./notes/{note}.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines[0][:5] == '#### ':
            mode = lines[0][5]
            lines.pop(0)
        for line in lines:
            two_col = line.strip().split('|', maxsplit=1)
            qa.append([two_col[0].strip(), two_col[1].strip()])
    # 打乱顺序
    random.shuffle(qa)
    for ql, al in qa:
        try_nu = 0 # 重试i次显示答案
        q_nu += 1
        ql = str(q_nu) + '/' + str(len(qa)) + ') ' + ql
        while True:
            try_nu += 1
            if try_nu == 3:
                ql += f'({al})'
                right_flag = True
            a = questionary.text(ql).ask()

            # 文本相似度 Jaccard相似度 Cosine相似度
            sim1 = textdistance.jaccard.normalized_similarity(a.strip(), al.strip())
            sim2 = textdistance.cosine.normalized_similarity(a.strip(), al.strip())

            if mode == '=' and (a.strip() == al.strip()): # 全等
                break
            if mode == '%' and (sim1 > 0.5 and sim2 > 0.5): # 模糊
                print(al.strip())
                print(a.strip())
                break

    # 保存配置
    note = note.split('.')[0]
    for item in config['notes']:
        if item['name'] == note:
            item['done_count'] += 1
            if not right_flag:
                item['right_count'] += 1

    # 返回菜单
    play()

# 加载保存配置
def load_config(cfg):
    global config
    if not cfg:
        with open('./config.json', 'r', encoding='utf-8') as f:
            cfg = json.load(f)

    notes = os.listdir('./notes/')
    notes_file = [item.split('.')[0] for item in notes]
    for idx, target_name in enumerate(notes_file):
        flag = False
        for item in cfg['notes']:
            if item['name'] == target_name:
                notes_file[idx] = f"{target_name}({item['right_count']}/{item['done_count']})"
                flag = True
        if not flag:
            notes_file[idx] = f"{target_name}(0/0)"
            cfg['notes'].append({'name': target_name, 'right_count': 0, 'done_count': 0})

    with open('./config.json', 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=4)

    config = cfg
    notes_file.append('Exit')
    return notes_file

# 开始
if __name__ == "__main__":
    print(' '.join(random.choice(["♥", '♠', '♣', '♦']) for _ in range(30)))
    config = {} # 全局配置
    play()
