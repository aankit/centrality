import itertools, string, random

class Nonsensenator(object):

	def __init__(self):
		self.bigrams = True
		self.source = list()
		#object objects
		self.combos = list()
		self.ncombos = dict()
		self.nposition = dict()
		self.after = dict()
		self.before = dict()
		self.posprops = dict()
		#word vars
		#combinations of letters in alphabet
		self.combos = [x+y for x,y in itertools.product(string.ascii_lowercase, repeat=2)]
		#analyze the bigrams found in the words

	def giveMeNonsense(self, ofThisStuff, length, b=True):
		self.source = ofThisStuff
		self.bigrams = b
		# self.bigramAnalyzer()
		return self.newWord(length)

	def select_weighted_int(self, d):
	   offset = random.randint(0, sum(d.itervalues())-1)
	   for k, v in d.iteritems():
	      if offset < v:
	         return k
	      offset -= v

	def select_max_at_pos(self, l, d, pos):
		max_prob = 0.0
		max_at_pos = ""
		for i in l:
			if d[i][pos] > max_prob:
				max_at_pos = i
				max_prob = d[i][pos]
		return max_at_pos

	def add(self, d, k1, k2, dim=2):
		if dim==2:
			if k1 not in d:
				d[k1] = dict()
			
				if k2 not in d[k1]:
					d[k1][k2] = 1
				else:
					d[k1][k2] += 1
		else:
			if k1 not in d:
				d[k1] = 1
			else:
				d[k1] += 1



	def bigramAnalyzer(self):
		
		#bigram frequency, position, and relationships
		for word in self.source:
			word = word.strip().lower()
			#foundBigrams = list()
			for c in self.combos:					
				if c in word:
					self.add(self.ncombos, c, "this means nothing", dim=1)
					
					#add the position in the word to nposition
					position = word.find(c)
					# print position
					self.add(self.nposition, c, position)

					#let's get the bigram before and...
					if position>=2:
						overlap = random.choice([True, True, True, True, True, True, False])+1
						prevBigram = word[position-overlap]+word[position-overlap+1]
						self.add(self.before, c, prevBigram)
					# elif position==1:
					# 	prevBigram = word[position-1]+word[position]
					# 	self.add(self.before, c, prevBigram)
						
					#also let's go ahead and get the one after
					
					if (len(word)-position)>3:
						overlap = random.choice([True, True, True, True, True, True, False])+1
						nextBigram = word[position+overlap] + word[position+overlap+1]
						self.add(self.after, c, nextBigram)
					# elif (len(word)-position)==3:
					# 	nextBigram = word[position+1] + word[position+2]
					# 	self.add(self.after, c, nextBigram)

	def newWord(self, length):
		
		if self.bigrams:
			self.bigramAnalyzer()
			newWord = ""

			#get the bigram seed that will create our word and the position we want to start it in
			seed = self.select_weighted_int(self.ncombos)
			seedPos = self.select_weighted_int(self.nposition[seed])

			#length of word based on seedPos
			# wordLen = length-seedPos
			word = list()
			if seedPos > length:
				word = [0]*(seedPos+1)
			else:
				word = [0]*(length+1)
			word[seedPos] = seed

			for i in range(len(word)):
				if i < seedPos:
					if seed in self.before:
						word[seedPos-(i+1)] = self.select_weighted_int(self.before[seed])
						seed = word[seedPos-(i+1)]
				elif i > seedPos:
					if seed in self.after:
						word[i] = self.select_weighted_int(self.after[seed])
						seed = word[i]

			word = filter(lambda x: x!=0, word)
			return "".join(word)
		else:
			newWord = random.choice(self.source)
			#print newWord
			return newWord

if __name__ == '__main__':
	import sys
	n = Nonsensenator()
	words = list()
	for l in sys.stdin:
		l = l.strip()
		words.append(l)
	# print words
	print n.giveMeNonsense(words, True)





