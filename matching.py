#!/usr/bin/python

#The operation of retriving advertisers or documents matching a given query can be executed in two phases:
#in the first phase, we build the necessary data structures;
#in the second phase, we answer to the given query.

#The first phase is usually run only once.
#The data structure that is usually built in this phase is an "inverted index".
#This is a dictionary that for every word (or for every query phrase) mantains a list of
#documents containing that word (query phrase) / advertisers requesting to appear on that word (query phrase).
#In this phase, we assume that there is a database in which we save for each document (advertiser, resp.)
#the link to the document (the name of the advertiser, resp.)
#and the list of word (or phrases) of the document (on which the advertiser request to appear, resp.).
#In the implementations below we assume that the database is a file as follows:
#    nome_adv1 prova,test,prova esame,esame,appello,appello esame
#    nome_adv2 prova,esempio,caso semplice,evidenza
#    nome_adv3 esempio test,esempio esame,esempio prova,esame prova

###BEST MATCH###

import sys

#Creation of inverted index
#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
#We also create the non-inverted index, so that it's easy to compute frequencies
def create_word_advs(databasefile):
    inverted_index = dict()
    index = dict()

    with open(databasefile) as infile:
        
        for line in infile:
            line = line.rstrip()
            name_list = line.split(' ',1)
            name=name_list[0]
            if name not in index.keys():
                index[name] = dict()
            queries=name_list[1].split(',')
            
            for i in range(len(queries)):
                
                query_words=queries[i].split()
                
                for word in query_words:
                    if word not in index[name]:
                        index[name][word] = 0
                    if word not in inverted_index.keys():
                        inverted_index[word]=dict() 
                    if name not in inverted_index[word].keys():
                        inverted_index[word][name] = 0 
                    
                    index[name][word] += 1
                    inverted_index[word][name] += 1
    return (index, inverted_index)
    
#First variant, using only inverted_index
#Given a query, each document score is proportional to the number of times it contains query terms
def best_match(query, threshold, inverted_index):
    adv_weights = dict()
    best_docs = set()
    
    query_words = query.split()
    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in inverted_index[word].keys():
            if doc not in adv_weights.keys():
                adv_weights[doc] = inverted_index[word][doc]
            else:
                adv_weights[doc] += inverted_index[word][doc]

            #We use a threshold to choose which document must be returned
            if adv_weights[doc] >= threshold:
                best_docs.add(doc)
                
    return best_docs    

#Computes the frequency of word in document given the search index
def compute_frequency(index, document, word):
    num_total_words_in_doc = 0
    frequency = index[document][word]
    for word_doc in index[document].keys():
        num_total_words_in_doc += index[document][word_doc]
    frequency /= num_total_words_in_doc
    return frequency

#Second variant, using both index and inverted_index
#Given a query, each document score is proportional to the frequency of each query term in it
def best_match2(query, inverted_index, index):

    adv_weights = dict()
    query_words = query.split()

    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in inverted_index[word].keys():
            #Computing word frequence in doc
            frequency = compute_frequency(index, doc, word)
            if doc not in adv_weights.keys():
                adv_weights[doc] = frequency
            else:
                adv_weights[doc] += frequency

    best_docs = sorted(adv_weights, key=adv_weights.get, reverse=True)             
    if len(best_docs) > 20:
        return best_docs[0:19]
    else:
        return best_docs

#Sorts inverted index from the document with highest frequency to lowest
def sort_inverted_index(inverted_index, index):
    sorted_inverted_index = dict()
    for query_term in inverted_index.keys():
        frequencies = list()
        for doc in inverted_index[query_term]:
            frequencies.append((doc, compute_frequency(index, doc, query_term)))
        sorted_inverted_index[query_term] = sorted(frequencies, key= lambda x:x[1], reverse=True)
    return sorted_inverted_index

#Third variant, it must be compared with best_match2
#sorted_inverted_index is a dict. Key: words. Value: list of couples. Couples: First term:document. Second term:Frequency
def best_match3(query, sorted_inverted_index):

    query_words = query.split()

    impact = dict()
    for word in query_words:
        #The impact of a word is its frequency in the the document with the word's highest frequency
        impact[word] = sorted_inverted_index[word][0][1]
    sorted(impact, key=impact.keys(), reverse=True)

    return None #Fuck you bogs

if __name__ == "__main__":
    (index, inverted_index) = create_word_advs(sys.argv[1])
    print(sort_inverted_index(inverted_index, index))
