from auctions import myBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from string import ascii_lowercase

# bots_types = [Bot1, Bot2,Bot3,Bot4,Bot5,Bot6,Bot7]

#In particular, for each auction format and for each bot adopted by the other advertiser
# you must run the auction for at least 500 different auction settings (slots’ click-through
# ratio, advertisers’ values and budgets) randomly generated.

queries = ["bread","bake","flour"]

################ PARAMETERS
# range of number of slots available to sell for each query
minSlots = 3
maxSlots = 4

#range of evaluation for each query
minValue = 0
maxValue = 10

#range of budgets for each bidder
minBudget = 20
maxBudget = 40

#number of random executions
nAuctions = 1

verbose = False



def printAuctionResult(nAuction,slots, adv_bots, adv_budgets, adv_values,adv_bids,assigned_slots,payments,step):
	print("**************************")
	print("Auction #",nAuction)
	print("\n//// INPUT")
	print("// SLOTS")
	print("ID\tClickthrough Rate")
	for slot in slots.keys():
		print(slot,"\t",slots[slot])
	print("// ADVERTISERS")
	print("Name\tValue\tBudget\tBid\tBot")
	for adv in adv_values.keys():
		if adv == "a":
			c="*"
		else:
			c=""
		print(c,adv,"\t",adv_values[adv],"\t",adv_budgets[adv],"\t","%.2f" % adv_bids[adv],"\t",adv_bots[adv])
	
	print("\n//// OUTPUT")
	print("// ASSIGNED SLOTS")
	print("ID\tAdv\tPayment\tUtility")
	for slot in assigned_slots.keys():
		paid = payments[assigned_slots[slot]]
		util = adv_values[assigned_slots[slot]] - paid
		print(slot,"\t",assigned_slots[slot],"\t","%.2f" % paid,"\t","%.2f" % util)
	print("// CLOSED IN")
	print(step,"steps")
	print("**************************")
	return




def run500Auctions(ourbot, otherbots):
	adv_bots = dict()
	adv_counter = 0

	#instantiate our Bot
	adv_bots[ascii_lowercase[adv_counter]] = ourbot()
	adv_counter += 1

	#instantiate all other bots
	while adv_counter < number_of_bots:
		adv_bots[ascii_lowercase[adv_counter]] = otherbots()
		adv_counter +=1 

	# for key in adv_bots.keys():
	# 	print(key, adv_bots[key])
	for i in range(nAuctions):
		

		slots = generateSlots(queries,minSlots,maxSlots)
		adv_values, adv_budgets = generateAdvertisers(queries,adv_bots.keys(),minValue,maxValue,minBudget,maxBudget)

		step = 0
		history = []
		adv_bids = dict()
		done = False
		max_step = 100

		while not done and step < max_step:
			done = True
			for adv_name in adv_bots.keys():
				adv_bids[adv_name] = adv_bots[adv_name].response(adv_name,adv_values[adv_name],history,slots,0,0)
				if step == 0 or adv_bids[adv_name] != history[step-1]["adv_bids"][adv_name]:
					done = False

			if done:
				break
			assigned_slots, payments = myBalance(slots,adv_bids,adv_budgets,adv_budgets)

			history.append(dict())
			history[step]["adv_bids"] = dict(adv_bids)
			history[step]["adv_slots"] = dict(assigned_slots)
			history[step]["adv_pays"] = dict(payments)

			# print(history[step])
			step += 1
		printAuctionResult(i,slots, adv_bots, adv_budgets, adv_values,adv_bids,assigned_slots,payments,step)
		


# SETTINGS
ourbot = Bot4
otherbots = Bot1
number_of_bots = 8

run500Auctions(ourbot,otherbots)