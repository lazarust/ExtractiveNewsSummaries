from bs4 import BeautifulSoup
import requests
import spacy
import pytextrank
from newspaper import Article
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


def create_vocab(docx, extra_words):
    all_words = [word.text for word in docx]
    Freq_word = {}
    for w in all_words:
        w1 = w.lower()
        if w1 not in extra_words and w1.isalpha():
            if w1 in Freq_word.keys():
                Freq_word[w1] += 1
        else:
            Freq_word[w1] = 1

    return Freq_word

def create_headline(Freq_word):
    val = sorted(Freq_word.values())
    max_freq = val[-3:]
    print("Topic of document given :-")
    for word, freq in Freq_word.items():
        if freq in max_freq:
            pass
        else:
            continue
    return max_freq


extra_words = list(STOP_WORDS) + list(punctuation) + ['\n']
res = requests.get('https://www.theverge.com/rss/index.xml')
soup = BeautifulSoup(res.text, 'html.parser')
nlp = spacy.load("en_core_web_sm")
tr = pytextrank.TextRank()

nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)

summaries = []
text = []
for link in soup.findAll('link')[1:]:
    article = Article(link['href'])
    article.download()
    article.parse()
    text.append((article.title, article.text))
    docx = nlp(article.text)
    Freq_word = create_vocab(docx, extra_words)
    max_freq = create_headline(Freq_word)
    for word in Freq_word.keys():
        Freq_word[word] = (Freq_word[word] / max_freq[-1])

    sent_strength = {}
    for sent in docx.sents:
        for word in sent:
            if word.text.lower() in Freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += Freq_word[word.text.lower()]
                else:
                    sent_strength[sent] = Freq_word[word.text.lower()]
        else:
            continue

    top_sentences = (sorted(sent_strength.values())[::-1])
    top30percent_sentence = int(0.5 * len(top_sentences))
    top_sent = top_sentences[:top30percent_sentence]

    summary = []
    for sent, strength in sent_strength.items():
        if strength in top_sent:
            summary.append(sent)
        else:
            continue

    summaries.append(str(summary))

print(summaries)