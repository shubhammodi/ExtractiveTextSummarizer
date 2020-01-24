# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:36:32 2020
Extractive Summarizer

@author: MODIS1
"""
import re
import urllib.request
from heapq import nlargest
import bs4 as bs
import nltk
nltk.download('stopwords')


SOURCE = urllib.request.urlopen('https://en.wikipedia.org/wiki/Aircraft_in_fiction')


SOUP = bs.BeautifulSoup(SOURCE, 'lxml')

TEXT = ""
for paragraph in SOUP.find_all('p'):
    TEXT += paragraph.text
# Preprocessing the text

def preprocessing_text(text):
    '''Preprocessing the text'''
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    clean_text = text.lower()
    clean_text = re.sub(r'\W', ' ', clean_text)
    clean_text = re.sub(r'\d', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text

SENTENCES = nltk.sent_tokenize(TEXT)
STOP_WORDS = nltk.corpus.stopwords.words('english')
WORD2COUNT = {}

def word2count_score(text):
    '''Creating Dictionary for word count score'''
    for word in nltk.word_tokenize(preprocessing_text(text)):
        if word not in STOP_WORDS:
            if word not in WORD2COUNT:
                WORD2COUNT[word] = 1
            else:
                WORD2COUNT[word] += 1
    for key in WORD2COUNT:
        WORD2COUNT[key] = WORD2COUNT[key]/max(WORD2COUNT.values())
    return WORD2COUNT

SENT2SCORE = {}
WORD2COUNT = word2count_score(TEXT)
def sent2count_score():
    '''Creating Dictionary for each sentence score using their word count score'''
    for sentence in SENTENCES:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in WORD2COUNT:
    #            if len(sentence.split(' ')) < 25:
                if sentence not in SENT2SCORE:
                    SENT2SCORE[sentence] = WORD2COUNT[word]
                else:
                    SENT2SCORE[sentence] += WORD2COUNT[word]
    return SENT2SCORE

SENT2SCORE = sent2count_score()
# Selecting the top scored sentences for our extractive summary
BEST_SENTENCES = nlargest(120, SENT2SCORE, key=SENT2SCORE.get)

print('Following are the best rated sentences -->>')
for best_sentence in BEST_SENTENCES:
    print(best_sentence)
