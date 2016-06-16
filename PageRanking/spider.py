import sys
import re
import urllib.request
import urllib.error
import lxml.html

def crawl(url, number_of_links_to_follow, graph = None, verbose= False, graphVerbose = False, errorVerbose = False):

    actual_layer = set()
    next_layer = set()
    crawledLinks = set()

    if not graph:
        graph = dict()
        if graphVerbose:
            print("Created graph")
    else:
        if graphVerbose:
            print("Loaded graph")
        for node in graph.keys():
            for link in graph[node]:
                crawledLinks.add(link)

    actual_layer.add(url)
    linkPattern = re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+))?$")
    i = 0
    layer = 0
    while i < number_of_links_to_follow:
        if len(actual_layer) == 0:
            break
        for actual_url in actual_layer:
            if verbose:
                print("Examining: " + actual_url)
            try:
                url_html = urllib.request.urlopen(actual_url)
                if actual_url not in graph:
                    graph[actual_url] = set()
                    if graphVerbose:
                        print("Added node: " + actual_url)
                # Pattern to check proper link
                dom = lxml.html.fromstring(lxml.html.tostring(lxml.html.parse(url_html)))
                for link in dom.xpath("//a/@href"):
                    if verbose:
                        print("Link founded: " + link)
                    if linkPattern.match(link): 
                        try:
                            urllib.request.urlopen(link)
                            if link not in graph:
                                if graphVerbose:
                                    print("Adding node: " + link)
                                graph[link] = set()
                            graph[actual_url].add(link)
                            if graphVerbose:
                                print("Adding edge from " + actual_url + " to " + link)
                            if(link not in crawledLinks):
                                if verbose:
                                    print("Adding " + link + " ")
                                crawledLinks.add(link) 
                                next_layer.add(link)
                                i += 1
                            else:
                                if verbose:
                                    print("Refusing " + link + " because it was already added")
                        except urllib.error.HTTPError as e:
                            if errorVerbose:
                                print(str(link) + " caused " +  str(e) + " so it wasn't added")
                        except urllib.error.URLError as e:
                            if errorVerbose:
                                print(str(link) + " caused " + str(e) + " so it wasn't added")
                    else:
                        if verbose:
                            print("Refusing " + link + "because did not match regexp")
            except urllib.error.HTTPError as e:
                if errorVerbose:
                    print("Start link " + str(actual_url) + " caused " +  str(e) + " so it wasn't added")
            except urllib.error.URLError as e:
                if errorVerbose:
                    print("Start link " + str(actual_url) + " caused " +  str(e) + " so it wasn't added")
        if verbose:
            print("-----------------------------")
            print("Finished layer " + str(layer))
            print("-----------------------------")
        layer += 1
        actual_layer = next_layer
        next_layer = set()
    return graph

if __name__ == "__main__":
    graph = crawl(sys.argv[1], int(sys.argv[2]))
    print(graph)

