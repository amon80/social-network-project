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

def read_graph(input_file):
    graph = dict()
    with open(input_file) as f:
        for line in f:
            nodes = line.split()
            node1 = nodes[0]
            node2 = nodes[1]
            if node1 not in graph:
                graph[node1] = set()
            if node2 not in graph:
                graph[node2] = set()
            graph[node1].add(node2)
    return graph

def write_index(index, output_file):
    with open(output_file, "w") as f:
        for page in index:
            f.write(page + " ")
            for query_term in index[page]:
                num_times = index[page][query_term]
                for i in range(num_times):
                    f.write(query_term + ",")
            f.write("\n")


def normalize_graph(input_file):
    graph = read_graph(input_file)
    graph_normalized = dict()
    index_node_mapping = dict()
    index = 1
    for node in graph.keys():
        index_node_mapping[node] = index
        graph_normalized[index] = set()
        index += 1
    for node in graph.keys():
        source_index = index_node_mapping[node]
        for edge in graph[node]:
            target_index = index_node_mapping[edge]
            graph_normalized[source_index].add(target_index)

    write_graph_as_csv(graph_normalized, input_file+'_normalized')


if __name__ == "__main__":
    normalize_graph(sys.argv[1])
