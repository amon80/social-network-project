import csv
import constants


class Reporter(object):

	bots = []
	bots_types = []
	executionNumber = -1
	slots = dict()

	values = dict()
	starting_budgets = dict()

	firstCall = True


	printStepOutput = True
	writeStepOutput = False
	writeStepOutputAll = False
	writeStepOutputUs = False

	writeAuctionsAdvertiserOutput = True
	writeAuctionsAuctionOutput = False

	def reportStep(self,step,max_step,stepHistory,our_expenses,our_utility):
		if self.printStepOutput:
			print("_______________________________________________________________",step,"/",max_step)
			print("Name\tBot\tValue\tBid\tPayment\tUtility\tSlot\tCtr\tBudget")
			for bot in self.bots:
				if bot in stepHistory[constants.WINNERS_KEY]:
					slot = stepHistory[constants.WINNERS_KEY][bot]
					slot_ctr = ("%.2f"% self.slots[slot])
					paid = ("%.2f"%stepHistory[constants.PAYMENTS_KEY][bot])
				else:
					slot = ""
					slot_ctr = ""
					paid = ""
				print(bot,"\t",self.bots_types[bot],"\t%.2f" % self.values[bot],
						"\t%.2f" % stepHistory[constants.BIDS_KEY][bot],
						"\t",paid,
						"\t%.2f" % stepHistory[constants.UTILITIES_KEY][bot],
						"\t",slot,
						"\t", slot_ctr,
						"\t%.0f/%.0f" % (stepHistory[constants.BUDGETS_KEY][bot],self.starting_budgets[bot]),)
		if self.writeStepOutput:
			if self.writeStepOutputAll:
				with open('Reports/'+str(self.executionNumber)+'_stepReportAll.csv','a') as csvfile:
					fieldnames = list(self.bots)
					writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
					if self.firstCall:
						writer.writeheader()
					toWrite = dict()
					for bot in self.bots:
						toWrite[bot] = ("%.2f"% stepHistory[constants.UTILITIES_KEY][bot]).replace(".",",")
						# if bot in stepHistory[constants.PAYMENTS_KEY]:
							# toWrite[bot] = stepHistory[constants.BUDGETS_KEY][bot]
						# else:
						# 	toWrite[bot] = 0
					writer.writerow(toWrite)
			elif self.writeStepOutputUs:
				with open('Reports/'+str(self.executionNumber)+'_stepReportUs.csv','a') as csvfile:
					fieldnames = ["expenses","utility","budget"]
					writer = csv.DictWriter(csvfile,fieldnames = fieldnames)

					our_budget = ("%.2f"% stepHistory[constants.BUDGETS_KEY][constants.OUR_BOT_NAME]).replace(".",",")
					if self.firstCall:
						writer.writeheader()
					writer.writerow({"expenses":("%.2f"% our_expenses).replace(".",","),"utility":("%.2f"% our_utility).replace(".",","), "budget":our_budget})

		self.firstCall = False





	def reportAuction(self,history):
		with open('Reports/'+str(self.executionNumber)+'_auctionReport.csv','a') as csvfile:
			fieldnames = []
			row = {}
			for step in range(100):
				stepName = str(step)
				fieldnames.append(stepName)
				if step < len(history):
					row[stepName] = ("%.2f"% history[step][constants.BUDGETS_KEY][constants.OUR_BOT_NAME]).replace(".",",")
				else:
					row[stepName] =  0

			writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
			if self.firstCall:
				writer.writeheader()
				self.firstCall = False
			writer.writerow(row)




	def reportAuctions(self,our_expenses,our_utility,auctions_revenue,auctions_utility):
		if self.writeAuctionsAdvertiserOutput:
			with open('Reports/'+str(self.executionNumber)+'_auctionsAdvertiserReport.csv','a') as csvfile:
				fieldnames = ["Our Bot","Adversary","Utility"]
				writer = csv.DictWriter(csvfile,fieldnames = fieldnames)

				if self.firstCall:
					writer.writeheader()
				writer.writerow({"Our Bot":self.bots_types[constants.OUR_BOT_NAME],"Adversary":self.bots_types["b"],"Utility":("%.2f"% our_utility).replace(".",",")})
		if self.writeAuctionsAuctionOutput:
			with open('Reports/'+str(self.executionNumber)+'_auctionsAuctionReport.csv','a') as csvfile:
				fieldnames = ["Bots","Auction revenue","Auction utility"]
				writer = csv.DictWriter(csvfile,fieldnames = fieldnames)

				if self.firstCall:
					writer.writeheader()
				writer.writerow({"Bots":self.bots_types[constants.OUR_BOT_NAME],"Auction revenue":("%.2f"% auctions_revenue).replace(".",","),"Auction utility":("%.2f"% auctions_utility).replace(".",",")})
		self.firstCall = False




outputRecap = True

def printAuctionRevenue(history,bots):
	bot_payments = dict()
	bot_utilities = dict()
	auction_revenue = 0
	auction_utilities = 0
	for bot in bots.keys():
		bot_payments[bot] = 0
		bot_utilities[bot] = 0

	for step in range(len(history)):
		for payingbot in history[step]["adv_pays"]:
			auction_revenue += history[step]["adv_pays"][payingbot]
			auction_utilities += history[step]["adv_utilities"][payingbot]
			bot_utilities[payingbot] += history[step]["adv_utilities"][payingbot]
			bot_payments[payingbot] += history[step]["adv_pays"][payingbot]

	print("User\tExpense\t\tUtility")
	for bot in bot_payments.keys():
		print(bot,"\t%.2f" % bot_payments[bot],"\t\t%.2f" % bot_utilities[bot])

	print("TOT\t%.2f" % auction_revenue,"\t\t%.2f" % auction_utilities)

def printAuctionSettings(no,number_of_bots,minSlots,maxSlots,minValue,maxValue,minBudget,maxBudget,nAuctions,max_step,isVCG):
	with open('Reports/'+str(no)+'_settings.txt','a') as txtfile:
		txtfile.write("N. Bots\t\t"+str(number_of_bots)+"\n")
		txtfile.write("Slots min\t\t"+str(minSlots)+"\n")
		txtfile.write("Slots max\t\t"+str(maxSlots)+"\n")
		txtfile.write("Evaluation min\t\t"+str(minValue)+"\n")
		txtfile.write("Evaluation max\t\t"+str(maxValue)+"\n")
		txtfile.write("Budget min\t\t"+str(minBudget)+"\n")
		txtfile.write("Budget max\t\t"+str(maxBudget)+"\n")
		txtfile.write("N. Auctions\t\t"+str(nAuctions)+"\n")
		txtfile.write("Step max\t\t"+str(max_step)+"\n")
		if isVCG:
			txtfile.write("Auction type\tVCG\n")
		else:
			txtfile.write("Auction type\tFirst Price Auction\n")

def printMultipleAuctionsRecap(our_utility,our_expenses,auction_revenue,auction_utility,ourbot, otherbots,no):
	if outputRecap:
		print()
		print("Using",ourbot,"against",otherbots)
		print("We spent %.2f" % our_expenses)
		print("For a utility of %.2f" % our_utility)
		print("Total Auction Revenue was of %.2f" % auction_revenue)
		print("Total Auction Utility was of %.2f" % auction_utility)
	with open('Reports/'+str(no)+'_report.csv','a') as csvfile:
		fieldnames = ["other_bots","our_bot","expenses","utilities"]
		writer = csv.DictWriter(csvfile,fieldnames = fieldnames)

		# writer.writeheader()
		writer.writerow({"other_bots":str(otherbots),"our_bot":str(ourbot),
						"expenses":our_expenses,"utilities":our_utility})

	with open('Reports/'+str(no)+'_revenue.csv','a') as csvfile:
		fieldnames = ["other_bots","our_bot","revenues","utilities"]
		writer = csv.DictWriter(csvfile,fieldnames = fieldnames)

		# writer.writeheader()
		writer.writerow({"other_bots":str(otherbots),"our_bot":str(ourbot),
						"revenues":auction_revenue,"utilities":auction_utility})


def printSingleAuctionRecap(history,values,bots,sbudgets):
	print("SINGLE AUCTION RECAP")
	for botVal in values.keys():
		print(botVal+":"+str(values[botVal]),end = "\t")
	print()
	start_budget = sbudgets[botname]
	end_budget = history[len(history)-1]["adv_budgets"][botname]
	spent_budget = start_budget - end_budget
	total_utility = 0
	print("Starting budget was ","%.2f" % start_budget)
	print("Final budget was ","%.2f" % end_budget)
	print("We spent ","%.2f" % spent_budget)

	for curr_step in range(len(history)):
		total_utility += history[curr_step]["adv_utilities"][botname]
	print("For a utility of ","%.2f" % total_utility)
	print()

	print("________________________________________________________________________")


def printTableRow(step,budgets,bids,slots,payments,utilities,evaluation,bots):
	print("________________________________________________________________________")
	print("#",step,end="\t")
	for adv in budgets.keys():
		print(adv,end="\t")
	print("\n________________________________________________________________________")
	print("\nbots",end="\t")
	for adv in budgets.keys():
		print(str(bots[adv]),end="\t")
	print("\nbudget",end="\t")
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
