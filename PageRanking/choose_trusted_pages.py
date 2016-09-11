from ranking import read_rankings, order_nodes
from normalize import read_normalization_map
from sys import argv

if __name__ == "__main__":
    prRank = read_rankings(argv[1])
    inv_prRank = read_rankings(argv[2])
    num_pages = int(argv[3])
    nodes = range(len(prRank))
    ordered_nodes_inv = order_nodes(nodes, inv_prRank)
    ordered_nodes = order_nodes(nodes, prRank)
    pages_on_which_use_oracle = ordered_nodes_inv[:num_pages] + ordered_nodes[:num_pages]
    norm_map, inv_norm_map = read_normalization_map('mapping')
    print("Inverted Pageranks")
    for page in ordered_nodes_inv[:num_pages]:
        print(inv_norm_map[page] + " - " + str(page))
    print("Pageranks")
    for page in ordered_nodes[:num_pages]:
        print(inv_norm_map[page] + " - " + str(page))
