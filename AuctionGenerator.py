from random import randint, random

################ PARAMETERS
# range of number of slots available to sell for each query
minSlots = 2
maxSlots = 3

#range of evaluation for each query
minValue = 0
maxValue = 10

#range of budgets for each bidder
minBudget = 20
maxBudget = 40

verbose = True


# generates bidders: evaluation for each query and budget
def generateAdvertisers(queries,advertisers, minValue, maxValue, minBudget, maxBudget):
	adv_bids = dict()
	for query in queries:
		adv_bids[query] = dict()
		for advertiser in advertisers:
			adv_bids[query][advertiser] = randint(minValue,maxValue)
			# if bid is 0, should I remove the bidder from that query?

	adv_budgets = dict()
	for advertiser in advertisers:
		adv_budgets[advertiser] = randint(minBudget,maxBudget)
	return adv_bids,adv_budgets

# generates clickthrough rates for each query and for each position
def generateSlots(queries, minSlots, maxSlots):
	slot_ctrs = dict()
	for query in queries:
		slot_ctrs[query] = dict()
		nSlots = randint(minSlots,maxSlots)
		for i in range(1,nSlots+1):
			slot_ctrs[query]["id"+str(i)] = random()
	return slot_ctrs


def generateAuctions(nAuctions,queries,advertisers):
	for a in range(nAuctions):
		sc = generateSlots(queries,minSlots,maxSlots)
		abi, abu = generateAdvertisers(queries,advertisers,minValue,maxValue,minBudget,maxBudget)
		if (verbose):
			print("|||||||||||||||||||||| Auction #"+str(a))
			print("Slots")
			print(sc)
			print("Bids")
			print(abi)
			print("Budgets")
			print(abu)
			print("\n\n\n\n\n")



#PARAMETERS
nAuctions = 10

queries = ["bread","bake","flour"]
advertisers = ["X","Y","Z"]




generateAuctions(nAuctions,queries,advertisers)



	