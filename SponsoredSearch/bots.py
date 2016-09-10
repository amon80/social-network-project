from abc import ABCMeta, abstractmethod
from random import randint
from math import ceil
import constants


# Bots:
#   INPUT
#       - Name (?)
#       - Personal Evaluation
#       - Bid History
#         |- Bids       KEY: Advertisers    VALUE: Bids
#         |- Slots      KEY: Advertisers    VALUE: Slots
#         '- Pays       KEY: Advertisers    VALUE: Prices
#       - Slots Clickthrough Rates
#       - Current Budget
#       - Initial Budget
#   OUTPUT
#       - Bid


# METAS
class Bot1Meta(type):
    def __str__(self):
        return "Bot1"

class Bot2Meta(type):
    def __str__(self):
        return "Bot2"

class Bot3Meta(type):
    def __str__(self):
        return "Bot3"

class Bot4Meta(type):
    def __str__(self):
        return "Bot4"

class Bot5Meta(type):
    def __str__(self):
        return "Bot5"

class Bot6Meta(type):
    def __str__(self):
        return "Bot6"

class Bot7Meta(type):
    def __str__(self):
        return "Bot7"

class Bot8Meta(type):
    def __str__(self):
        return "Bot8"

class Bot9Meta(type):
    def __str__(self):
        return "Bot9"

class Bot(object):
# class Bot(metaclass=ABCMeta):
    @abstractmethod
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        pass


def evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation):
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sorted_slots_clicktr)):

        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sorted_last_step_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
        elif i == len(sorted_last_step_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
        else:    #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sorted_last_step_bids[i+1]

        #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sorted_slots_clicktr[i]]*(evaluation - tmp_pay)

        if new_utility > utility :
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay

    if utility<0:
        preferred_slot = -1
    return utility, preferred_slot, payment

class Bot1(Bot,metaclass=Bot1Meta):

    """Best-response bot with balanced tie-breaking rule"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        if evaluation==0:
            return 0
        #If this is the first step there is no history and no best-response is possible
        #We suppose that adevertisers simply bid their value.
        #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
        if step == 0:
            return evaluation

        #Initialization
        last_step_slots = history[step-1][constants.SLOTS_KEY]
        last_step_bids = history[step-1][constants.BIDS_KEY]

        sorted_last_step_bids = sorted(last_step_bids.values(), reverse = True)
        sorted_slots_clicktr = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

        #Saving the index of slots assigned at the advertiser in the previous auction
        if name not in last_step_slots.keys():
            last_slot = -1
        else:
            last_slot = sorted_slots_clicktr.index(last_step_bids[name])

        utility, preferred_slot, payment = evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation)

        #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
        if preferred_slot == -1:
            # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
            return min(evaluation, sorted_last_step_bids[len(sorted_last_step_bids)-1])

        if preferred_slot == 0:
            # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
            return float(evaluation+payment)/2

        #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
        return (evaluation - float(slot_ctrs[sorted_slots_clicktr[preferred_slot]])/slot_ctrs[sorted_slots_clicktr[preferred_slot-1]] * (evaluation - payment))

    def __str__(self):
        return "Bot1"

    def strategy(self):
        return "Best-response bot with balanced tie-breaking rule"


class Bot2(Bot,metaclass=Bot2Meta):
    """Best-response bot with competitor bursting tie-breaking rule"""
    """Submit the highest possible bid that gives the desired slot"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        #If this is the first step there is no history and no best-response is possible
        #We suppose that adevertisers simply bid their value.
        #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
        if step == 0:
            return evaluation

        #Initialization
        last_step_slots = history[step-1][constants.SLOTS_KEY]
        last_step_bids = history[step-1][constants.BIDS_KEY]

        sorted_last_step_bids = sorted(last_step_bids.values(), reverse = True)
        sorted_slots_clicktr = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

        #Saving the index of slots assigned at the advertiser in the previous auction
        if name not in last_step_slots.keys():
            last_slot = -1
        else:
            last_slot = sorted_slots_clicktr.index(last_step_bids[name])

        utility, preferred_slot, payment = evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation)

        #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
        if preferred_slot == -1:
            # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
            return min(evaluation, sorted_last_step_bids[len(sorted_last_step_bids)-1])

        if preferred_slot == 0:
            # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
            return float(evaluation+payment)/2



        #TIE-BREAKING RULE: Submit the highest possible bid that gives the desired slot
        return sorted_last_step_bids[preferred_slot-1] - 0.1

    def __str__(self):
        return "Bot2"

    def strategy(self):
        return "Competitor bursting, Submit the highest possible bid that gives the desired slot"


class Bot3(Bot,metaclass=Bot3Meta):
    """Best-response bot with altruistic bidding tie-breaking rule"""
    """Submit the lowest possible bid that gives the desired slot"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        #If this is the first step there is no history and no best-response is possible
        #We suppose that adevertisers simply bid their value.
        #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
        if step == 0:
            return evaluation

        #Initialization
        last_step_slots = history[step-1][constants.SLOTS_KEY]
        last_step_bids = history[step-1][constants.BIDS_KEY]

        sorted_last_step_bids = sorted(last_step_bids.values(), reverse = True)
        sorted_slots_clicktr = sorted(slot_ctrs.keys(), key = slot_ctrs.__getitem__, reverse = True)

        #Saving the index of slots assigned at the advertiser in the previous auction
        if name not in last_step_slots.keys():
            last_slot = -1
        else:
            last_slot = sorted_slots_clicktr.index(last_step_bids[name])

        utility, preferred_slot, payment = evaluate_slots(sorted_slots_clicktr, sorted_last_step_bids, slot_ctrs, last_slot, evaluation)

        #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
        if preferred_slot == -1:
            # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
            return min(evaluation, sorted_last_step_bids[len(sorted_last_step_bids)-1])

        if preferred_slot == 0:
            # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
            return float(evaluation+payment)/2

        #TIE-BREAKING RULE: Submit the lowest possible bid that gives the desired slot
        return sorted_last_step_bids[preferred_slot]

    def __str__(self):
        return "Bot3"

    def strategy(self):
        return "Altruistic bidding, submit the lowest possible bid that gives the desired slot"


class Bot4(Bot,metaclass=Bot4Meta):
    """Competitor-bursting bot"""
    """Submit the highest bid seen in previous auctions, even if it is greater than own value"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):

        step = len(history)

        if step == 0:
            return evaluation

        max_bid = -1
        for step in range(len(history)):
            for bid in history[step][constants.BIDS_KEY].values():
                if bid >= max_bid:
                    max_bid = bid
        return max_bid

    def __str__(self):
        return "Bot4"

    def strategy(self):
        return "Competitor-bursting bot, Submit the highest bid seen in previous auctions"

class Bot5(Bot,metaclass=Bot5Meta):
    """Budget-saving bot"""
    """Submit minimum among the last non-winning bid and the advertiser value for the query"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):

        step = len(history)

        if step == 0:
            return evaluation

        last_step_bids = history[step-1][constants.BIDS_KEY]
        min_bid_last_step = min(last_step_bids.values())


        return min(min_bid_last_step, evaluation)

    def __str__(self):
        return "Bot5"

    def strategy(self):
        return "Budget-saving bot, Submit minimum among the last non-winning bid and the advertiser value for the query"

class Bot6(Bot,metaclass=Bot6Meta):
    """Random bot"""
    """Submit random bid"""
    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):

        # step = len(history)

        # if step == 0:
        #     return evaluation

        # last_step_bids = history[step-1][constants.BIDS_KEY]
        # min_bid_last_step = min(last_step_bids.values())
        # max_bid_last_step = max(last_step_bids.values())
        # mab = ceil(min_bid_last_step*10)
        # mib = ceil(max_bid_last_step*10)
        return randint(0,10)

    def __str__(self):
        return "Bot6"

    def strategy(self):
        return "Random bot, Submit random bid"

class Bot7(Bot,metaclass=Bot7Meta):
    """Combination of the above bots based on the current badget or the advertiser value for the current query"""
    "e.g. do competitor-bursting as long as your current budget is half the initial budget and then do best-response"

    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        if step == 0:
            return evaluation

        if current_budget > initial_budget/2:
            return Bot4().response(name,evaluation,history,slot_ctrs,current_budget, initial_budget)
        else:
            return Bot1().response(name,evaluation,history,slot_ctrs,current_budget, initial_budget)
        return

    def __str__(self):
        return "Bot7"

    def strategy(self):
        return "Do competitor-bursting as long as your current budget is half the initial budget and then do best-response"

class Bot8(Bot,metaclass=Bot8Meta):
    """Combination of the above bots based on the current badget or the advertiser value for the current query"""
    "e.g. do competitor bursting for queries for which the advertiser value is high and budget-saving for the others"

    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        if step == 0:
            return evaluation

        if evaluation > 6:
            return Bot4().response(name,evaluation,history,slot_ctrs,current_budget, initial_budget)
        else:
            return Bot5().response(name,evaluation,history,slot_ctrs,current_budget, initial_budget)


    def __str__(self):
        return "Bot8"

    def strategy(self):
        return "Combination of the above bots based on the current badget or the advertiser value for the current query"

class Bot9(Bot,metaclass=Bot9Meta):
    bidRaise = 0.1

    def response(self,name,evaluation,history,slot_ctrs,current_budget, initial_budget):
        step = len(history)

        if step == 0:
            return 0

        utility = 0
        payment = 0


        for winner in history[step-1][constants.PAYMENTS_KEY]:
            paid = history[step-1][constants.PAYMENTS_KEY][winner]
            ctr = slot_ctrs[history[step-1][constants.WINNERS_KEY][winner]]

            if winner == name:
                #If the bot won this slot, he has no interest in raising its price
                new_utility = (evaluation - paid)*ctr
                if new_utility > utility:
                    utility = new_utility
                    payment = paid
            else:
                #If another bot won this slot, the bot must raise to obtain it
                new_utility = (evaluation - paid-self.bidRaise)*ctr
                if new_utility > utility:
                    utility = new_utility
                    payment = paid + self.bidRaise

        return payment




    def __str__(self):
        return "Bot9"

    def strategy(self):
        return "Incremental Bot - Begins low, grow higher to obtain its place."



#We implement a possible bot for an advertiser in a repeated GSP auction
#The bot of an advertiser is a program that, given the history of what occurred in previous auctions, suggest a bid for the next auction.
#Specifically, a bot takes in input
#- the name of the advertiser (it allows to use the same bot for multiple advertisers)
#- the value of the advertiser (it is necessary for evaluating the utility of the advertiser)
#- the clickthrough rates of the slots
#- the history
#We assume the history is represented as an array that contains an entry for each time step,
#i.e. history[i] contains the information about the i-th auction.
#In particular, for each time step we have that
#- history[i]["adv_bids"] returns the advertisers' bids as a dictionary in which the keys are advertisers' names and values are their bids
#- history[i]["adv_slots"] returns the assignment as a dictionary in which the keys are advertisers' names and values are their assigned slots
#- history[i]["adv_pays"] returns the payments as a dictionary in which the keys are advertisers' names and values are their assigned prices

#The bot that we implement here is a symple best_response bot:
#it completely disregards the history except the last step,
#and suggest the bid that will maximize the advertiser utility
#given that the other advertisers do not change their bids.
def best_response(name, adv_value, slot_ctrs, history):

    step = len(history)

    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0

    #Initialization
    adv_slots=history[step-1][constants.SLOTS_KEY]
    adv_bids=history[step-1][constants.BIDS_KEY]

    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)

    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])

    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):

        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned

        elif i == len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0

        else: #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser

    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)

        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay

    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return min(adv_value, sort_bids[len(sort_slots)])

    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value+payment)/2



    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return (adv_value - float(slot_ctrs[sort_slots[preferred_slot]])/slot_ctrs[sort_slots[preferred_slot-1]] * (adv_value - payment))
