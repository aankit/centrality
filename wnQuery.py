#wordnet functions - what data do I want to extract?
#lemmas - names, antonyms, derivationally_related_forms, pertainyms (adj) 

import random, nltk
nltk.data.path.append('./nltk_data/')
from nltk.corpus import wordnet as wn

class Syns(object):

	def __init__(self, word, pos):		
		self.word = word
		self.pos = pos
		self.number = 0
		self.structure = self.generateStructure(word, pos)

	def generateStructure(self, word, pos):
		structure = dict()
		synsets = [synset for synset in wn.synsets(word) if synset.pos == pos]
		for synset in synsets:
			if synset.pos == pos:
				if synset.name not in structure:
					self.number += 1
					structure[synset.name] = synsets[0].path_similarity(synset)
		return structure

	def ontoList(self, synset):
		# things to pick from
		ln = wn.synset(synset).lexname.split('.')[1]
		hyper = self.lemmatize(self.getHypernyms(synset))
		definition = self.getDefinition(synset)
		lemmas = self.lemmatize(self.getLemmas(synset))
		examples = self.getExamples(synset)
		strings = [string.replace("_", " ") for string in self.getFrameStrings(synset)]
		hypo = self.lemmatize(self.getHyponyms(synset))  
		
		ontologyList = [strings, ln, lemmas, examples, hypo, definition, hyper]
		returnList = list()
		for o in ontologyList:
			if o:
				returnList.append(o)
		return returnList

	def chooser(self, l, i):
		if type(l[i]) == list:
			# print "this is o[i]: " + str(o[i])
			j = random.choice(l[i])
			return j
		else:
			return l[i]

	def findCaps(self, l):
		templist = list()
		for i in l:
			templist.append(" ".join([word for word in i.split(" ") if not word.isupper()]))
		return templist

	def ontologies(self, synset, sd):
		o = self.ontoList(synset)
		inBounds = ""
		if o:
			inBounds = self.chooser(o, random.randint(0,len(o)-1))
			# for i in range(-2, 2):
			# 	if sd<=i and sd>=i-1:
			# 		inBounds.append(self.chooser(o, i+2))
		return inBounds

	def lexStringFilter(self, synset):
		compareList = list()
		compareList.extend(self.lemmatize(self.getLemmas(synset)))
		compareList.extend(self.lemmatize(self.getHypernyms(synset)))
		compareList.extend(self.lemmatize(self.getHyponyms(synset)))
		return compareList

	def getSynset(self, word):
		return [synset.name for synset in wn.synsets(word) if synset.pos == self.pos]

	def getDefinition(self, synset):
		return wn.synset(synset).definition

	def getExamples(self, synset):
		return wn.synset(synset).examples

	def getLemmas(self, synset):
		return wn.synset(synset).lemmas

	def getFrameStrings(self, synset):
		frameStrings = list()
		synset = wn.synset(synset)
		for lemma in synset.lemmas:
			if(lemma != synset.lemmas[0]):
				lfs_less = self.findCaps(lemma.frame_strings)
				frameStrings.extend(lfs_less)
		return frameStrings

	def getLexname(self, synset):
		return wn.synset(synset).lexname

	#less specific
	def getHypernyms(self, synset):
		root = wn.synset(synset).root_hypernyms()
		hyper = wn.synset(synset).hypernyms()
		root.extend(hyper)
		return root

	#more specific
	def getHyponyms(self, synset):
		hyponyms = list()
		for h in self.getHypernyms(synset):
			hyponyms.extend(h.hyponyms())
		return hyponyms

	def lemmatize(self, thingList):
		try:
			return [t.name.replace("_", " ") for tl in thingList for t in tl.lemmas]
		except:
			return [t.name.replace("_", " ") for t in thingList]

class Pos(object):

	def __init__(self, word):
		self.word = word

	def verbExists(self):
		synlist = wn.synsets(self.word)
		returnVar = False
		for sl in synlist:
			if sl.pos == 'v':
				 returnVar = True
		return returnVar


#decode('ascii', errors='replace') this might be necessary

if __name__ == "__main__":
	import sys
	pos = Pos(sys.argv[1])
	# theList = list()
	print pos.verbExists()
		


