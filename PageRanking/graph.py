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

def read_graph(input_file, integer = True, verbose = True):
    graph = dict()
    with open(input_file) as f:
        line_no = 1
        for line in f:
            try:
                nodes = line.split()
                if integer:
                    node1 = int(nodes[0])
                    node2 = int(nodes[1])
                else:
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

def count_edges(graph):
    counted_edges = 0
    for node in graph.keys():
        counted_edges += len(graph[node])
    return counted_edges

def delete_node(graph, node):
    try:
        del graph[node]
        for node1 in graph:
            if node in graph[node1]:
                graph[node1].remove(node)
        return True
    except KeyError:
        return False

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
