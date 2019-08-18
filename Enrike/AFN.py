#!python3
from State import State
from Transition import Transition
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

	#Union of 2 afns
	def join(self, afnB):
		#Get state sets
		statesA = self.getStates().copy()
		statesB = afnB.getStates().copy()
		#Get start states from both afns
		startA = self.getStart()
		startB = afnB.getStart()
		#Get accept states
		acceptA = State(self.getAccept().getId()) #Create new state object, 
		acceptB = State(afnB.getAccept().getId()) #to avoid modifications on original afns
		#Create new start, accept state and new states set
		newStart = State(-1)
		newAccept = State(0)
		newStates = set([])

		#Add epsilon transitions to new start state
		newStart.addTransition(Transition('E', startA))
		newStart.addTransition(Transition('E', startB))

		#Add epsilon transition to new accept state
		acceptA.addTransition(Transition('E', newAccept))
		acceptB.addTransition(Transition('E', newAccept))

		#Add all states to new set, except original accept states
		for s1, s2 in zip(statesA, statesB):
			if(s1.equals(acceptA) == False):
				newStates.add(s1)

			if(s2.equals(acceptB) == False):
				newStates.add(s2)
		
		#Add updated accept states, new start and new accept
		newStates.add(acceptA)
		newStates.add(acceptB)	
		newStates.add(newStart)
		newStates.add(newAccept)

		return AFN(newStates, newStart, newAccept)
