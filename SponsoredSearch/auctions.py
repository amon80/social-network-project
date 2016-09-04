from math import exp


utilityDebug = False

def balance(slot_ctrs, bids, starting_budgets, current_budgets, query):
	query_winners = dict()
	query_pay = dict()

	psi = dict()

	#Only consider advertisers that have a bid for this query
	for advertiser in bids[query].keys():
		if current_budgets[advertiser] >= bids[query][advertiser]:
			#the weight assigned to each advertiser is a tradeoff between his bid an the fraction of budget that is still available to him
			psi[advertiser] = bids[query][advertiser] * (1 - exp(-current_budgets[advertiser]/starting_budgets(advertiser)))


	sorted_slots = sorted(slot_ctrs[query].keys(), key = slot_ctrs[query].__getitem__, reverse = True)
	sorted_advertisers = sorted(psi.keys(), key = psi.__getitem__, reverse = True)

	for i in range(min(len(sorted_slots),len(sorted_advertisers))):
		query_winners[sorted_slots[i]] = sorted_advertisers[i]
		query_pay[sorted_advertisers[i]] = bids[query][sorted_advertisers[i]] #Here, we use first price auction, winner pays exactly their bid

	return query_winners, query_pay





def myBalance(slot_ctrs, bids, starting_budgets, current_budgets):
	query_winners = dict()
	query_pay = dict()

	psi = dict()

	#Only consider advertisers that have a bid for this query
	for advertiser in bids.keys():
		if current_budgets[advertiser] >= bids[advertiser]:
			#the weight assigned to each advertiser is a tradeoff between his bid an the fraction of budget that is still available to him
			psi[advertiser] = bids[advertiser] * (1 - exp(-current_budgets[advertiser]/starting_budgets[advertiser]))


	sorted_slots = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)
	sorted_advertisers = sorted(psi.keys(), key = psi.__getitem__, reverse = True)

	for i in range(min(len(sorted_slots),len(sorted_advertisers))):
		query_winners[sorted_slots[i]] = sorted_advertisers[i]
		query_pay[sorted_advertisers[i]] = bids[sorted_advertisers[i]] #Here, we use first price auction, winner pays exactly their bid
	return query_winners, query_pay



def computeWeights(bids,current_budgets,starting_budgets):
	psi = dict()
	for advertiser in bids.keys():
		if current_budgets[advertiser] >= bids[advertiser]:
			#the weight assigned to each advertiser is a tradeoff between his bid an the fraction of budget that is still available to him
			psi[advertiser] = bids[advertiser] * (1 - exp(-current_budgets[advertiser]/starting_budgets[advertiser]))
	return psi



# Budgeted VCG with Balance algorithm (winners are selected according to the Balance algorithm,
# but they pay the harm they make to the live bidders, that is bidders whose current budget is
# at least the current bid)
def budgetedVCGBalance(slot_ctrs, bids, starting_budgets, current_budgets):
	query_winners = dict()
	rev_query_winners = dict()
	query_pay = dict()



	psi = computeWeights(bids,current_budgets,starting_budgets)

	# print(bids)
	# print(slot_ctrs)
	sorted_slots = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)
	# print(sorted_slots)
	sorted_advertisers = sorted(psi.keys(), key = psi.__getitem__, reverse = True)

	# print()

	nWinners = min(len(sorted_slots),len(sorted_advertisers))

	for i in range(nWinners):
		query_winners[sorted_slots[i]] = sorted_advertisers[i]
		rev_query_winners[sorted_advertisers[i]] = sorted_slots[i]

	# print("The winners are:"+str(rev_query_winners))



	# actual_utilities = 0
	# for winner in query_winners.values():
	# 	actual_utilities += (adv_values[winner] - bids[winner])

	for winner in query_winners.values():
		utility_with_me = 0
		# How much did the other winners win when I am competing???
		if utilityDebug:
			print ("Utility with",winner)
		for other_winner in rev_query_winners.keys():
			if other_winner != winner:
				if utilityDebug:
					print(bids[other_winner],"*",slot_ctrs[rev_query_winners[other_winner]],end=" + ")
				utility_with_me += bids[other_winner]*slot_ctrs[rev_query_winners[other_winner]]
		if utilityDebug:
			print("=",utility_with_me)

		alternative_bids = dict(bids)
		alternative_starting_budgets = dict(starting_budgets)
		alternative_current_budgets = dict(current_budgets)
		del alternative_bids[winner]
		del alternative_current_budgets[winner]
		del alternative_starting_budgets[winner]
		alternative_psi = computeWeights(alternative_bids,alternative_current_budgets,alternative_starting_budgets)

		sorted_alt_advertisers = sorted(alternative_psi.keys(), key = alternative_psi.__getitem__, reverse = True)



		query_alt_winners = dict()
		rev_query_alt_winners = dict()


		for i in range(nWinners-1):
			query_alt_winners[sorted_slots[i]] = sorted_alt_advertisers[i]
			rev_query_alt_winners[sorted_alt_advertisers[i]] = sorted_slots[i]



		if utilityDebug:
			print ("Utility without",winner)
		utility_without_me = 0
		for alt_winner in rev_query_alt_winners.keys():
			if utilityDebug:
				print(bids[alt_winner],"*",slot_ctrs[rev_query_alt_winners[alt_winner]],end=" + ")
			utility_without_me += bids[alt_winner]*slot_ctrs[rev_query_alt_winners[alt_winner]]
		harm = utility_without_me - utility_with_me
		if utilityDebug:
			print("=",utility_without_me)
			print(">>Without",winner,"the winners are",query_alt_winners.values())
			print("And the harm is ",harm)


		query_pay[winner] = harm


	# query_pay[sorted_advertisers[i]] = bids[sorted_advertisers[i]]

	return query_winners, query_pay
