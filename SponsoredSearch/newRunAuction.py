from auctions import myBalance, budgetedVCGBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from Reporter import *
from string import ascii_lowercase
from random import randint
from math import ceil
import time


#SETTINGS
#number of executions
nAuctions = 1000
max_step = 100

# range of number of slots available to sell
minSlots = 3
maxSlots = 3

#range of evaluation
minValue = 0
maxValue = 10

#range of budgets for each advertiser
minBudget = 100
maxBudget = 200

#is VCG or FirstPriceAuction
isVCG = True



def generateBots(bots_list):
    bots = dict()

    for b in range(len(bots_list)):
        bots[ascii_lowercase[b]] = bots_list[b]()
    return bots


def runAuction(slots,adv_bids, adv_sbudgets,adv_budgets):
    if isVCG:
        assigned_slots, payments = budgetedVCGBalance(slots,adv_bids, adv_sbudgets,adv_budgets)
    else:
        assigned_slots, payments = myBalance(slots,adv_bids,adv_sbudgets,adv_budgets)
    return assigned_slots, payments


def updateBots(bots,payments,values,budgets):
    utilities = dict()
    for bot in bots:
        if bot in payments and payments[bot] > 0:
            utilities[bot] = values[bot] - payments[bot]
            budgets[bot] = budgets[bot] - payments[bot]
        else:
            utilities[bot] = 0
    return utilities, budgets


def createHistoryStep(adv_bids,assigned_slots,payments,adv_utilities,adv_budgets):
    stepHistory = dict()

    stepHistory["adv_bids"] = dict(adv_bids)
    stepHistory["adv_slots"] = dict(assigned_slots)
    stepHistory["adv_pays"] = dict(payments)
    stepHistory["adv_utilities"] = dict(adv_utilities)
    stepHistory["adv_budgets"] = dict(adv_budgets)
    return stepHistory

def runAuctions(bots_list,):
    bots = generateBots(bots_list)

    for auctionIndex in range(nAuctions):
        #Auction initialization
        slots = generateSlots(minSlots,maxSlots)
        values, starting_budgets = generateAdvertisers(bots.keys(),minValue,
		maxValue,minBudget,maxBudget)

        step = 0
        history = []
        bids = dict()
        utilities = dict()
        budgets = dict(starting_budgets)
        done = False

        while not done and step < max_step:
            for b in bots.keys():

                bids[b] = bots[b].response(b,values[b],history,slots,budgets[b],starting_budgets[b])

            assigned_slots, payments = runAuction(slots,bids,starting_budgets,budgets)

            utilities, budgets = updateBots(bots,payments,values,budgets)

            history.append(createHistoryStep(bids,assigned_slots,payments,utilities,budgets))
            print(history[step])

runAuctions([Bot1,Bot2])
