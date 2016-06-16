
# As seen during the course
def pageRank(graph, s, step, confidence):
	nodes = graph.keys()
	n = len(nodes)
	done = 0
	time = 0

	# Initialization
	rank = dict()
	for node in nodes:
		rank[node] = float(1)/2


	tmp = dict()
	while not done and time < step:
		time += 1

		for node in nodes:
			# Each node receives a share of 1/n with probability 1-s
			tmp[node] = float(1-s)/n 

		for node in nodes:
			for neighbour in graph[node]:
				# Each node receives a fraction of its neighbour rank with probability s
				tmp[neighbour] += float(s*rank[node])/len(graph[node])

		# Computes the distance between the old rank vector and the new rank vector in L_1 norm
		diff = 0
		for node in nodes:
			diff += abs(rank[node] - tmp[node])
			rank[node] = tmp[node]

		if diff <= confidence:
			done = 1
	return time, rank


# TrustRank is topic-sensitive PageRank, where the "topic" is a set of pages
# believed to be trustworthy (not spam). The theory is that while a spam page
# might easly be made to link to a trustworthy page, it is unlikely that a 
# trustworthy page would link to a spam page.
# The borderline area is a site with blogs or other opportunities for spammers
# to create links.
# Two approaches to develop a suitable teleport set of trustworthy pages:
# 1 Let humans examine a set of pages and decide which of them are trustworthy.
# 	For example, we might pick the pages of highest PageRank to examine,
#	on the theory that, while link spam can raise a page's rank from the bottom
#	to the middle of the pack, it is esssentially impossible to give a spam page a
#	PageRank near the top of the list
# 2 Pick a domain whose membership is controlled, on the assumption that it is hard
#	for a spammer to get their pages into these domains (e.g. .edu, .gov, .mil)
def trustRank(graph, trusted_pages):
	return


def trustRankProva(graph, trusted_pages, s, step, confidence):
	nodes = graph.keys()
	n = len(nodes)
	done = 0
	time = 0

	# Initialization
	rank = dict()
	for node in trusted_pages:
		rank[node] = float(1)/2


	tmp = dict()
	while not done and time < step:
		time += 1

		for node in nodes:
			# Each node receives a share of 1/n with probability 1-s
			tmp[node] = float(1-s)/n 

		for node in trusted_pages:
			for neighbour in graph[node]:
				# Each node receives a fraction of its neighbour rank with probability s
				tmp[neighbour] += float(s*rank[node])/len(graph[node])

		# Computes the distance between the old rank vector and the new rank vector in L_1 norm
		diff = 0
		for node in nodes:
			diff += abs(rank[node] - tmp[node])
			rank[node] = tmp[node]

		if diff <= confidence:
			done = 1
	return time, rank

# The idea behind spam mass is that we measure for each page the fraction
# of its PageRank that comes from spam. We do so by computing both the 
# ordinary PageRank and the TrustRank based on some teleport set of trustworthy pages.
# Suppose page p has PageRank r and TrustRank t. Then the spam mass of p is
# (r-t)/r. 
# A negative or small positive spam mass means that p is probably not a spam page,
# while a spam mass close to 1 suggests that the page probably is spam.
def spamMass(graph):
	prTime, prRank = pageRank(graph,0.85,75,0)
	trTime, trRank = trustRank(graph)

	finalRank = dict()
	for node in graph.keys():
		finalRank[node] = ( prRank[node] - trRank[node] ) / trRank[node] 

	return finalRank


























