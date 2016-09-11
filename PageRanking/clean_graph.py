from graph import read_graph, write_graph, delete_node
from index import read_index, write_index
import sys

#Use just this function
#Maybe must be called more than once
def clean_graph_and_index(graph_input_file, index_input_file):
    graph = read_graph(graph_input_file)
    index = read_index(index_input_file, integer = False, also_inverted = False)
    page_to_remove = []
    
    #check for pages present in index but not in graph, if there are, remove those pages from the index
    for page in index:
        if page not in graph:
            page_to_remove.append(page)
    for page in page_to_remove:
        del index[page]

    #check for pages present in graph but not in index, if there are, remove those pages from the graph
    node_to_remove = []
    for node in graph:
        if node not in index:
            node_to_remove.append(node)

    for node in node_to_remove:
        delete_node(graph, node)

    write_index(index, index_input_file+'_cleaned')
    write_graph(graph, graph_input_file+'_cleaned')

if __name__ == "__main__":
    clean_graph_and_index(sys.argv[1], sys.argv[2])
