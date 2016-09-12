from index import read_index
from sys import argv
from matching import best_match, best_match2, sort_inverted_index
from time import clock
from random import randint

if __name__ == "__main__":
    index, inv_index = read_index(argv[1], integer = True, also_inverted = True)
    terms = list(inv_index.keys())
    num_queries = int(argv[2])
    len_range = range(1,int(argv[3]))

    sorted_inverted_index = sort_inverted_index(inv_index, index)
    print("Finished to sort the inverted index")
    
    for j in len_range:
        with open('best_match_'+str(j)+'_terms_times', 'w') as best_match_times:
            with open('best_match_'+str(j)+'_terms_results', 'w') as best_match_results:
                with open('best_match2_'+str(j)+'_terms_times', 'w') as best_match2_times:
                    with open('best_match2_'+str(j)+'_terms_results', 'w') as best_match2_results:
                        for i in range(num_queries):
                            query = ""
                            for i in range(j):
                                query += terms[randint(0, len(terms) - 1)] + " "

                            print("Query is " + query)

                            start = clock()
                            results = best_match(query, inv_index, index)
                            doc_results = []
                            for res in results:
                                doc_results.append(res[0])
                            end = clock()
                            time_best_match = end - start

                            start = clock()
                            results2 = best_match2(query, sorted_inverted_index, index)
                            doc_results2 = []
                            for res in results2:
                                doc_results2.append(res[0])
                            end = clock()
                            time_best_match2 = end - start

                            best_match_times.write(str(time_best_match)+"\n")
                            best_match2_times.write(str(time_best_match2)+"\n")
                            for doc in doc_results:
                                best_match_results.write(str(doc) + " ")
                            best_match_results.write("\n")
                            for doc in doc_results2:
                                best_match2_results.write(str(doc) + " ")
                            best_match2_results.write("\n")
