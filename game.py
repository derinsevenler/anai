# This module contains the 'game' class
# A Game contains *all* information about a game *at a particular time*.
# It is omniscient. It runs play by sequentially asking players what changes they wish to make. 

import random

class Game:

	def __init__(self):
		# Instantiate a new game

		# Instantiate all the servers and installables
		self.RD = newCorpDeck()
		self.protectRD = []
		self.corpHand = [self.RD.pop(x) for x = [0,0]] # pull 2 cards to begin
		self.HQ = []
		self.protectHQ = []	# ICE protecting a server is
		self.ArchivesFaceUp = []
		self.ArchivesFaceDown = []
		self.protectArchives = []
		self.remoteServers = []
			# remoteServers is a list of dictionaries
			# Each dictionary key 'inside' gives a list of installed cards
			# Each dictionary key 'ice' gives a list of installed ICE
			# The unrezzed-rezzed status of cards is annotated with a suffix 'u' or 'r'. i.e., 'au' means unrezzed asset.
				# remoteServers[0] = {'inServer': 'au', 'ice': [] }
			# The runner sees un-rezzed ice/assets as simply their letter or otherwise 'u', e.g.,
				# {'inServer': 'u', 'ice': ['u', 'b']} <-- card in server is unrezzed, outermost ICE is barrier, inner ICE is unrezzed
			# Advanced cards are indicated with a number in between: e.g.,
				# Runner sees: 	{'inServer': '3u', 'ice': []} <-- server with unrezzed card advanced three times, no ice
				# Corp sees: 	{'inServer': 'g3u','ice':[]}
		self.stack = newRunnerDeck()
		self.heap = []
		self.grip = [self.stack.pop(x) for x = [0,0]] # pull 2 cards to begin
		self.runnerInstalled = [] # a list of all installed cards (ice breakers), labeled as strings, e.g. ['fracter','killer']

		# each player gets 5 credits to start
		self.corpCreds = 5
		self.runnerCreds = 5

		# Instantiate game variables
		self.turnNumber = 1
		self.runnerPoints = 0
		self.corpPoints = 0
		self.clicksLeft = 3
		self.timing = 0

	def playthrough(self, corpPlayer, runnerPlayer):


		while True:
			
			# ===================================
			# Corp's turn

			# 1. Draw Phase ---------------------

			# 1.1 paid ability window
			self.timing = 'c1.1'
			corpPlayer.paidAbility(self.corpView)
			runnerPlayer.paidAbility(self.runnerView)

			# 1.2 Turn begins - 'when your turn begins' conditional is met
			self.timing = 'c1.2'
			beginCorpTurn(self)

			# 1.3 Corp draws one card if able, otherwise loses immediately
			self.timing = 'c1.3'
			if (len(self.RD)<1):
				print('Runner wins by decking the corp!')
				break
			self.corpHand.append(self.RD.pop(0))

			# 2. Action Phase -------------------

			# 2.1 paid ability window
			self.timing = 'c2.1'
			corpPlayer.paidAbility(self.corpView)
			runnerPlayer.paidAbility(self.runnerView)

			# 2.2 Perform clicks
			self.timing = 'c2.2'
			while self.clicksLeft > 0

				corpPlayer.clickAbility(self)
				return self if self.corpPoints>=3 or self.runnerPoints>=3 # i.e., end the game if the corp scores out

				# paid ability window after each action
				corpPlayer.paidAbility(self.corpView)
				runnerPlayer.paidAbility(self.runnerView)

			# 3. Discard Phase ------------------

			# 3.1 discard down to maximum hand size
			self.timing = 'c3.1'
			corpPlayer.discardDown(self)

			# 3.2 paid ability window
			self.timing = 'c3.2'
			corpPlayer.paidAbility(self.corpView)
			runnerPlayer.paidAbility(self.runnerView)

			# 3.3 turn ends

			# ===================================
			# Runner's turn
			self.clicksLeft = 4

			# 1. Action Phase -------------------

			# 1.1 paid ability window
			self.timing = 'r1.1'
			runnerPlayer.paidAbility(self.runnerView)
			corpPlayer.paidAbility(self.corpView)

			# 1.2 Turn begins
			self.timing = 'r1.2'
			beginRunnerTurn(self)

			# 1.3 paid ability window
			self.timing = 'r1.3'
			runnerPlayer.paidAbility(self.runnerView)
			corpPlayer.paidAbility(self.corpView)

			# 1.4 Perform clicks
			self.timing = 'r1.4'
			while self.clicksLeft > 0

				runnerPlayer.clickAbility(self)
				return self if len(self.grip<0) #i.e., end the game if the runner has been flatlined
				return self if self.corpPoints>=3 or self.runnerPoints>=3 # i.e., end the game if the runner steals out
				
				print('clicks left:')
				print(self.clicksLeft)

				# paid ability window after each action
				runnerPlayer.paidAbility(self.runnerView)
				corpPlayer.paidAbility(self.corpView)

			# 2. Discard Phase ------------------

			# 2.1 discard down to maximum hand size
			self.timing = 'r2.1'
			runnerPlayer.discardDown(self)

			# 2.2 paid ability window
			self.timing = 'r2.2'
			runnerPlayer.paidAbility(self.runnerView)
			corpPlayer.paidAbility(self.corpView)

			# 2.3 turn ends - conditionals are met

		print('Score out! Runner score: ')
		print(self.runnerPoints)
		print('Corp score:')
		print(self.corpPoints)

	# 'view' is a dictionary, containing all information available to playerss
	def commonView(self):
		view = {
			'corpCreds'		:self.corpCreds,
			'runnerCreds'	:self.runnerCreds,
			'turnNumber'	: self.turnNumber,
			'runnerPoints'	: self.runnerPoints,
			'corpPoints'	: self.corpPoints,
			'clicksLeft'	: self.clicksLeft,
			'timing'	: self.timing,
			'stackSize' :len(self.stack),
			'heap'		:self.heap, # cards in the heap are public knowledge
			'gripSize'	:len(self.grip),
			'runnerInstalled' :self.runnerInstalled,
			'RDSize'	:len(self.RD),
			'HQSize'	:len(self.HQ)
			'ArchivesFaceUp' :self.ArchivesFaceUp,
			'archivesFaceDownSize' :len(self.ArchivesFaceDown),
		}

		return view

	def runnerView(self):
		view = self.commonView()
		rezFilter = lambda ice: [(k[1:] if k[-1] =='u' else k[:-1]) for k in ice] # if it's unrezzed, give all but the first letter (it's identity) - if it's rezzed, give everything except the redundant 'r'
		rView = {
			'grip'		: self.grip, #tragically, this is all the hidden info the runner has.
			'protectArchives'	: rezFilter(self.protectArchives),
			'protectHQ'	: rezFilter(self.protectHQ),
			'protectRD'	: rezFilter(self.protectRD),
			'remoteServers'		: [ {'inServer': rezFilter(server['inServer']), 'ice': rezFilter(server['ice'])} for server in self.remoteServers]
		}
		view.update(rView)
		return view

	def corpView(self):
		view = self.commonView()		
		cView = {
			'protectArchives' : self.protectArchives,
			'protectHQ'		: self.protectHQ,
			'protectRD'		: self.protectRD,
			'remoteServers'	: self.remoteServers,
			'HQ'			: self.HQ
		}
		view.update(cView)
		return view


# Initialization thingies ======================================================

def newCorpDeck():
	# provides a freshly shuffled default corp deck - a list of chars
	# The 'top' card is at the front of the list
	# total of 20 cards:
	# a = asset (3)
	# g = agenda (6)
	# b = barrier (3)
	# c = code gate (3)
	# s = sentry (2)
	# o = operation (hedge fund) (3)
	cards = list(3*'a' + 6*'g' + 3*'b' + 3*'c' + 2*'s' + 3*'o')
	random.shuffle(cards)
	return cards

def newRunnerDeck():
	# provides a freshly shuffled default runner deck - a list of chars
	# The 'top' card is at the front of the list
	# total of 16 cards:
	# e = easy mark (5)
	# i = inside job (2)
	# f = fracter (3)
	# d = decoder (3)
	# k = killer (3)
	cards = list(5*'e' + 2*'i' + 3*'f' + 3*'d' + 3*'k')
	random.shuffle(cards)
	return cards


# Conditionals ===============================================================

def beginCorpTurn(game):
	# fire all 'when corp turn begins' conditionals
	numRezzedAssets = [server['inServer'][0] for server in self.remoteServers].count('ar') # count the number of remote servers with a rezzed asset in slot 0
	game.corpCreds += numRezzedAssets
