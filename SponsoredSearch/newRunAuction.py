from auctions import myBalance, budgetedVCGBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from Reporter import *
from string import ascii_lowercase
from random import randint
from math import ceil
import time
import constants

#SETTINGS
#number of advertisers
num_advertisers = 7

#number of executions
nAuctions = 1
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

mustReportStep = True
mustReportAuction = False
mustReportAuctions = False

all_bots_list = [Bot1,Bot2,Bot3,Bot4,Bot5,Bot6,Bot7]





def generateBots(bots_list):
    bots = dict()

    for b in range(len(bots_list)):
        bots[ascii_lowercase[b]] = bots_list[b]()
    return bots

def runAuctions(bots_list):
    bots = generateBots(bots_list)

    #Update Reporter
    rep.bots = list(bots.keys())
    rep.bots_types = bots

    #Variables
    our_expenses = 0
    our_utility = 0
    auctions_revenue = 0
    auctions_utility = 0

    for auctionIndex in range(nAuctions):
        #Auction initialization
        slots = generateSlots(minSlots,maxSlots)
        values, starting_budgets = generateAdvertisers(bots.keys(),minValue, maxValue,minBudget,maxBudget)

        #Update Reporter
        rep.slots = slots
        rep.values = values
        rep.starting_budgets = starting_budgets

        #Variables initialization
        step = 0
        history = []
        bids = dict()
        utilities = dict()
        budgets = dict(starting_budgets)
        done = False

        while not done and step < max_step:
            done = True
            for b in bots.keys():
                bids[b] = bots[b].response(b,values[b],history,slots,budgets[b],starting_budgets[b])
                if step == 0 or bids[b] != history[step-1]["adv_bids"][b]:
                    done = False
            if done:
                break


            # Run Auction
            if isVCG:
                assigned_slots, assigned_advs, payments = budgetedVCGBalance(slots,bids, starting_budgets,budgets)
            else:
                assigned_slots, assigned_advs, payments = myBalance(slots,bids,starting_budgets,budgets)



            # Update bots utilities and budgets
            utilities = dict()
            for bot in bots:
                if bot in payments and payments[bot] > 0:
                    utilities[bot] = (values[bot]*slots[assigned_advs[bot]] - payments[bot])
                    budgets[bot] = budgets[bot] - payments[bot]
                    auctions_revenue += payments[bot]
                else:
                    utilities[bot] = 0
                auctions_utility += utilities[bot]



            # Create History Step
            stepHistory = dict()
            stepHistory[constants.BIDS_KEY] = dict(bids)
            stepHistory[constants.SLOTS_KEY] = dict(assigned_slots)
            stepHistory[constants.PAYMENTS_KEY] = dict(payments)
            stepHistory[constants.UTILITIES_KEY] = dict(utilities)
            stepHistory[constants.BUDGETS_KEY] = dict(budgets)
            stepHistory[constants.WINNERS_KEY] = dict(assigned_advs)

            # Update our values
            if constants.OUR_BOT_NAME in payments:
                our_expenses += payments[constants.OUR_BOT_NAME]
                our_utility += utilities[constants.OUR_BOT_NAME]

            history.append(stepHistory)
            if mustReportStep:
                rep.reportStep(step,max_step,stepHistory,our_expenses,our_utility)
            step += 1
        if mustReportAuction:
            rep.reportAuction(history)
    if mustReportAuctions:
        rep.reportAuctions(our_expenses,our_utility,auctions_revenue,auctions_utility)

def generateBotList(us, adv,num):
    bl = []
    bl.append(us)
    for n in range(num):
        bl.append(adv)
    return bl

def runAllBotsAuction():
    runAuctions(all_bots_list)

def runSingleAuctionDifferentSettings():
    #Settings
    # range of number of slots available to sell
    global minSlots
    minSlots = 3
    global maxSlots
    maxSlots = 3
    #range of evaluation
    global minValue
    minValue = 0
    global maxValue
    maxValue = 10

    #range of budgets for each advertiser
    global minBudget
    minBudget = 100
    global maxBudget
    maxBudget = 200

    runSingleBotCombinationAuction()

def runSingleBotCombinationAuction():
    #Settings
    our_bot = Bot1
    their_bot = Bot1
    #execution
    runAuctions(generateBotList(our_bot,their_bot,num_advertisers))

def runMultipleBotCombinationsAuctions():
    #execution
    for us in all_bots_list:
        for adversary in all_bots_list:
            runAuctions(generateBotList(us,adversary,num_advertisers))


no = randint(1,1000)
rep = Reporter()
rep.executionNumber = no
print("Executing ",no)
runSingleBotCombinationAuction()
# runMultipleBotCombinationsAuctions()
# runAllBotsAuction()
# runSingleAuctionDifferentSettings()
