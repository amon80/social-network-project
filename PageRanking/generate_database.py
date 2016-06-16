from spider import crawl
from textparser import get_parsed_document
import random
import itertools

#This function generates the graph crawled from the web + the random links
def generate_database(start_link_file, database_file_name, n_link_to_follow = 2000, n_elements = 2000):

    #Generating graph from crawling
    with open(start_link_file, "r") as readfile:
        graph = dict()
        for line in readfile:
            line = line.rstrip()
            graph = crawl(line, n_link_to_follow, graph)

    ngroups = len(graph) // n_elements
    nodes = graph.keys()

    #Adding random nodes
    for i in range(ngroups-1):
        for j in range(i+1, ngroups):
            random1 = random.randint(i*n_elements, (i+1)*n_elements)
            random2 = random.randint(j*n_elements, (j+1)*n_elements)
            graph[nodes[random1]].add(nodes[random2])
            
    with open(database_file_name, "w") as writefile:
        for node in graph:
            for edge in graph[node]:
                writefile.write(node + " " + edge + "\n")
                # print(node + " " + edge)
    return graph


def generate_pages_contents(graph):
    documents = dict()
    toRemove = []
    for node in graph.keys():
        try:
            documents[node] = get_parsed_document(node)
        except AttributeError as e:
            toRemove.append(node)
    for node in toRemove:
        del graph[node]
    return documents

if __name__ == "__main__":
    graph = generate_database('links.txt', 'bogs_database.txt', 10, 10)
    print (generate_pages_contents(graph))
