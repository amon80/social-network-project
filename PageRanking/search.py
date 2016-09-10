from matching import best_match, best_match2, sort_inverted_index
from index import read_index
from ranking import read_ranking
from time import clock
from sys import argv
from graph import read_normalization_mapping

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
    #Loading indeces
    index, inv_index = read_index('total_index_with_spam_farm_normalized')
    sorted_inv_index = sort_inverted_index(inverted_index, index)
    #Loading rankings
    pageranks = read_ranking('total_graph_random_edges_and_spam_farm_normalized_pagerank')
    spammass_ranks = read_ranking('spamMass')
    #Loading mapping
    mapping, inv_mapping = read_normalization_mapping('normalized_mapping')
    #Starting queries

    #Best_match with pagerank
    start = clock()
    result_best_match_pagerank = query_database_pagerank_bestmatch(query, pageranks, index, inv_index)
    end = clock()
    result_best_match_pagerank_time = end - start

    #Best_match2 with pagerank
    start = clock()
    result_best_match2_pagerank = query_database_pagerank_bestmatch2(query, pageranks, index, sorted_inv_index)
    end = clock()
    result_best_match2_pagerank_time = end - start

    #Best_match with spammass
    start = clock()
    result_best_match_spammass = query_database_spammass_bestmatch(query, pageranks, spammass_ranks, index, inv_index)
    end = clock()
    result_best_match_pagerank_time = end - start

    #Best_match2 with spammass
    start = clock()
    result_best_match2_spammass = query_database_spammass_bestmatch2(query, pageranks, spammass_ranks, index, sorted_inv_index)
    end = clock()
    result_best_match2_spammass_time = end - start

