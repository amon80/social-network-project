from random import randint, random
import constants

################ PARAMETERS
# # range of number of slots available to sell for each query
# minSlots = 8
# maxSlots = 8
#
# #range of evaluation for each query
# minValue = 6
# maxValue = 10
#
# #range of budgets for each bidder
# minBudget = 20
# maxBudget = 40

verbose = False

overrideMyBudget = False
overrideMyEvaluation = False
overridedBudget = 200
overridedEvaluation = 3

# generates bidders: evaluation for each query and budget
def generateAdvertisers(advertisers, minValue, maxValue, minBudget, maxBudget):
	adv_evaluations = dict()
	for advertiser in advertisers:
		adv_evaluations[advertiser] = randint(minValue,maxValue)
	if overrideMyEvaluation:
		adv_evaluations[constants.OUR_BOT_NAME] = overridedEvaluation

	adv_budgets = dict()
	for advertiser in advertisers:
		adv_budgets[advertiser] = randint(minBudget,maxBudget)
	if overrideMyBudget:
		adv_budgets[constants.OUR_BOT_NAME] = overridedBudget

	return adv_evaluations,adv_budgets

# generates clickthrough rates for each query and for each position
def generateSlots( minSlots, maxSlots):
	slot_ctrs = dict()
	nSlots = randint(minSlots,maxSlots)
	slot_tmp = []
	for i in range(1,nSlots+1):
		slot_tmp.append(random())
	slot_tmp.sort(reverse=True)

	for i in range(1,nSlots+1):
		slot_ctrs["id"+str(i)] = slot_tmp[i-1]
	return slot_ctrs


def generateAuction(advertisers):
	sc = generateSlots(minSlots,maxSlots)
	aev, abu = generateAdvertisers(advertisers,minValue,maxValue,minBudget,maxBudget)
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
