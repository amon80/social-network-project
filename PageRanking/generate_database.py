import random
import itertools
import os
from multiprocessing import Pool
from spider import crawl
from textparser import get_parsed_document
from MyException import MyException


def generate_graph(start_link_list, n_link_to_follow = 2000, verbose = True):

    graph = None

    pid = os.getpid()

    i = 0
    num_links = len(start_link_list)

    if verbose:
        print(str(pid) + " --- must crawl " + str(num_links) + " links.")
    for link in start_link_list:
        link = link.rstrip()
        graph = crawl(link, n_link_to_follow, graph, pid)
        i += 1
        if verbose:
            print(str(pid) + " --- Crawled " + str(i) + " links out of " + str(num_links))

    write_graph(graph, 'graph_generated_by_'+str(pid))

    return graph

def add_random_nodes_to_total_graph(graph, n_elements = 50):
    ngroups = len(graph) // n_elements
    nodes = list(graph.keys())
    for i in range(ngroups-1):
        for j in range(i+1, ngroups):
            random1 = random.randint(i*n_elements, (i+1)*n_elements)
            random2 = random.randint(j*n_elements, (j+1)*n_elements)
            graph[nodes[random1]].add(nodes[random2])

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
            graph[node1].append(node1)

    return graph

def write_index(index, output_file):
    with open(output_file, "w") as f:
        for page in index:
            f.write(page + " ")
            for query_term in index[page]:
                f.write(query_term + ",")
            f.write("\n")

def generate_pages_contents(graph, verbose = True):
    index = dict()
    toRemove = []
    current_node = 0
    total_nodes = len(graph.keys())
    for node in graph.keys():
        try:
            index[node] = get_parsed_document(node)
        except:
            if verbose:
                print(node + " is being removed from the graph")
            toRemove.append(node)
        finally:
            if verbose:
                print("Processed node " + str(current_node) + " out of " + str(total_nodes))
            current_node += 1
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

def write_index_from_graph(graph_input_file, index_output_file):
    graph = read_graph(graph_input_file)
    index = generate_pages_contents(graph)
    write_graph(graph, graph_input_file+'_with_no_unreachable_nodes')
    write_index(index_output_file)

if __name__ == "__main__":
    list_links = []
    list_list_links = []
    num_cores = 7
    for i in range(num_cores):
       list_list_links.append(list())
    with open('links.txt') as f:
        for line in f:
            list_links.append(line.rstrip())
    num_links = len(list_links)
    num_links_for_thread = num_links // num_cores
    actual_link = 0
    for i in range(num_cores):
        for j in range(num_links_for_thread):
            list_list_links[i].append(list_links[actual_link])
            actual_link += 1
    while actual_link < num_links:
        list_list_links[-1].append(list_links[actual_link])
        actual_link += 1
    p = Pool(num_cores)
    graphs = p.map(generate_graph, list_list_links)
    print(graphs)
