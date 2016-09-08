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
from index import read_index

#Creation of inverted index
#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
#We also create the non-inverted index, so that it's easy to compute frequencies
    
#First variant, using only inverted_index
#Given a query, each document score is proportional to the number of times it contains query terms
def best_match(query, threshold, inverted_index):
    scores = dict()
    best_docs = set()
    
    query_words = query.split()
    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in inverted_index[word].keys():
            if doc not in scores:
                scores[doc] = inverted_index[word][doc]
            else:
                scores[doc] += inverted_index[word][doc]

            #We use a threshold to choose which document must be returned
            if scores[doc] >= threshold:
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

    scores = dict()
    query_words = query.split()

    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in inverted_index[word].keys():
            #Computing word frequence in doc
            frequency = compute_frequency(index, doc, word)
            if doc not in scores:
                scores[doc] = (doc, frequency)
            else:
                scores[doc] = (doc, scores[doc][1] + frequency)

    best_docs = sorted(scores.items(), key = lambda x:x[1], reverse=True)
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


# The Score of a document depend on the frequency of a query term in that document,
# where the frequency is the ratio between the number of occurences of the term and
# total number of words in the document
def compute_score(query_term, doc_frequencies):
    number_occurences_term = doc_frequencies[query_term]
    total_occurences = 0
    for word_frequency in doc_frequencies.values():
        total_occurences += word_frequency
    return number_occurences_term / total_occurences


#Third variant, it must be compared with best_match2
#sorted_inverted_index is a dict. Key: words. Value: list of couples. Couples: First term:document. Second term:Frequency
def best_match3(query, sorted_inverted_index,index):    

    impacts = dict()            # key: doc_name     | value: impact
    scores  = dict()            # key: doc_name     | value: score (#occurence of query term / # words)
    #sorted_inverted_index      # key: query_item   | value: doc list
    #index                      # key: doc_name     | value: frequency list (word:frequency)
    query_words = query.split()

    ##2  For every query term define its possible impact on the score as the frequency of the most frequent document in its index
    for word in query_words:
        impacts[word] = sorted_inverted_index[word][0][1]

    ##3  Sort the query terms in decreasing order of impact
    query_term_ordered_by_impact = sorted(impacts, key=impacts.get, reverse=True)

    ##4 consider the first 20 documents in the index of the first query term
    current_query_term_index = 0
    # iterate until 20 scores have been computed or query terms are over
    while len(scores) < 20 and current_query_term_index < len(query_term_ordered_by_impact): 
        current_query_term = query_term_ordered_by_impact[current_query_term_index]
        current_doc_index = 0

        # iterate until 20 scores have been computed or all documents from current query term have been scored
        while len(scores) < 20 and current_doc_index < len(sorted_inverted_index[query_term_ordered_by_impact[current_query_term_index]]):
            current_doc_name = sorted_inverted_index[query_term_ordered_by_impact[current_query_term_index]][current_doc_index][0]
            ##5  Compute the score for each of these documents
            if current_doc_name not in scores:
                scores[current_doc_name] = compute_score(current_query_term,index[current_doc_name])
            current_doc_index += 1
        current_query_term_index += 1

    
    ##6  Consider the first term in which there are documents that have not been scored
    
    term_index = 0
    while term_index < len(query_term_ordered_by_impact):
        termDone = False
        query_term = query_term_ordered_by_impact[term_index]
        doc_index = 0
        while doc_index < len(sorted_inverted_index[query_term]) and not termDone:
            doc_name = sorted_inverted_index[query_term][doc_index][0]

            ##7 consider the first non-scored document in the index of this term;
            if doc_name not in scores:
                frequency_current_term  = index[doc_name][query_term]
                next_terms_impact = 0
                if term_index+1 < len(query_term_ordered_by_impact):
                    for i in range(term_index+1, len(query_term_ordered_by_impact)):
                        next_terms_impact += impacts[query_term_ordered_by_impact[i]]
                last_document_score = list(scores.items())[-1][1]

                #8  If the frequency of the current term in the current document plus the sum
                #   of the impact of nex terms is larger than the score of the 20-th scored document,
                #   then score this document and repeat from 7, otherwise consider the next term and
                #   repeat from 7
                if (frequency_current_term + next_terms_impact > last_document_score):
                    scores[doc_name] = compute_score(query_term,index[doc_name])
                else:
                    termDone = True
            doc_index += 1
        term_index +=1

    # sorted_scores = sorted(scores,key=),reverse=True)
    sorted_scores = sorted(scores.items(), key = lambda x:x[1], reverse=True)

    
    #9  Return the 20 documents with higher score
    if len(sorted_scores) > 20:
        return sorted_scores[0:19]
    else:
        return sorted_scores


if __name__ == "__main__":
    (index, inverted_index) = read_index(sys.argv[1])
    
    print(index)

    new_query = "prova vasco"

    ##1  Sort documents in each inverted index in order of frequency of the derm at which the inverted index refers
    # sorted_inverted_index = sort_inverted_index(inverted_index, index)
    #
    # res = best_match3(new_query,sorted_inverted_index,index)
    # print(new_query)
    #
    # i=0
    # for re in res:
    #     i+=1
    #     print("\n#",i,)
    #     print(re[0])
    #     print("Frequency:",re[1])
    #     print("Doc:")
    #     print(index[re[0]])
    #     print("\n")
