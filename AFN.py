#!python3
from State import State
from Transition import Transition
from copy import deepcopy
epsilon = '\u03B5'

class AFN:
	#Constructor
	def __init__(self, states, start, accept):
		self.states = states 		#Set<State>
		self.start = start 			#State
		self.accept = accept 		#State

	#Parameters: Nothing
	#Return: Set<States>
	def getStates(self):
		return self.states 

	#Parameters: Set<States>
	#Return: Nothing
	def setStates(self, states):
		self.states = states

	#Parameters: Nothing
	#Return: State
	def getStart(self):
		return self.start

	#Parameters: State
	#Return: Nothing
	def setStart(self, start):
		self.start = start

	#Parameters: Nothing
	#Return: State
	def getAccept(self):
		return self.accept

	#Parameters: States
	#Return: Nothing
	def setAccept(self, accept):
		self.accept = accept

	#Parameters: Nothing
	#Return: Nothing
	def display(self):
		print("Estado inicial: {}".format(self.getStart().getId()))
		print("Estado Final: {}".format(self.getAccept().getId()))
		for e in self.states:
			e.displayTransitions()
	
	#Parameters: AFN
	#Return: AFN
	def join(self, afnB):
		#Create a deepcopy of start states from both afns
		startA = deepcopy(self.getStart())
		startB = deepcopy(afnB.getStart())
		#Create a deepcopy of accept states
		acceptA = deepcopy(self.getAccept()) 
		acceptB = deepcopy(afnB.getAccept()) 

		#Create new start, accept state and new states set
		newStart = State(0)
		newAccept = State(len(self.getStates()) + len(afnB.getStates()) + 1)
		newStates = set([])

		#Add epsilon transitions to new start state
		newStart.addTransition(Transition(epsilon, startA))
		newStart.addTransition(Transition(epsilon, startB))

		#Add epsilon transition to new accept state
		acceptA.addTransition(Transition(epsilon, newAccept))
		acceptB.addTransition(Transition(epsilon, newAccept))

		#Add all states to new set, except original accept states
		for s1, s2 in zip(self.getStates(), afnB.getStates()):
			if(s1.equals(self.getAccept()) == False):
				newStates.add(s1)
			if(s2.equals(afnB.getAccept()) == False):
				newStates.add(s2)
		
		#Add updated "accept" states (no longer accepted), new start and new accept
		newStates.add(acceptA)
		newStates.add(acceptB)	
		newStates.add(newStart)
		newStates.add(newAccept)

		return AFN(newStates, newStart, newAccept)

	#Parameters: AFN
	#Return: AFN
	def concat(self, afnB):
		#Create a deepcopy of start states from both afns
		startA = deepcopy(self.getStart())
		startB = deepcopy(afnB.getStart())
		#Create a deepcopy of accept states
		acceptA = deepcopy(self.getAccept()) 
		acceptB = deepcopy(afnB.getAccept())
		newStates = set([])

		#Add AFNB start state's transitions to AFNA accept state
		#Merge states
		for t in startB.getTransitions():
			acceptA.addTransition(t)

		#Add all states to new set, 
		#except original AFNA accept state and AFNB start state
		for s1, s2 in zip(self.getStates(), afnB.getStates()):
			if (s1.equals(self.getAccept()) == False):
				newStates.add(s1)
			if (s2.equals(afnB.getStart()) == False):
				newStates.add(s2)

		#Add updated AFNA "accept" state (no longer an accepted state)
		newStates.add(acceptA)

		return AFN(newStates, startA, acceptB)
