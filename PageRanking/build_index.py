from generate_database import generate_pages_contents, write_index
from graph import read_graph
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    graph = read_graph(input_file)
    nodes = list(graph.keys())
    index = generate_pages_contents(nodes, sys.argv[1])
    write_index(index, sys.argv[1]+'_index')
    #write_index_from_graph('toy_graph', 'toy_index', num_cores = 4)
