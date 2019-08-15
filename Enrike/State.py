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




