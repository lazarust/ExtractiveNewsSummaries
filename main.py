from bs4 import BeautifulSoup
import requests
import nltk
from newspaper import Article

res = requests.get('https://www.theverge.com/rss/index.xml')
soup = BeautifulSoup(res.text, 'html.parser')

text = []
for link in soup.findAll('link')[1:]:
    article = Article(link['href'])
    article.download()
    article.parse()
    article.nlp()
    text.append((article.title, article.text))