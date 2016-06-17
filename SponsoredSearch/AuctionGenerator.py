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

verbose = False


# generates bidders: evaluation for each query and budget
def generateAdvertisers(queries,advertisers, minValue, maxValue, minBudget, maxBudget):	
	adv_evaluations = dict()
	for advertiser in advertisers:
		adv_evaluations[advertiser] = randint(minValue,maxValue)
			# if bid is 0, should I remove the bidder from that query?

	adv_budgets = dict()
	for advertiser in advertisers:
		adv_budgets[advertiser] = randint(minBudget,maxBudget)
	return adv_evaluations,adv_budgets

# generates clickthrough rates for each query and for each position
def generateSlots(queries, minSlots, maxSlots):
	slot_ctrs = dict()
	nSlots = randint(minSlots,maxSlots)
	for i in range(1,nSlots+1):
		slot_ctrs["id"+str(i)] = random()
	return slot_ctrs


def generateAuction(queries,advertisers):
	sc = generateSlots(queries,minSlots,maxSlots)
	aev, abu = generateAdvertisers(queries,advertisers,minValue,maxValue,minBudget,maxBudget)
	if (verbose):
		print("Auction")
		print("Slots")
		print(sc)
		print("Evaluations")
		print(aev)
		print("Budgets")
		print(abu)
		print("\n\n")
	return sc, aev, abu;











	