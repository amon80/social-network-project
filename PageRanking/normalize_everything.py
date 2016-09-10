from graph import read_graph, write_graph
from normalize import normalize_graph, read_normalization_map, normalize_index
from index import read_index, write_index
from generate_database import create_spam_farm
from sys import argv

if __name__ == "__main__":
    graph = read_graph(argv[1])
    index, inv_index = read_index(argv[2])
    create_spam_farm(graph, index)
    normalized_graph = normalize_graph(graph)
    norm_map, inv_norm_map = read_normalization_map('normalized_mapping')
    normalized_index = normalize_index(index, norm_map)
    write_graph(normalized_graph, argv[1]+'_normalized')
    write_index(normalized_index, argv[2]+'_normalized')
