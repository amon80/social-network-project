from abc import ABCMeta, abstractmethod

# Bots:
#   INPUT
#       - Name (?)
#       - Personal Evaluation
#       - Bid History
#         |- Bids.      KEY: Advertisers    VALUE: Bids
#         |- Slots      KEY: Advertisers    VALUE: Slots
#         '- Pays       KEY: Advertisers    VALUE: Prices
#       - Slots Clickthrough Rates
#   OUTPUT
#       - Bid

class Bot(metaclass=ABCMeta):
    @abstractmethod
    def best_response(self,name,bids,slot_ctrs,history):
        pass


class Bot1(Bot):
    """Best-response bot with balanced tie-breaking rule"""
    def best_response(self,name,bids,slot_ctrs,history):
        return

class Bot2(Bot):
    """Best-response bot with comptetitor bursting tie-breaking rule"""
    """Submit the highest possible bid that gives the desired slot"""
    def best_response(self,name,bids,slot_ctrs,history):
        return

class Bot3(Bot):
    """Best-response bot with altruistic bidding tie-breaking rule"""
    """Submit the lowest possible bid that gives the desired slot"""
    def best_response(self,name,bids,slot_ctrs,history):
        return

class Bot4(Bot):
    """Comptetitor-bursting bot"""
    """Submit the highest bid seen in previous auctions, even if it is greater than own value"""
    def best_response(self,name,bids,slot_ctrs,history):
        return

class Bot5(Bot):
    """Budget-saving bot"""
    """Submit minimum among the last non-winning bid and the advertiser value for the query"""
    def best_response(self,name,bids,slot_ctrs,history):
        return

class Bot6(Bot):
    """Random bot"""
    """Submit random bid"""
    def best_response(self,name,bids,slot_ctrs,history):
        return

class Bot7(Bot):
    """Combination ov the above bots based on the current badget or the advertiser value for the current query"""
    
    def best_response(self,name,bids,slot_ctrs,history):
        return

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
# def best_response(name, adv_value, slot_ctrs, history):
    
#     step = len(history)
    
#     #If this is the first step there is no history and no best-response is possible
#     #We suppose that adevertisers simply bid their value.
#     #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
#     if step == 0:
#         return adv_value
    
#     #Initialization
#     adv_slots=history[step-1]["adv_slots"]
#     adv_bids=history[step-1]["adv_bids"]
    
#     sort_bids=sorted(adv_bids.values(), reverse=True)
#     sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
#     #Saving the index of slots assigned at the advertiser in the previous auction
#     if name not in adv_slots.keys():
#         last_slot=-1
#     else:
#         last_slot=sort_slots.index(adv_slots[name])
        
#     #The best response bot makes the following steps:
#     #1) Evaluate for each slot, how much the advertiser would pay if
#     #   - he changes his bid so that that slot is assigned to him
#     #   - no other advertiser change the bid
#     for i in range(len(sort_slots)):
        
#         if i < last_slot: #If I take a slot better than the one previously assigned to me
#             tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
            
#         elif i = len(sort_bids) - 1 #If I take the last slot, I must pay 0
#             tmp_pay = 0
            
#         else: #If I take the slot as before or a worse one (but not the last)
#             tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser
        
#     #2) Evaluate for each slot, which one gives to the advertiser the largest utility
#     #ToDo
    
#     #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
#     #ToDo
    
#     return best