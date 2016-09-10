def read_index(databasefile, verbose = False):
    inverted_index = dict()
    index = dict()

    with open(databasefile) as infile:
        line_no = 1
        
        for line in infile:
            line = line.rstrip()
            name_list = line.split(' ',1)
            name = int(name_list[0])
            if name not in index.keys():
                index[name] = dict()
            try:
                queries = name_list[1].split(',')
                for i in range(len(queries)):
                    query_words = queries[i].split(',')
                    
                    for word in query_words:
                        if len(word) == 0:
                            continue
                        if word not in index[name]:
                            index[name][word] = 0
                        if word not in inverted_index.keys():
                            inverted_index[word]=dict() 
                        if name not in inverted_index[word].keys():
                            inverted_index[word][name] = 0 
                        
                        index[name][word] += 1
                        inverted_index[word][name] += 1
            except IndexError:
                if verbose:
                    print("No spaces or no query on " + str(line_no))
            finally:
                line_no += 1
    return (index, inverted_index)

def write_index(index, output_file):
    with open(output_file, "w") as f:
        for page in index:
            f.write(str(page) + " ")
            for query_term in index[page]:
                num_times = index[page][query_term]
                for i in range(num_times):
                    f.write(str(query_term) + ",")
            f.write("\n")

def normalize_index(index, normalization_map):
    normalized_index = dict()
    for page in index:
        normalized_index[normalization_map[page]] = index[page]
    return normalized_index

