import csv


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

def printMultipleAuctionsRecap(our_utility,our_expenses,ourbot, otherbots,no):
	print()
	print("Using",ourbot,"against",otherbots)
	print("We spent %.2f" % our_expenses)
	print("For a utility of %.2f" % our_utility)
	with open('Reports/'+str(no)+'_report.csv','a') as csvfile:
		fieldnames = ["other_bots","our_bot","expenses","utilities"]
		writer = csv.DictWriter(csvfile,fieldnames = fieldnames)

		# writer.writeheader()
		writer.writerow({"other_bots":str(otherbots),"our_bot":str(ourbot),
						"expenses":our_expenses,"utilities":our_utility})


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
