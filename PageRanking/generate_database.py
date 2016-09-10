import random

#n_elements and n_couples adapted to our graph
def add_random_edges_to_total_graph(graph, n_elements = 878, num_couples = 4):
    ngroups = len(graph.keys()) // n_elements
    nodes = list(graph.keys())
    for i in range(ngroups-1):
        for j in range(i+1, ngroups):
            for k in range(num_couples):
                added = False
                while not added:
                    random1 = random.randint(i*n_elements, (i+1)*n_elements)
                    random2 = random.randint(j*n_elements, (j+1)*n_elements)
                    if nodes[random2] not in graph[nodes[random1]]:
                        graph[nodes[random1]].add(nodes[random2])
                        added = True

def find_most_frequent_term(index, doc, termsToAvoid = set()):
    most_frequent_score = 0
    most_frequent_term = ""
    for actual_term in index[doc]:
        actual_term_frequency = index[doc][actual_term]
        if actual_term_frequency > most_frequent_score and actual_term not in termsToAvoid:
            most_frequent_score = actual_term_frequency
            most_frequent_term = actual_term
    return (most_frequent_term, most_frequent_score)

#Use on non normalized graph
def create_spam_farm(graph, index, supporting_pages = 35, random_pages_linking_spam = 10):
    nodes_without_spam = list(graph.keys())
    num_nodes_without_spam = len(nodes_without_spam)
    #Creating target page
    graph["target"] = set()
    index["target"] = dict()
    #Creating supporting pages and linking two way with target page
    for i in range(supporting_pages):
        spam_page_name = "spam"+str(i)
        index[spam_page_name] = dict()
        graph[spam_page_name] = set()
        graph[spam_page_name].add("target")
        graph["target"].add(spam_page_name)
    #Adding links from random_pages_linking_spam to target page
    for i in range(random_pages_linking_spam):
        r = random.randint(0, num_nodes_without_spam-1)
        graph[nodes_without_spam[r]].add("target")
    #Builing target paged index
    most_frequent_terms_with_frequencies = list()
    most_frequent_terms = set()
    for node in nodes_without_spam:
        #smaller index means most frequent term or less frequent?
        result = find_most_frequent_term(index, node, most_frequent_terms)
        if result[1] == 0:
            continue
        most_frequent_terms_with_frequencies.append(result)
        most_frequent_terms.add(result[0])
    sorted_most_frequent_terms = sorted(most_frequent_terms_with_frequencies, key = lambda x:x[1], reverse=True)
    actual_size = min(len(sorted_most_frequent_terms), 500)
    for i in range(actual_size):
        if sorted_most_frequent_terms[i][0] not in index["target"]:
            index["target"][sorted_most_frequent_terms[i][0]] = sorted_most_frequent_terms[i][1]

