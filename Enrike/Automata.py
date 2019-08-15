#!python3
class Automata:
	#Constructor
	def __init__(self, states, start, accepted):
		self.states = states 		#States set
		self.start = start 			#Start state
		self.accepted = accepted 	#Accepted state

	def getStates(self):
		return self.states 

	def setStates(self, states):
		self.states = states

	def getStart(self):
		return self.start

	def setStart(self, start):
		self.start = start

	def getAccepted(self):
		return self.accepted

	def setAccepted(self, accepted):
		self.accepted = accepted