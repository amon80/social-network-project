from matching import best_match, best_match2, sort_inverted_index
from index import read_index
from ranking import read_ranking
from sys import argv

def query_database_pagerank_bestmatch(query, pageranks, index, inverted_index):
    final_scores = dict()
    best_docs_matching_scores = dict()
    best_docs_rank_scores = dict()

    #computing matching score
    best_docs_as_list_of_tuples = best_match(query, inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]
    
    #combining the two scores
    for doc in best_docs:
        final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]

    return sorted(final_scores.items(), key=final_scores.get, reverse=True)

#inverted_index must be given already sorted
def query_database_pagerank_bestmatch2(query, pageranks, index, sorted_inverted_index):
    final_scores = dict()
    best_docs_matching_scores = dict()
    best_docs_rank_scores = dict()

    #computing matching score
    best_docs_as_list_of_tuples = best_match2(query, sorted_inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]
    
    #combining the two scores
    for doc in best_docs:
        final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]

    return sorted(final_scores.items(), key=final_scores.__getitem__, reverse=True)

def query_database_spammass_bestmatch(query, pageranks, spammass_ranks, index, inverted_index, spammass_threshold = 0.70):
    final_scores = dict()
    best_docs_matching_scores = dict()

    #computing matching score
    best_docs_as_list_of_tuples = best_match(query, inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]
    
    #combining the two scores
    for doc in best_docs:
        if spammass_ranks[doc] > spammass_threshold:
            final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]
        else:
            final_scores[doc] = 0

    return sorted(final_scores.items(), key=final_scores.__getitem__, reverse=True)

#inverted_index must be given already sorted
def query_database_spammass_bestmatch2(query, pagerank, spammass_ranks, index, sorted_inverted_index, spammass_threshold = 0.70):
    final_scores = dict()
    best_docs_matching_scores = dict()
    best_docs_rank_scores = dict()

    #computing matching score
    best_docs_as_list_of_tuples = best_match2(query, sorted_inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]
    
    #combining the two scores
    #since spammass >= to 1 when its spam, the scores remains the same. If spammass is little or negative, score is boosted
    for doc in best_docs:
        if spammass_ranks[doc] > spammass_threshold:
            final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]
        else:
            final_scores[doc] = 0

    return sorted(final_scores.items(), key=final_scores.get, reverse=True)

if __name__ == "__main__":
    query = ""
    for i in range(1, len(argv)):
        query += argv[i] + " "

