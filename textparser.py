#!/usr/bin/python

import string
import nltk
from nltk.stem import WordNetLemmatizer

#Given a file with a stopword for line, constructs a set with stopwords
def stop_word_list_constructor(stopword_file):
    stopwords = set()
    with open(stopword_file) as infile:
        for line in infile:
            line = line.rstrip()
            stopwords.add(line)
    return stopwords

#Given a document, returns the list of all words (avoiding stopwords, punctuation, lemmatizing words)
def document_parser(document):
    #key = the word, value = count
    document_words = dict()
    stopwords = stop_word_list_constructor('stopword_list.txt')
    translator = str.maketrans({key: None for key in string.punctuation})
    wordnet_lemmatizer = WordNetLemmatizer()
    admitted_tags = set();
    admitted_tags.add("NN")
    admitted_tags.add("NNS")
    admitted_tags.add("NNP")
    admitted_tags.add("NNPS")
    admitted_tags.add("JJ")
    with open(document) as infile:
        for line in infile:
            line = line.rstrip()
            line = line.translate(translator)
            line = line.replace('\'', ' ')
            line = line.lower()
            #removing non ascii characters
            line = ''.join([i if ord(i) < 128 else ' ' for i in line])
            #removing digits
            line = ''.join([i for i in line if not i.isdigit()])
            tokens = nltk.word_tokenize(line)
            tagged_tokens = nltk.pos_tag(tokens)
            for tagged_token in tagged_tokens:
                tag = tagged_token[1]
                if tag in admitted_tags:
                    word = tagged_token[0]
                    word = wordnet_lemmatizer.lemmatize(word)
                    if word not in stopwords and len(word) > 1:
                        if word not in document_words.keys():
                            document_words[word] = 0
                        document_words[word] += 1
    return document_words

if __name__ == "__main__":
    words = document_parser('prova.txt')
    print(sorted(words, key=words.get, reverse=True))
