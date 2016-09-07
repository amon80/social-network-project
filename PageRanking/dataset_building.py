from textparser import get_parsed_document
from spider import crawl
from multiprocessing import Pool
from MyException import MyException
from graph import write_graph, read_graph, write_index
import os

def generate_graph(start_link_list, n_link_to_follow = 2000, verbose = True):

    graph = None
    pid = os.getpid()
    i = 1
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

def generate_pages_contents(nodes, graph_name, log = True):
    string_pid = str(os.getpid())
    if log:
        logfile = open('log-' + string_pid, "w")
    index = dict()
    toRemove = []
    current_node = 1
    total_nodes = len(nodes)
    for node in nodes:
        try:
            index[node] = get_parsed_document(node)
        except:
            if log:
                logfile.write(str(current_node) + " is being removed from the graph\n")
                logfile.flush()
                os.fsync(logfile.fileno())
            toRemove.append(node)
        finally:
            if log:
                logfile.write(" Processed node " + str(current_node) + " out of " + str(total_nodes) + "\n")
                logfile.flush()
                os.fsync(logfile.fileno())
            current_node += 1
    # write_index(index, 'index-'+string_pid)
    if log:
        logfile.close()
    with open(graph_name+'_nodes_to_be_removed', 'w') as f:
        for node in toRemove:
            f.write(node+"\n")
    return index

#parallel version, set num_cores to 1 for sequential or use generate_pages_contents
def write_index_from_graph(graph_input_file, index_output_file, num_cores = 7, verbose = True):
    graph = read_graph(graph_input_file)
    nodes = list(graph.keys())
    list_list_nodes = []
    for i in range(num_cores):
       list_list_nodes.append(list())
    num_nodes = len(nodes)
    num_nodes_for_thread = num_nodes // num_cores
    actual_node = 0
    for i in range(num_cores):
        for j in range(num_nodes_for_thread):
            list_list_nodes[i].append(nodes[actual_node])
            actual_node += 1
    actual_list = 0
    while actual_node < num_nodes:
        list_list_nodes[actual_list].append(nodes[actual_node])
        actual_node += 1
        actual_list += 1
        actual_list %= num_cores
    p = Pool(processes=num_cores)
    for i in range(num_cores):
        p.apply_async(generate_pages_contents, (list_list_nodes[i],))
    p.close()
    p.join()
    if verbose:
        print("Threads have finished their job")

def build_graph_from_crawling(start_link_list, verbose = True, num_cores = 7):
    list_links = []
    list_list_links = []
    for i in range(num_cores):
        list_list_links.append(list())
    with open(start_link_list) as f:
        for line in f:
            list_links.append(line.rstrip())
    num_links = len(list_links)
    num_links_for_thread = num_links // num_cores
    actual_link = 0
    for i in range(num_cores):
        for j in range(num_links_for_thread):
            list_list_links[i].append(list_links[actual_link])
    actual_link += 1
    actual_list = 0
    while actual_link < num_links:
        list_list_links[actual_list].append(list_links[actual_link])
        actual_link += 1
        actual_list += 1
        actual_list %= num_cores
    p = Pool(num_cores)
    for i in range(num_cores):
        p.apply_async(generate_graph, (list_list_links[i],))
    p.close()
    p.join()
    if verbose:
        print("Threads have finished their job")
