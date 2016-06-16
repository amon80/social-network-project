from random import randint, choice

def generateRandomDoc(wordsArray, nDoc, maxWords, minWords):	
	f = open('queryfileT.txt','w')
	for di in range(nDoc):
		docName = "doc"+str(di)
		nWords = randint(minWords,maxWords)

		

		f.write(docName+" ")
		for i in range(nWords):
			f.write(choice(wordsArray)+" ")
		f.write('\n')
	f.close()



wordsArray = ['prova','test','esame','appello', 'ciaone', 'pippo', 'paperino', 'pluto', 'vasco', 'rossi', 'blasco', 'comandante', 'gigidag', 'ernesto', 'anestepone', 'platone', 'socrate', 'homecoming', 'vagone', 'compilatori', 'score', 'partita', 'calcio']

# a little cheat to make some words more frequent
wordsRedArray = wordsArray[:10]
wordsArray.extend(wordsRedArray)

generateRandomDoc(wordsArray,40,30,10)




