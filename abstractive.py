import string

import pandas as pd
import re


def format_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

df1 = pd.read_csv('data/articles1.csv', ',')
df2 = pd.read_csv('data/articles2.csv', ',')
df3 = pd.read_csv('data/articles3.csv', ',')
dfs = [df1, df2, df3]
df = pd.concat(dfs)

del df['url']
del df['month']
del df['year']

df['content'] = df['content'].apply(format_text)

for x in range(df.shape()[0]):
    print(df.iloc[x])
