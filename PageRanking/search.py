from matching import best_match, best_match2, sort_inverted_index
from index import read_index
from ranking import read_rankings
from time import clock
from normalize import read_normalization_map
from sys import argv

def query_database_pagerank_bestmatch(query, pageranks, index, inverted_index):
    final_scores = dict()
    best_docs_matching_scores = dict()


    #computing matching score
    best_docs_as_list_of_tuples = best_match(query, inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]
    
    #combining the two scores
    for doc in best_docs_matching_scores:
        final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]

    return sorted(final_scores.keys(), key=final_scores.__getitem__, reverse=True)

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
    for doc in best_docs_matching_scores:
        final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]

    return sorted(final_scores.keys(), key=final_scores.__getitem__, reverse=True)

def query_database_spammass_bestmatch(query, pageranks, spammass_ranks, index, inverted_index, spammass_threshold = 0.70):
    final_scores = dict()
    best_docs_matching_scores = dict()

    #computing matching score
    best_docs_as_list_of_tuples = best_match(query, inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]
    
    #combining the two scores
    for doc in best_docs_matching_scores:
        if spammass_ranks[doc] > spammass_threshold:
            final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]
        else:
            final_scores[doc] = 0

    return sorted(final_scores.keys(), key=final_scores.__getitem__, reverse=True)

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
    for doc in best_docs_matching_scores:
        if spammass_ranks[doc] > spammass_threshold:
            final_scores[doc] = best_docs_matching_scores[doc] * pageranks[doc]
        else:
            final_scores[doc] = 0

    return sorted(final_scores.keys(), key=final_scores.__getitem__, reverse=True)

def convert_pages_from_integers_to_url(list_pages_as_indeces, pages_mapping):
    converted_pages = list()
    for page in list_pages_as_indeces:
        converted_pages.append(pages_mapping[page])
    return converted_pages

if __name__ == "__main__":
    query = ""
    for i in range(1, len(argv)):
        query += argv[i] + " "
    #Loading indeces
    index, inv_index = read_index('total_index_with_spam_farm_normalized')
    sorted_inv_index = sort_inverted_index(inv_index, index)
    #Loading rankings
    pageranks = read_rankings('total_graph_random_edges_and_spam_farm_normalized_pagerank')
    spammass_ranks = read_rankings('spamMass')
    #Loading mapping
    mapping, inv_mapping = read_normalization_map('normalized_mapping')
    #Starting queries

    #Best_match with pagerank
    start = clock()
    result_best_match_pagerank = query_database_pagerank_bestmatch(query, pageranks, index, inv_index)
    result_best_match_pagerank_for_human = convert_pages_from_integers_to_url(result_best_match_pagerank, inv_mapping)
    end = clock()
    result_best_match_pagerank_time = end - start

    #Best_match2 with pagerank
    start = clock()
    result_best_match2_pagerank = query_database_pagerank_bestmatch2(query, pageranks, index, sorted_inv_index)
    result_best_match2_pagerank_for_human = convert_pages_from_integers_to_url(result_best_match2_pagerank, inv_mapping)
    end = clock()
    result_best_match2_pagerank_time = end - start

    #Best_match with spammass
    start = clock()
    result_best_match_spammass = query_database_spammass_bestmatch(query, pageranks, spammass_ranks, index, inv_index)
    result_best_match_spammass_for_human = convert_pages_from_integers_to_url(result_best_match_spammass, inv_mapping)
    end = clock()
    result_best_match_pagerank_time = end - start

    #Best_match2 with spammass
    start = clock()
    result_best_match2_spammass = query_database_spammass_bestmatch2(query, pageranks, spammass_ranks, index, sorted_inv_index)
    result_best_match2_spammass_for_human = convert_pages_from_integers_to_url(result_best_match2_spammass, inv_mapping)
    end = clock()
    result_best_match2_spammass_time = end - start

