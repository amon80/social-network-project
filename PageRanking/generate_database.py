from spider import crawl
from textparser import get_parsed_document
import random
import itertools

#This function generates the graph crawled from the web + the random links
def generate_graph(start_link_file, n_link_to_follow = 2000, n_elements = 2000):

    #Generating graph from crawling
    with open(start_link_file, "r") as readfile:
        graph = dict()
        for line in readfile:
            line = line.rstrip()
            graph = crawl(line, n_link_to_follow, graph)

    ngroups = len(graph) // n_elements
    nodes = list(graph.keys())

    #Adding random nodes
    for i in range(ngroups-1):
        for j in range(i+1, ngroups):
            random1 = random.randint(i*n_elements, (i+1)*n_elements)
            random2 = random.randint(j*n_elements, (j+1)*n_elements)
            graph[nodes[random1]].add(nodes[random2])
    return graph

def write_graph(graph, output_file):
    with open(output_file, "w") as f:
        for node in graph:
            for edge in graph[node]:
                f.write(node + " " + edge + "\n")
    
def write_index(index, output_file):
    with open(output_file, "w") as f:
        for page in index:
            f.write(page + " ")
            for query_term in index[page]:
                f.write(query_term + ",") 
            f.write("\n")


def generate_pages_contents(graph):
    index = dict()
    toRemove = []
    for node in graph.keys():
        try:
            index[node] = get_parsed_document(node)
        except AttributeError as e:
            toRemove.append(node)
    for node in toRemove:
        del graph[node]
        for node1 in graph.keys():
            if node in graph[node1]:
                graph[node1].remove(node)
            
    return index

def find_most_frequent_term(index, doc, termsToAvoid = set()):
    most_frequent_score = 0
    most_frequent_term = ""
    for actual_term in index[doc]:
        actual_term_frequency = index[doc][actual_term]
        if actual_term_frequency > most_frequent_score and actual_term not in termsToAvoid:
            most_frequent_score = actual_term_frequency
            most_frequent_term = actual_term
    return (most_frequent_term, most_frequent_score)

def create_spam_farm(graph, index, supporting_pages=100, random_pages_linking_spam=30):
    nodes_without_spam = list(graph.keys())
    num_nodes_without_spam = len(nodes_without_spam)
    graph["target"] = set()
    index["target"] = dict()
    for i in range(supporting_pages):
        spam_page_name = "spam"+str(i)
        graph[spam_page_name] = set()
        graph[spam_page_name].add("target")
        graph["target"].add(spam_page_name)
    for i in range(random_pages_linking_spam):
        r = random.randint(0, num_nodes_without_spam-1)
        graph[nodes_without_spam[r]].add("target")
    most_frequent_terms_with_frequencies = list()
    most_frequent_terms = set()
    for node in nodes_without_spam:
        result = find_most_frequent_term(index, node, most_frequent_terms)
        if result[1] == 0:
            continue
        most_frequent_terms_with_frequencies.append(result)
        most_frequent_terms.add(result[0])
    sorted_most_frequent_terms = sorted(most_frequent_terms_with_frequencies, key = lambda x:x[1], reverse=True)
    actual_size = min(len(sorted_most_frequent_terms), 500)
    for i in range(actual_size):
        if sorted_most_frequent_terms[i][0] not in index["target"]:
            index["target"][sorted_most_frequent_terms[i][0]] = sorted_most_frequent_terms[i][1]

if __name__ == "__main__":
    graph = generate_graph('links.txt', 5, 2)
    index = generate_pages_contents(graph)
    create_spam_farm(graph,index, supporting_pages=10, random_pages_linking_spam=5)
