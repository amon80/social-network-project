from ranking import read_rankings, order_nodes
from normalize import read_normalization_map
from sys import argv

def choose_trusted_pages(PageRanks, inv_PageRanks, num_pages):
    nodes = range(len(PageRanks))
    ordered_nodes_inv = order_nodes(nodes, inv_PageRanks)
    ordered_nodes = order_nodes(nodes, PageRanks)
    trusted_pages = ordered_nodes_inv[:num_pages] + ordered_nodes[:num_pages]
    #Fortunately, target page is the only one on which the oracle says no
    trusted_pages.remove(12639)
    return trusted_pages

def write_trusted_pages(trusted_pages_list, output_file_name):
    with open(output_file_name, 'w') as f:
        for page in trusted_pages_list:
            f.write(str(page)+'\n')

if __name__ == "__main__":
    prRank = read_rankings(argv[1])
    inv_prRank = read_rankings(argv[2])
    num_pages = int(argv[3])
    trusted_pages = choose_trusted_pages(prRank, inv_prRank, num_pages)
    write_trusted_pages(trusted_pages, 'trusted_pages_'+str(num_pages*2))
