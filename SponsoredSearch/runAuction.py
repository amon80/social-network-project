from auctions import myBalance, budgetedVCGBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from string import ascii_lowercase
from math import ceil
import time

################ PARAMETERS
#Number of bots
number_of_bots = 8

# range of number of slots available to sell for each query
minSlots = 2
maxSlots = 4

#range of evaluation for each query
minValue = 0
maxValue = 10

#range of budgets for each bidder
minBudget = 200
maxBudget = 700

#number of random executions
nAuctions = 1
max_step = 10
	
verbose = False


def printTableRow(step,budgets,bids,slots,payments,utilities,evaluation):
	print("________________________________________________________________________")
	print("#",step,end="\t")
	for adv in budgets.keys():
		print(adv,end="\t")
	print("\n________________________________________________________________________")
	print("budget",end="\t")
	for adv in budgets.keys():
		print("%.1f" % budgets[adv],end="\t")
	print("\nevals",end="\t")
	for adv in budgets.keys():
		print("%.1f" % evaluation[adv],end="\t")
	print("\nbids",end="\t")
	for adv in budgets.keys():
		print("%.1f" % bids[adv],end="\t")
	print("\npaid",end="\t")
	for adv in budgets.keys():
		if adv in payments.keys():
			print("%.1f" % payments[adv],end="\t")
		else:
			print(end="\t")
	print("\nutils",end="\t")
	for adv in budgets.keys():
		print("%.1f" % utilities[adv],end="\t")
	print(end="\n")
	return


def generateBots(ourbot, otherbots):
	adv_bots = dict()
	adv_counter = 0

	#instantiate our Bot
	adv_bots[ascii_lowercase[adv_counter]] = ourbot()
	adv_counter += 1
	
	#instantiate all other bots
	while adv_counter < number_of_bots:
		adv_bots[ascii_lowercase[adv_counter]] = otherbots()
		adv_counter +=1 
	return adv_bots


def runAuctions(ourbot, otherbots):
	adv_bots = generateBots(ourbot,otherbots)
	
	for auctionIndex in range(nAuctions):
		slots = generateSlots(minSlots,maxSlots)
		adv_values, adv_sbudgets = generateAdvertisers(adv_bots.keys(),minValue,maxValue,minBudget,maxBudget)

		step = 0
		history = []
		adv_bids = dict()
		adv_utilities = dict()
		adv_budgets = dict(adv_sbudgets)
		done = False

		while not done and step < max_step:
			# done = True
			for adv_name in adv_bots.keys():
				adv_bids[adv_name] = adv_bots[adv_name].response(adv_name,adv_values[adv_name],history,slots,adv_budgets[adv_name],adv_sbudgets[adv_name])

			assigned_slots, payments = budgetedVCGBalance(slots,adv_bids,adv_sbudgets,adv_budgets)
			# assigned_slots, payments = myBalance(slots,adv_bids,adv_sbudgets,adv_budgets)


			adv_utilities = dict()

			for adv in adv_values:
				if adv in payments and payments[adv] > 0:
					adv_utilities[adv] = adv_values[adv]- payments[adv]
					adv_budgets[adv] = adv_budgets[adv] - payments[adv]
				else:
					adv_utilities[adv] = 0

			history.append(dict())
			history[step]["adv_bids"] = dict(adv_bids)
			history[step]["adv_slots"] = dict(assigned_slots)
			history[step]["adv_pays"] = dict(payments)
			history[step]["adv_utilities"] = dict(adv_utilities)
			history[step]["adv_budgets"] = dict(adv_budgets)
			#printTableRow(step,adv_budgets,adv_bids,assigned_slots,payments,adv_utilities,adv_values)
			step += 1



def runAllBotsCombinations():
	bots_types = [Bot1, Bot2,Bot3,Bot4,Bot5,Bot6,Bot7]
	for ourbot in bots_types:
		for otherbots in bots_types:
			print("#")
			runAuctions(ourbot,otherbots)
	

def runSingleBotCombination():
	ourbot = Bot1
	otherbots = Bot1
	runAuctions(ourbot,otherbots)

runSingleBotCombination()
























