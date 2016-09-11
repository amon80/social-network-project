from ranking import read_rankings, write_rankings, trustRank
from graph import read_graph
from sys import argv
from time import clock

if __name__ == "__main__":
    graph = read_graph(argv[1])
    trusted_pages = []
    with open(argv[2], 'r') as f:
        for line in f:
            trusted_pages.append(int(line.rstrip()))
    start = clock()
    trTime, trRank = trustRank(graph, trusted_pages, step = 1000, confidence = 0.000000001, verbose = True)
    output_file_name = argv[1]+'_trustrank_'+str(len(trusted_pages))+'_nodes'
    write_rankings(trRank, output_file_name)
    end = clock()
    print("Time: " + str(end-start))
