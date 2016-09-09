from ranking import read_rankings, order_nodes, spamMass, write_rankings
from graph import read_normalization_map
from sys import argv

if __name__ == "__main__":
    prRank = read_rankings(argv[1])
    trRank = read_rankings(argv[2])
    graph = range(len(prRank))

    final_rankings = spamMass(graph, prRank = prRank, trRank = trRank)
    write_rankings(final_rankings, 'spamMass')
