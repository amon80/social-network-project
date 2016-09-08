from graph import read_graph, write_graph
from index import read_index, write_index
import sys

def clean_graph(graph_input_file, nodes_to_be_removed_file):
    graph = read_graph(graph_input_file)
    with open(nodes_to_be_removed_file, 'r') as f:
        for node_to_remove in f:
            node_to_remove = node_to_remove.rstrip()
            del graph[node_to_remove]
            for node in graph:
                if node_to_remove in graph[node]:
                    graph[node].remove(node_to_remove)
    write_graph(graph, graph_input_file+'_with_nodes_removed')


def clean_graph_and_index(graph_input_file, index_input_file):
    graph = read_graph(graph_input_file)
    (index, inverted_index) = read_index(index_input_file)
    page_to_remove = []
    for page in index.keys():
        if page not in graph.keys():
            page_to_remove.append(page)
    for page in page_to_remove:
        del index[page]

    node_to_remove = []
    for node in graph.keys():
        if node not in index.keys():
            node_to_remove.append(node)

    for node in node_to_remove:
        del graph[node]
        for node1 in graph:
            if node in graph[node1]:
                graph[node1].remove(node)

    write_index(index, index_input_file+'_cleaned')
    write_graph(graph, graph_input_file+'_cleaned')

if __name__ == "__main__":
    clean_graph_and_index(sys.argv[1], sys.argv[2])
