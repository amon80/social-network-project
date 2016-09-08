import sys

def write_graph(graph, output_file):
    with open(output_file, "w") as f:
        for node in graph:
            for edge in graph[node]:
                f.write(str(node) + " " + str(edge) + "\n")

def write_graph_as_csv(graph, output_file):
    with open(output_file, "w") as f:
        for node in graph:
            for edge in graph[node]:
                f.write(str(node) + "," + str(edge) + "\n")

def read_graph(input_file, verbose = True):
    graph = dict()
    with open(input_file) as f:
        line_no = 1
        for line in f:
            try:
                nodes = line.split()
                node1 = nodes[0]
                node2 = nodes[1]
                if node1 not in graph:
                    graph[node1] = set()
                if node2 not in graph:
                    graph[node2] = set()
                graph[node1].add(node2)
            except IndexError as e:
                if verbose:
                    print("Empty line found on line " + str(line_no) + "\n")
            finally:
                line_no += 1
    return graph

def read_integer_graph(input_file, verbose = True):
    graph = dict()
    with open(input_file) as f:
        line_no = 1
        for line in f:
            try:
                nodes = line.split()
                node1 = int(nodes[0])
                node2 = int(nodes[1])
                if node1 not in graph:
                    graph[node1] = set()
                if node2 not in graph:
                    graph[node2] = set()
                graph[node1].add(node2)
            except IndexError as e:
                if verbose:
                    print("Empty line found on line " + str(line_no) + "\n")
            finally:
                line_no += 1
    return graph

def normalize_graph(graph, print_mapping = True):
    graph_normalized = dict()
    index_node_mapping = dict()
    index = 0
    for node in graph.keys():
        index_node_mapping[node] = index
        graph_normalized[index] = set()
        index += 1
    for node in graph.keys():
        source_index = index_node_mapping[node]
        for edge in graph[node]:
            target_index = index_node_mapping[edge]
            graph_normalized[source_index].add(target_index)

    if print_mapping:
        with open('normalized_mapping', 'w') as f:
            for node in index_node_mapping:
                index = index_node_mapping[node]
                f.write(str(index)+" "+node+"\n")
    return graph_normalized

def read_normalization_map(graph_normalized_mapping_file):
    normalization_map = dict()
    inverse_normalization_map = dict()
    with open(graph_normalized_mapping_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            tokens = line.split()

            index = int(tokens[0])
            page = tokens[1]

            normalization_map[page] = index
            inverse_normalization_map[index] = page
    return (normalization_map, inverse_normalization_map)
    
def count_edges(graph):
    counted_edges = 0
    for node in graph.keys():
        counted_edges += len(graph[node])
    return counted_edges

def convert_graph(graph):
    return False
    # adj_
    # converted_graph = []

if __name__ == "__main__":
    normalize_graph(sys.argv[1], print_mapping = True)
