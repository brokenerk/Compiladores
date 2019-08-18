#!python3
class State:
	#Constructor - self = this
	def __init__(self, id):
		self.id = id 					#Identificator
		self.transitions = set([]) 		#Transitions set
		self.visited = False 			#Visited yet?

	def getId(self):
		return self.id

	def setId(self, id):
		self.id = id

	def getTransitions(self):
		return self.transitions

	def setTransitions(self, transitions):
		self.transitions = transitions

	def getVisited(self):
		return self.visited

	def setVisited(self, visited):
		self.visited = visited

	#IMPORTANT: Hash and equals to compare objects of the state class
	def hash(self):
		return hash(self.id)

	def equals(self, other):
 		return (self.__class__ == other.__class__ and self.id == other.id)

	#Operations
	def addTransition(self, t):
		self.transitions.add(t)




