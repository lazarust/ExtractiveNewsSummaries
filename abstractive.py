import string
from datetime import time

import pandas as pd
import re

import spacy

punctuation = string.punctuation + '\n' + '—' + '“' + ',' + '”' + '‘' + '-' + '’'


def format_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(punctuation), '', text)
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
df.drop(columns=['Unnamed: 0'], inplace=True)
print(f"What's the shape: {df.shape}")

articles = []
for i in range(df.shape[0]):
    articles.append(df.iloc[i]['content'])


nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])
