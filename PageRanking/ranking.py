from numpy import add,dot,multiply
from math import sqrt

#All the functions in this module work only with an integer graph
#usually given as a transition matrix. So be sure to normalize your graph.

#for inverse pagerank give the function the inverse transition matrix
def matricial_pageRank(transition_matrix, s=0.85, step=1000, confidence=0, tax = None, rank = None, verbose = True):
    n = len(transition_matrix)
    nodes = range(n)
    done = False
    time = 0

    if rank is None:
        rank = []
        for i in nodes:
            rank.append(1/n)
    if tax is None:
        tax = []
        for i in nodes:
            tax.append(1/n)

    first_term = multiply(s,transition_matrix)
    second_term = multiply((1-s),tax)
    while not done and time < step:
        time += 1 
        first_term_bis = dot(first_term, rank)
        tmp = add(first_term_bis, second_term)
        diff = 0
        #tmp is a linear matrix, with this command we take the vector
        tmp = tmp.A1
        for i in nodes:
            diff += abs(rank[i]-tmp[i])
            rank[i] = tmp[i]

        if verbose:
            print(str(time) + " - diff: " + str(diff))
        if diff <= confidence:
            done = True
    return time, rank

def matricial_trustRank(transition_matrix, trusted_pages, s=0.85, step = 1000, confidence = 0, verbose = True):
    tax_vector = list()
    n = len(transition_matrix)
    for i in range(n):
        tax_vector.append(0)
    for page in trusted_pages:
        tax_vector[page] = 1
    rank_vector = list(tax_vector)
    tax_vector = multiply((1/len(trusted_pages)),tax_vector)
    time, rank = matricial_pageRank(transition_matrix, tax = tax_vector, rank = rank_vector, verbose = verbose, confidence = confidence, s = s, step = step)
    return time,rank

def order_nodes(nodes, scores):
    tmp = dict()
    for i in nodes:
        tmp[i] = scores[i]
    return sorted(tmp, key=tmp.__getitem__, reverse = True)

# A negative or small positive spam mass means that p is probably not a spam page,
# while a spam mass close to 1 suggests that the page probably is spam.
def spamMass(graph, trusted_pages, s=0.85, step=1000, confidence=0.001, prRank = None, trRank = None):
    if prRank == None:
        prTime, prRank = matricial_pageRank(graph, s, step, confidence)
    if trRank == None:
        trTime, trRank = trustRank(graph, trusted_pages, s, step, confidence)

    finalRank = dict()
    for node in graph.keys():
        finalRank[node] = ( prRank[node] - trRank[node] ) / prRank[node] 

    return finalRank

def read_trusted_pages(trusted_pages_list):
    pages = list()
    with open(trusted_pages_list, 'r') as f:
        for line in f:
            line = line.rstrip()
            pages.append(int(line))
    return pages

def read_rankings(rankfile):
    rankings = list()
    with open(rankfile, 'r') as f:
        for line in f:
            line = line.rstrip()
            rank = float(line)
            rankings.append(rank)
    return rankings

def write_rankings(rankings, rankfile):
    with open(rankfile, 'w') as f:
        for rank in rankings:
            f.write(str(rank)"\n")

if __name__ == "__main__":
    from graph import read_integer_graph, get_transition_matrix, get_inverse_transition_matrix
    from ranking import matricial_pageRank, pageRank, matricial_trustRank, order_nodes, write_rankings, read_rankings
    from sys import argv
    graph = read_integer_graph(argv[1])
    print("Finished Read graph")
    transition_matrix = matrix(get_transition_matrix(graph))
    print("Finished Get transition_matrix")
    inv_transition_matrix = matrix(get_inverse_transition_matrix(graph))
    print("Finished Get inv_transition_matrix")
    inv_step, inv_scores = matricial_pageRank(inv_transition_matrix, step = 1000, confidence = 0.001, verbose = True)
    print("Finished inverse pageRank")
    prTime, prRank = matricial_pageRank(transition_matrix, step = 1000, confidence = 0.001, verbose = True)
    print("Finished classical pageRank")

    # nodes = range(len(graph))
    # ordered_nodes_inv = order_nodes(nodes, inv_scores)
    # print("Nodes ranked using inverted pagerank")
    # print(ordered_nodes_inv[:20])
    # ordered_nodes= order_nodes(nodes, prRank)
    # print("Nodes ranked using pageRank")
    # print(ordered_nodes[:20])
    # trTime, trRank = matricial_trustRank(transition_matrix, [1 , 3,], step = 1000, confidence = 0.001 verbose = False)
