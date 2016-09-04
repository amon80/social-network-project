import sys
import re
import urllib.request
import urllib.error
import lxml.html
import ssl
import http.client

def crawl(url, number_of_links_to_follow, graph = None, pid = 0, verbose = True, graphVerbose = True, errorVerbose = True, numLinkVerbose = True):

    #convenience variables
    actual_layer = set()
    next_layer = set()
    crawledLinks = set()

    #creating graph if not existing already
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

    #Add first link to layer 0
    actual_layer.add(url)

    #Compiling regular expression and settings sites to avoid
    #Regular expression does not allow relative urls
    linkPattern = re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&%@!\-\/\(\)]+))?$")
    sites_to_avoid = ["messenger","facebook", "twitter", "instagram", "youtube", "plus.google", "google", "t.co", "itunes.apple.com"]

    #Setting other convenience variables before starting to crawl
    examined_links = 0
    layer = 0
    breaked = False
    while examined_links < number_of_links_to_follow:
        #If there is no link in this layer
        if len(actual_layer) == 0:
            break
        #if we have reached the maxinum num of link while exploring a layer
        #(added for apparentely no reason but without these two lines nothing
        #works)
        if breaked:
            break

        #For every url in the actual_layer
        for actual_url in actual_layer:
            if verbose:
                print("Examining: " + actual_url)
            if breaked:
                break
            try:
                #See if it's reachable
                with urllib.request.urlopen(actual_url) as connection:
                    html = connection.read()
                #Adding actual_url as a node if is not present
                if actual_url not in graph:
                    graph[actual_url] = set()
                    if graphVerbose:
                        print("Added node: " + actual_url)
                #Take the dom, so links can be found with a proper xpath
                dom = lxml.html.fromstring(html)

                #for each link contained in actual_url, check if it points to
                #itself or a forbidden site
                break_for_forbidden_site = False
                #grep all the links that it contains
                for link in dom.xpath("//a/@href"):
                    if verbose:
                        print("Link founded: " + link)
                    if linkPattern.match(link):
                        if actual_url in link:
                            if verbose:
                                print("Found local loop")
                            continue
                        for site in sites_to_avoid:
                            if site in link:
                                break_for_forbidden_site = True
                                if errorVerbose:
                                    print("Avoiding " + site + " on link " + link)
                                break
                        if break_for_forbidden_site:
                            break_for_forbidden_site = False
                            continue

                        #Now that we have verified that this link is good, see
                        #if it's reachable, if so we add it to the graph
                        #(both node and edge)
                        try:

                            with urllib.request.urlopen(link) as connection_to_outer_link:
                                html_outer = connection_to_outer_link.read()
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
                                examined_links += 1
                                if numLinkVerbose:
                                    print(str(pid) + " --- Link followed until now " + str(examined_links))
                                if examined_links >= number_of_links_to_follow:
                                    if numLinkVerbose:
                                        print(str(pid) + " --- Reached " + str(number_of_links_to_follow))
                                    breaked = True
                                    break
                            else:
                                if verbose:
                                    print("Refusing " + link + " because it was already added")
                        except urllib.error.HTTPError as e:
                            if errorVerbose:
                                print(str(link) + " caused " +  str(e) + " so it wasn't added")
                        except urllib.error.URLError as e:
                            if errorVerbose:
                                print(str(link) + " caused " + str(e) + " so it wasn't added")
                        except ssl.CertificateError as e:
                            if errorVerbose:
                                print(str(link) + " caused " + str(e) + " so it wasn't added")
                        except lxml.etree.SerialisationError as e:
                            if errorVerbose:
                                print(str(actual_url) + " caused SerialisationError, so it wasn't added");
                        except http.client.RemoteDisconnected as e:
                            if errorVerbose:
                                print(str(actual_url) + " caused http.client.RemoteDisconnected error, so it wasn't added")
                        except:
                            if errorVerbose:
                                print(str(actual_url) + " caused unknown error, so it wasn't added")
                    else:
                        if verbose:
                            print("Refusing " + link + " because did not match regexp")
            except urllib.error.HTTPError as e:
                if errorVerbose:
                    print("Start link " + str(actual_url) + " caused " +  str(e) + " so it wasn't added")
            except urllib.error.URLError as e:
                if errorVerbose:
                    print("Start link " + str(actual_url) + " caused " +  str(e) + " so it wasn't added")
            except ssl.CertificateError as e:
                if errorVerbose:
                    print(str(actual_url) + " caused " + str(e) + " so it wasn't added")
            except lxml.etree.SerialisationError as e:
                if errorVerbose:
                    print(str(actual_url) + " caused SerialisationError, so it wasn't added");
            except http.client.RemoteDisconnected as e:
                if errorVerbose:
                    print(str(actual_url) + " caused http.client.RemoteDisconnected error, so it wasn't added")
            except:
                if errorVerbose:
                    print(str(actual_url) + " caused unknown error, so it wasn't added")
        if not breaked:
            if verbose:
                print("-----------------------------")
                print("Finished layer " + str(layer))
                print("-----------------------------")
            layer += 1
            actual_layer = next_layer
            next_layer = set()
        else:
            if verbose:
                print("-----------------------------")
                print("Ended due to number_of_links_to_follow reached")
                print("-----------------------------")
            break
    return graph

if __name__ == "__main__":
    graph = crawl(sys.argv[1], int(sys.argv[2]))
    print(graph)
