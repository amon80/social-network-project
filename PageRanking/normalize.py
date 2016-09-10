def normalize_index(index, normalization_map):
    normalized_index = dict()
    for page in index:
        normalized_index[normalization_map[page]] = index[page]
    return normalized_index

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

def convert_pages_from_integers_to_url(list_pages_as_indeces, pages_mapping):
    converted_pages = list()
    for page in list_pages_as_indeces:
        converted_pages.append(pages_mapping[page])
    return converted_pages
