#!python3
class AFN:
	#Constructor
	def __init__(self, states, start, accept):
		self.states = states 		#States set
		self.start = start 			#Start state
		self.accept = accept 		#Accepted state

	def getStates(self):
		return self.states 

	def setStates(self, states):
		self.states = states

	def getStart(self):
		return self.start

	def setStart(self, start):
		self.start = start

	def getAccept(self):
		return self.accept

	def setAccept(self, accept):
		self.accept = accept

	#Operations
	#Display states with transitions
	def display(self):
		for s in self.getStates():
			for t in s.getTransitions():
				print(str(s.getId()) + " -- " + t.getCharacter() + " ---> " + str(t.getNext().getId()))

		print("Estado inicial: " + str(self.start.getId()))
		print("Estado aceptado: " + str(self.accept.getId()))
