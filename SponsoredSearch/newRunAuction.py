from auctions import myBalance, budgetedVCGBalance
from AuctionGenerator import generateAdvertisers,generateSlots
from bots import Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7
from Reporter import *
from string import ascii_lowercase
from random import randint
from math import ceil
import time



def generateBots(bots_list):
    adv_bots = dict()

    for b in range(len(bots_list)):
        adv_bots[ascii_lowercase[b]] = bots_list[b]()
    return adv_bots

def runAuctions(bots_list):
    print(bots_list)
    adv_bots = generateBots(bots_list)

    print(adv_bots)




runAuctions([Bot1,Bot2])
