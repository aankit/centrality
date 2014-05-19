from wnQuery import Syns, Pos
import BellCurve
import nonsensenator
import sys, numpy, random, operator

class Centrality(object): 

	def __init__(self, word):
		self.word = word
		self.pos = "v"
		self.verbExists = Pos(word)
		self.s = Syns(self.word, self.pos)
		self.n = nonsensenator.Nonsensenator()
		self.curves = dict()
		sourceOntology = list()
		self.cleanOntology = list()
		#these are the keys
		self.varScalar = 1.20	#shape of the curve
		self.nonsense = .50		#amount and spread of nonsense in standard deviations

		#generate variance of each synset's distribution, create the curve, 
		#and pull the full ontology for nonsensenator
		count = 0
		for k,v in self.s.structure.items():
			count += 1
			svar = self.varScalar*v
			bc = BellCurve.BellCurve(v, svar)
			self.curves[k] = bc
			sourceOntology.extend(self.s.ontoList(k))

		self.numLines = int(count*2)	#poem length
		self.minWords = 10		#line length


		#clean up the sourceOntology to be a list of individual words, that's all
		#nonsensenator will accept
		for item in sourceOntology:
			if type(item) == list:
				for i in item:
					i = i.strip()
					i_words = i.split(' ')
					for w in i_words:
						if w.lower() != 'something' and w.lower() != 'somebody':
							self.cleanOntology.append(w)
			else:
				item = item.strip()
				item_words = item.split(' ')
				for w in item_words:
					if w.lower() != 'something' and w.lower() != 'somebody':
							self.cleanOntology.append(w)

	def writePoem(self):
		if self.verbExists.verbExists():
			outputStr = ""
			#main loop, can adjust the linspace min and max to calibrate the poem
			xAxis = numpy.linspace(-.5,1.25, num=self.numLines)
			lineCount = 0;
			for x in numpy.nditer(xAxis):
				
				line=list()
				totalWords = 0
				diff = self.minWords
				words = ''
				while diff>0:
					# get the synset & the word
					synset = self.pickSynset(x)
					word = self.getWords(x, synset)
					# add words to the running list for the line
					line.append(word)
					# perform check on line length
					words += word
					countWords = words.split(" ")
					for word in countWords:
						totalWords += 1
					diff = self.minWords - totalWords
				if line:
					toPrint = " ".join(line)
				else:
					toPrint = line[0]
				toPrint = toPrint.strip()
				if lineCount%5 == 0 and lineCount != 0:
					lineCount += 1
					outputStr += "<br>"
					outputStr += toPrint + "<br>"
				else:
					lineCount += 1
					outputStr += toPrint + "<br>"
			return outputStr	
		else:
			return "No poem for you because you didn't follow my one request, I'm just a dumb computer."


	def select_weighted_uni(self, d, min, max):
		target = random.uniform(min, max)
		winner = ''
		sortedProb = sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)
		for k, v in sortedProb:
			if target < v:	
				winner = k
		return winner

	def pickSynset(self, x):
		prob = dict()
		for k,v in self.curves.items():
			prob[k] = v.probability(x)
		maxProb = max(prob.iteritems(), key=lambda foo:foo[1])[1]
		return self.select_weighted_uni(prob, 0, maxProb)


	def getWords(self, x, k):
		v = self.curves[k]
		sd = v.stdev(x)
		if sd<self.nonsense and sd>-self.nonsense:
			w = self.s.ontologies(k, sd)
			#turn it into a list
			wList = w.split(" ")
			if len(wList) > 1:
				tempList = list()
				for i in wList:
					# iLemma = s.lemmatize(s.getLemmas(s.getSynset(i)))
					# print iLemma
					# print s.lexStringFilter(k)
					if i in self.s.lexStringFilter(k):
						# print 'eval'
						tempList.append(self.n.giveMeNonsense(self.cleanOntology, len(i)/2, True))
					else:
						tempList.append(i)
				return " ".join(tempList)
			else:
				return self.n.giveMeNonsense(self.cleanOntology, len(w)/2, True)
		else:
			return self.s.ontologies(k, sd)

		

#				 ||   __/\				
# ______________{..}__(^/^)_________________
# ______|______|______|______|______|______|
# ___|______|______|______|______|______|___


if __name__ == '__main__':
	centrality = Centrality(sys.argv[1])
	print centrality.writePoem()


