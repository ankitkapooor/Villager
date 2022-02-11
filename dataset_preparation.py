import pandas as pd
import json

with open('Dataset/train.json', 'r', encoding = "UTF-8") as f:
    with open('Dataset/processsed.txt', 'w', encoding = "UTF-8") as g:
        data = json.load(f)
        for idx, i in enumerate(data):
            for j in data[i]['content']:
                g.write(f'{j["agent"]}: {j["message"]}\n')
        g.write('agent_2: Null')

df = pd.DataFrame()

temp, User, Bot = [], [], []
with open('Dataset/processsed.txt', 'r', encoding = "UTF-8") as f:
    temp = f.readlines()
    for idx, x in enumerate(temp):
        if "agent_1" in x and "agent_2" in temp[idx+1]:
            User.append(x[9:])
        elif "agent_2" in x and "agent_1" in temp[idx-1]:
            Bot.append(x[9:])

df['User'] = User
df['Bot'] = Bot

special_token = ' <|endoftext|> '
df['train_param'] = 'User: ' + df.User + 'Bot: ' + df.Bot + special_token
#print(df.iloc[100].train_param)

df.to_pickle('Dataset/df_preprocessed.pkl')

dataset_train = df[:90000].train_param.values
dataset_val = df[90000:].train_param.values

with open('Dataset/dataset_train.txt', 'w', encoding = 'UTF-8') as f:
  f.write('\n'.join(dataset_train))

with open('Dataset/dataset_val.txt', 'w', encoding = 'UTF-8') as f:
  f.write('\n'.join(dataset_val))
