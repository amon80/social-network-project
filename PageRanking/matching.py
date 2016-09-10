#!/usr/bin/python

###BEST MATCH###

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
def best_match(query, inverted_index, index):

    scores = dict()
    query_words = query.split()

    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        try:
            documents_responding_to_word = inverted_index[word]
        except KeyError:
            continue
        for doc in documents_responding_to_word:
            #Computing word frequence in doc
            frequency = compute_frequency(index, doc, word)
            if doc not in scores:
                scores[doc] = (doc, frequency)
            else:
                scores[doc] = (doc, scores[doc][1] + frequency)
    if len(scores) == 0:
        return []


    scores_as_list = list(scores.values())
    best_docs = sorted(scores_as_list, key = lambda x:x[1], reverse=True)
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


#sorted_inverted_index is a dict. Key: words. Value: list of couples. Couples: First term:document. Second term:Frequency
def best_match2(query, sorted_inverted_index, index):    

    impacts = dict()            # key: doc_name     | value: impact
    scores  = dict()            # key: doc_name     | value: score (#occurence of query term / # words)
    #sorted_inverted_index      # key: query_item   | value: doc list
    #index                      # key: doc_name     | value: frequency list (word:frequency)
    query_words = query.split()

    ##2  For every query term define its possible impact on the score as the frequency of the most frequent document in its index
    for word in query_words:
        try:
            impacts[word] = sorted_inverted_index[word][0][1]
        except KeyError:
            continue
    if len(impacts) == 0:
        return []

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
