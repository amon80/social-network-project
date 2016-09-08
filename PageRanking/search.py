def query_database(query, graph, ranks, index, inverted_index, matching_function, alpha = 1, beta = 2):
    final_scores = dict()
    best_docs_matching_scores = dict()
    best_docs_rank_scores = dict()

    best_docs_as_list_of_tuples = matching_function(query, inverted_index, index) 
    for best_doc_tuple in best_docs_as_list_of_tuples:
        best_docs_matching_scores[best_doc_tuple[0]] = best_doc_tuple[1]

    for doc in best_docs:
        best_docs_rank_scores[doc] = ranks[doc]
    
    for doc in best_docs:
        final_scores[doc] = alpha * best_docs_matching_scores[doc] + beta * best_docs_rank_scores[doc]

    return sorted(final_scores.items(), key=final_scores.get, reverse=True)
