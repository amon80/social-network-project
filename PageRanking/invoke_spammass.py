from ranking import read_rankings, write_rankings, spamMass
from graph import read_graph
from sys import argv
from time import clock

if __name__ == "__main__":
    graph = read_graph(argv[1])
    pagerank = read_rankings(argv[2])
    trustRank = read_rankings(argv[3])
    spamMass_ranks = spamMass(graph, prRank = pagerank, trRank = trustRank)
    write_rankings(spamMass_ranks, argv[1]+'_spamMass')

