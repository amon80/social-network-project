def write_graph(graph, output_file):
    with open(output_file, "w") as f:
        for node in graph:
            for edge in graph[node]:
                f.write(node + " " + edge + "\n")

def read_graph(input_file):
    graph = dict()
    with open(input_file) as f:
        for line in f:
            nodes = line.split()
            node1 = nodes[0]
            node2 = nodes[1]
            if node1 not in graph:
                graph[node1] = list()
            if node2 not in graph:
                graph[node2] = list()
            graph[node1].append(node2)
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
