from ranking import read_rankings, write_rankings, pageRank
from graph import read_graph
from sys import argv
from time import clock

if __name__ == "__main__":
    graph = read_graph(argv[1])
    s = float(argv[2])
    step = int(argv[3])
    confidence = float(argv[4])
    start = clock()
    prTime, prRank = pageRank(graph, step = step, confidence = confidence, s = s, verbose = True)
    output_file_name = argv[1]+'_pagerank_s_'+str(s)+'_step_'+str(step)+'_confidence_'+str(confidence)
    write_rankings(prRank, output_file_name)
    end = clock()
    print("Time: " + str(end-start))
