#!/usr/bin/python

import string
import nltk
import urllib.request
import lxml
import sys
from nltk.stem import WordNetLemmatizer
from lxml.html.clean import Cleaner
from html.parser import HTMLParser
from MyException import MyException

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#Given a file with a stopword for line, constructs a set with stopwords
def stop_word_list_constructor(stopword_file):
    stopwords = set()
    with open(stopword_file) as infile:
        for line in infile:
            line = line.rstrip()
            stopwords.add(line)
    return stopwords

#Given a document as a single large string, returns the list of all words (avoiding stopwords, punctuation, lemmatizing words)
def document_parser(document, removeLowFrequency=True, lowFrequency=1):
    #key = the word, value = count
    document_words = dict()
    stopwords = stop_word_list_constructor('stopword_list.txt')
    wordnet_lemmatizer = WordNetLemmatizer()
    admitted_tags = set();
    admitted_tags.add("NN")
    admitted_tags.add("NNS")
    admitted_tags.add("NNP")
    admitted_tags.add("NNPS")
    admitted_tags.add("JJ")
    tokens = nltk.word_tokenize(document)
    tagged_tokens = nltk.pos_tag(tokens)
    for tagged_token in tagged_tokens:
        tag = tagged_token[1]
        if tag in admitted_tags:
            word = tagged_token[0]
            word = wordnet_lemmatizer.lemmatize(word)
            if word not in stopwords and len(word) > 2:
                if word not in document_words.keys():
                    document_words[word] = 0
                document_words[word] += 1
    if removeLowFrequency:
        toRemove = list()
        for key,value in document_words.items():
            if value <= lowFrequency:
                toRemove.append(key)
        for keyToremove in toRemove:
            document_words.pop(keyToremove)
    return document_words

#Given a url gets the document, cleans it and parses it
def get_parsed_document(url,verbose = True):
    try:
        with urllib.request.urlopen(url, timeout = 3) as connection:
            html = connection.read()
        dom = lxml.html.fromstring(html)
        cleaner = Cleaner(style = True, links = True, javascript = True, meta = True, scripts = True, comments = True, forms = True, annoying_tags = True, frames = True)
        cleaner(dom)
        raw = dom.text_content()
        raw = strip_tags(raw)
        raw = raw.rstrip()
        #removing punctuation and trailers
        translator = str.maketrans({key: None for key in string.punctuation})
        raw = raw.translate(translator)
        raw = raw.replace('\'', ' ')
        raw = raw.replace('\n', ' ')
        raw = raw.replace('\t', ' ')
        raw = raw.replace('\r', ' ')
        raw = raw.lower()
        #removing non ascii characters
        raw = ''.join([i if ord(i) < 128 else ' ' for i in raw])
        return document_parser(raw)
    except:
        raise MyException(url + " caused error while gettint it's contents")


if __name__ == "__main__":
    words = get_parsed_document(sys.argv[1])
    sorted_words = sorted(words, key=words.get, reverse=True)
    for word in sorted_words:
        print(word + " - " + str(words[word]))
