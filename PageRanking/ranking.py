# As seen during the course
# Pagerank with teleport
from numpy import add,dot,multiply
from math import sqrt

#matricial_pagerank works only on normlized graph given as transition matrix
#for inverse pagerank give the function the inverse transition matrix
#if given, tax must be a vector that sums to one(biased pagerank)
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

#As above
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

#Works only on integer graphs
def order_nodes(nodes, scores):
    tmp = dict()
    for i in nodes:
        tmp[i] = scores[i]
    return sorted(tmp, key=tmp.__getitem__, reverse = True)

def pageRank(graph, s=0.85, step=1000, confidence=0, verbose = True):
    nodes = graph.keys()
    n = len(nodes)
    done = 0
    time = 0

    # Initialization
    rank = dict()
    for node in nodes:
        rank[node] = float(1)/n

    tmp = dict()
    done = False
    while not done and time < step:
        time += 1
        if verbose:
            print(time)

        for node in nodes:
        # Each node receives a share of 1/n with probability 1-s
            tmp[node] = float(1-s)/n 

        for node in nodes:
            for neighbour in graph[node]:
                # Each node receives a fraction of its neighbour rank with probability s
                tmp[neighbour] += float(s*rank[node])/len(graph[node])

        # Computes the distance between the old rank vector and the new rank vector in L_1 norm
        diff = 0
        for node in nodes:
            diff += abs(rank[node] - tmp[node])
            rank[node] = tmp[node]

        if diff <= confidence:
            done = True
    return time, rank


# The idea behind spam mass is that we measure for each page the fraction
# of its PageRank that comes from spam. We do so by computing both the 
# ordinary PageRank and the TrustRank based on some teleport set of trustworthy pages.
# Suppose page p has PageRank r and TrustRank t. Then the spam mass of p is
# (r-t)/r. 
# A negative or small positive spam mass means that p is probably not a spam page,
# while a spam mass close to 1 suggests that the page probably is spam.
def spamMass(graph, trusted_pages, s=0.85, step=1000, confidence=0, prRank = None, trRank = None):
    if prRank == None:
        prTime, prRank = pageRank(graph, s, step, confidence)
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
            pages.append(line)
    return pages

def read_rankings(rankfile):
    rankings = dict()
    with open(rankfile, 'r') as f:
        for line in f:
            line = line.rstrip()

            tokens = line.split()
            page = tokens[0]
            rank = float(tokens[1])
            rankings[page] = rank
    return rankings

def write_rankings(rankings, rankfile):
    with open(rankfile, 'w') as f:
        for page in rankings.keys():
            f.write(str(page) + " " + str(rankings[page]) + "\n")


if __name__ == "__main__":
    from graph import read_graph
    graph = read_graph('final_graph.dataset')
    prTime, prRank = pageRank(graph)
    trusted_pages = read_trusted_pages('trusted_pages')
    trTime, trRank = trustRank(graph, trusted_pages)
    finalRank = spamMass(graph, trusted_pages, prRank = prRank, trRank = trRank)
    pr_sorted_list = sorted(prRank.keys(), key = prRank.__getitem__, reverse = True)
    spamMass_sorted_list = sorted(finalRank.keys(), key = finalRank.__getitem__, reverse = True)
    write_rankings(prRank, 'pageRank')
    write_rankings(finalRank, 'spamMass')
    write_rankings(trRank, 'trustRank')
