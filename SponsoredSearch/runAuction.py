from auctions import myBalance, budgetedVCGBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from Reporter import *
from string import ascii_lowercase
from random import randint
from math import ceil
import time

################ PARAMETERS
#Number of bots
number_of_bots = 7
all_bots_list = [Bot1,Bot2,Bot3,Bot4,Bot5,Bot6,Bot7]

# range of number of slots available to sell for each query
minSlots = 3
maxSlots = 3

#range of evaluation for each query
minValue = 0
maxValue = 10

#range of budgets for each bidder
minBudget = 100
maxBudget = 200

#number of random executions
nAuctions = 100
max_step = 100

isVCG = True

verbose = False
recap = False
mulrecap = True
tryAll = False

botname = "a"

no = 0

# def generateBots(ourbot, otherbots):
def generateBots(bots_list):
	number_of_bots = len(bots_list)
	adv_bots = dict()

	for adv_counter in range(len(bots_list)):
		adv_bots[ascii_lowercase[adv_counter]] = bots_list[adv_counter]()
	return adv_bots


# def runAuctions(ourbot, otherbots,no=0):
def runAuctions(bots_list,no=0):
	if recap:
		print("*"+str(ourbot)+"* VS "+str(otherbots))
	adv_bots = generateBots(bots_list)
	# adv_bots = generateBots(ourbot,otherbots)

	if mulrecap:
		our_expenses = 0
		our_utility = 0
		auction_revenue = 0
		auction_utility = 0

	for auctionIndex in range(nAuctions):
		slots = generateSlots(minSlots,maxSlots)
		adv_values, adv_sbudgets = generateAdvertisers(adv_bots.keys(),minValue,
		maxValue,minBudget,maxBudget)

		step = 0
		history = []
		adv_bids = dict()
		adv_utilities = dict()
		adv_budgets = dict(adv_sbudgets)
		done = False

		while not done and step < max_step:
			# done = True
			for adv_name in adv_bots.keys():
				adv_bids[adv_name] = adv_bots[adv_name].response(adv_name,
				adv_values[adv_name],history,slots,adv_budgets[adv_name],
				adv_sbudgets[adv_name])

			if isVCG:
				assigned_slots, payments = budgetedVCGBalance(slots,adv_bids, adv_sbudgets,adv_budgets)
			else:
				assigned_slots, payments = myBalance(slots,adv_bids,adv_sbudgets,adv_budgets)


			# print(assigned_slots)
			adv_utilities = dict()

			for adv in adv_values:
				if adv in payments and payments[adv] > 0:
					adv_utilities[adv] = adv_values[adv] - payments[adv]
					adv_budgets[adv] = adv_budgets[adv] - payments[adv]
				else:
					adv_utilities[adv] = 0
			history.append(dict())

			history[step]["adv_bids"] = dict(adv_bids)
			history[step]["adv_slots"] = dict(assigned_slots)
			history[step]["adv_pays"] = dict(payments)
			history[step]["adv_utilities"] = dict(adv_utilities)
			history[step]["adv_budgets"] = dict(adv_budgets)
			if verbose:
				printTableRow(step,adv_budgets,adv_bids,assigned_slots,payments,adv_utilities,adv_values,adv_bots)

			if mulrecap:
				our_utility += adv_utilities[botname]
				if botname in payments:
					our_expenses += payments[botname]
				for payment in payments:
					auction_revenue += payments[payment]
				for au in adv_utilities:
					auction_utility += adv_utilities[au]
			step += 1
		if recap:
			printSingleAuctionRecap(history,adv_values,adv_bots,adv_sbudgets)


	if mulrecap:
		printMultipleAuctionsRecap(our_utility,our_expenses,auction_revenue,auction_utility,bots_list[0],bots_list[1:len(bots_list)-1],no)


def generateBotList(us,them,howmany):
	bl = []
	bl.append(us)
	for hm in range(howmany):
		bl.append(them)
	print(bl)
	return bl


def runAllBotsAtOnce():
	number_of_bots = 7
	runAuctions([Bot1,Bot2,Bot3,Bot4,Bot5,Bot6,Bot7])


def runAllBotsCombinations():
	no = randint(1,1000)
	if mulrecap:
		print("Executing auction",no)
		printAuctionSettings(no,number_of_bots,minSlots,maxSlots,minValue,maxValue,minBudget,maxBudget,nAuctions,max_step,isVCG)
	bots_types = [Bot1, Bot2,Bot3,Bot4,Bot5,Bot6,Bot7]
	for otherbots in bots_types:
		for ourbot in bots_types:
			runAuctions(ourbot,otherbots,no)


def runSingleBotCombination():
	ourbot = Bot1
	otherbots = Bot1
	num_of_bots = 7
	runAuctions(generateBotList(ourbot,otherbots,num_of_bots))


runSingleBotCombination()
