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

#Works only when the nodes are integers starting from zero
def get_transition_matrix(graph):
    transition_matrix = list()
    for i in range(len(graph)):
        transition_matrix.append(list())
    for i in range(len(graph)):
        for j in range(len(graph)):
            transition_matrix[i].append(0)
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i in graph[j]:
                transition_matrix[i][j] = 1/len(graph[j]) 
    return transition_matrix

def get_indegrees(graph):
    in_degrees = dict()
    for node in graph:
        in_degrees[node] = 0
        for node1 in graph:
            if node in graph[node1]:
                in_degrees[node] += 1
    return in_degrees

#Works only when the nodes are integers starting from zero
def get_inverse_transition_matrix(graph):
    inv_transition_matrix = list()
    in_degrees = get_indegrees(graph)
    for i in range(len(graph)):
        inv_transition_matrix .append(list())
    for i in range(len(graph)):
        for j in range(len(graph)):
            inv_transition_matrix [i].append(0)
    for i in range(len(graph)):
        for j in range(len(graph)):
            if j in graph[i]:
                inv_transition_matrix [i][j] = 1/in_degrees[j]
    return inv_transition_matrix 

if __name__ == "__main__":
    graph = read_integer_graph('toy_graph')
    inv_transition_matrix = get_inverse_transition_matrix(graph)
    print(graph)
    print(inv_transition_matrix)
