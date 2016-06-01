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
def create_word_advs(databasefile):
    word_advs = dict()

    with open(databasefile) as infile:
        
        for line in infile:
            line = line.rstrip()
            name_list = line.split(' ',1)
            name=name_list[0]
            queries=name_list[1].split(',')
            
            for i in range(len(queries)):
                
                query_words=queries[i].split()
                
                for word in query_words:
                
                    if word not in word_advs.keys():
                        word_advs[word]=dict() 
                    if name not in word_advs[word].keys():
                        word_advs[word][name] = 0 
                    
                    word_advs[word][name] += 1
    return word_advs
    
def best_match(query, threshold, databasefile='queryfile.txt'):
    adv_weights = dict()
    best_docs = set()
    
    query_words = query.split()
    word_advs = create_word_advs(databasefile)
    
    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in word_advs[word].keys():
            if doc not in adv_weights.keys():
                adv_weights[doc] = word_advs[word][doc]
            else:
                adv_weights[doc] += word_advs[word][doc]

            #We use a threshold to choose which document must be returned
            if adv_weights[doc] >= threshold:
                best_docs.add(doc)
                
    return best_docs    

if __name__ == "__main__":
    print(best_match(sys.argv[1], 0))
