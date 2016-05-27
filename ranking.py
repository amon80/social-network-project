
# As seen during the course
def pageRank(graph, s, step, confidence):
	nodes = graph.keys()
	n = len(nodes)
	done = 0
	time = 0

	# Initialization
	rank = dict()
	for i in nodes:
		rank[i] = float(1)/2


	tmp = dict()
	while not done and time < step:
		time += 1

		for i in nodes:
			# Each node receives a share of 1/n with probability 1-s
			tmp[i] = float(1-s)/n 

		for i in nodes:
			for j in graph[i]:
				# Each node receives a fraction of its neighbor rank with probability s
				tmp[j] += float(s*rank[i])/len(graph[i])

		# Computes the distance between the old rank vector and the new rank vector in L_1 norm
		diff = 0
		for i in nodes:
			diff += abs(rank[i] - tmp[i])
			rank[i] = tmp[i]

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
def trustRank():
	return


# The idea behind spam mass is that we measure for each page the fraction
# of its PageRank that comes from spam. We do so by computing both the 
# ordinary PageRank and the TrustRank based on some teleport set of trustworthy pages.
# Suppose page p has PageRank r and TrustRank t. Then the spam mass of p is
# (r-t)/r. 
# A negative or small positive spam mass means that p is probably not a spam page,
# while a spam mass close to 1 suggests that the page probably is spam.
def spamMass():
	return


























