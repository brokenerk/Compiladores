#!python3
from State import State
from Transition import Transition
from copy import deepcopy
from collections import deque
epsilon = '\u03B5'
Id = 0

class AFN:
	#Constructor
	def __init__(self, states, alphabet, start, accept):
		global Id
		Id += 1
		self.id = Id 						#Integer
		self.states = states 				#Set<State>
		self.alphabet = alphabet			#Set<Char>
		self.start = start 					#State
		self.accept = accept 				#State

	#Parameters: Nothing
	#Return: Integer
	def getId(self):
		return self.id  
	#Parameters: Integer
	#Return: Nothing
	def setId(self, id):
		self.id = id    

	#Parameters: Nothing
	#Return: Set<States>
	def getStates(self):
		return self.states   
	#Parameters: Set<States>
	#Return: Nothing
	def setStates(self, states):
		self.states = states   

	#Parameters: Nothing
	#Return: Set<Char>
	def getAlphabet(self):
		return self.alphabet   
	#Parameters: Set<Char>
	#Return: Nothing
	def setAlphabet(self, alphabet):
		self.alphabet = alphabet

	#Parameters: Nothing
	#Return: State
	def getStart(self):
		return self.start 
	#Parameters: State
	#Return: Nothing
	def setStart(self, start):
		self.start = start  

	#Parameters: Nothing
	#Return: Set<State>
	def getAccept(self):
		return self.accept 
	#Parameters: State
	#Return: Nothing
	def setAccept(self, accept):
		self.accept = accept

	#Parameters: Nothing
	#Return: Nothing
	def display(self):
		print("Id: {}".format(self.getId()))
		print("Alfabeto: {}".format(self.getAlphabet()))
		print("Estado inicial: {}".format(self.getStart().getId()))
		print("Estado Final: {}".format(self.getAccept().getId()))
		for e in self.states:
			e.displayTransitions()   

	#Parameters: Character
	#Return: AFN
	def createBasic(symbol):
		e1 = State()
		e2 = State()
		t1 = Transition(symbol, e2)
		e1.addTransition(t1)
		states = set([e1, e2])
		alphabet = set([symbol])
		return AFN(states, alphabet, e1, e2)

	#Parameters: Set<States>
	#Return: Set<Char>
	def addNewAlphabet(newStates):
		#Add new alphabet
		newAlphabet = set([])
		for s in newStates:
			for t in s.getTransitions():
				symbol = t.getSymbol()
				#Avoid epsilon
				if(symbol != epsilon):
					newAlphabet.add(symbol)
		return newAlphabet

	#Parameters: Set<States>, Set<States>, State, State
	#Return: Set<States>
	def createNewStates(statesA, statesB, sA, sB):
		newStates = set([])

		for s1, s2 in zip(statesA, statesB):
			if (s1.equals(sA) == False):
				newStates.add(s1)
			if (s2.equals(sB) == False):
				newStates.add(s2)

		return newStates 

	#Parameters: AFN, Integer
	#Return: AFN
	def join(self, afnB):
		#Create a deepcopy of start states from both afns
		startA = deepcopy(self.getStart())
		startB = deepcopy(afnB.getStart())
		#Create a deepcopy of accept states
		acceptA = deepcopy(self.getAccept()) 
		acceptB = deepcopy(afnB.getAccept())     
		#Create new start, accept state and new states set
		newStart = State()
		newAccept = State()
		
		#Add epsilon transitions to new start state
		newStart.addTransition(Transition(epsilon, startA))
		newStart.addTransition(Transition(epsilon, startB))    
		#Add epsilon transition to new accept state
		acceptA.addTransition(Transition(epsilon, newAccept))
		acceptB.addTransition(Transition(epsilon, newAccept))    
		#Add updated "accept" states (no longer accepted), new start and new accept
		newStates = set([newStart, acceptA, acceptB, newAccept])  

		#Add all states to new set, except original accept states
		newStates = newStates.union(AFN.createNewStates(self.getStates(), afnB.getStates(), 
			self.getAccept(), afnB.getAccept()))

		#Free memory
		del startA
		del startB
		del acceptA
		del acceptB

		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, newAccept)   

	#Parameters: AFN, Integer
	#Return: AFN
	def concat(self, afnB):
		#Create a deepcopy of start states from both afns
		startA = deepcopy(self.getStart())
		startB = deepcopy(afnB.getStart())

		#Create a deepcopy of accept states
		acceptA = deepcopy(self.getAccept()) 
		acceptB = deepcopy(afnB.getAccept())  

		#Add AFNB start state's transitions to AFNA accept state
		#Merge states
		for t in startB.getTransitions():
			acceptA.addTransition(t)    
		#Add updated AFNA "accept" state (no longer an accepted state)
		newStates = set([acceptA])    

		#Add all states to new set, 
		#except original AFNA accept state and AFNB start state
		newStates = newStates.union(AFN.createNewStates(self.getStates(), afnB.getStates(), 
			self.getAccept(), afnB.getStart()))

		#Free memory
		del startB
		del acceptA

		return AFN(newStates, AFN.addNewAlphabet(newStates), startA, acceptB)    

	#Parameters: Integer
	#Return: AFN
	def positiveClosure(self):
		#Create new start state
		newStart = State()
		#Create new accept state
		newAccept = State()

		#Create a deepcopy of actual start and accept state
		start = deepcopy(self.getStart())
		accept = deepcopy(self.getAccept()) 

		#Add epsilon transitions
		newStart.addTransition(Transition(epsilon, start))
		accept.addTransition(Transition(epsilon, newAccept))
		accept.addTransition(Transition(epsilon, start))    
		#Add updated states on new set
		newStates = set([newStart, start, accept, newAccept])  

		#Add remaining states to new set
		for s in self.getStates():
			if(s.equals(start) == False and s.equals(accept) == False):
				newStates.add(s) 

		#Free memory
		del start
		del accept 

		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, newAccept)

	#Parameters: Integer
	#Return: AFN
	def kleeneClosure(self):
		#Get positive closure
	    posClosure = self.positiveClosure(); 

		#Just add epsilon transition from start to accept state
	    for s in posClosure.getStates():
		    if(s.equals(posClosure.getStart()) == True):
			    s.addTransition(Transition(epsilon, posClosure.getAccept())) 

	    return posClosure

	#Parameters: Integer
	#Return: AFN
	def optional(self):
		newStart = State()
		newAccept = State()
		start = deepcopy(self.getStart())
		accept = deepcopy(self.getAccept()) 

		newStart.addTransition(Transition(epsilon, start))
		newStart.addTransition(Transition(epsilon, newAccept))
		accept.addTransition(Transition(epsilon, newAccept)) 
		newStates = set([newStart, start, accept, newAccept])  

		for s in self.getStates():
		    if(s.equals(start) == False and s.equals(accept) == False):
		        newStates.add(s)  

		#Free memory
		del start
		del accept

		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, newAccept)

	#Parameters: Set<State>
	#Return: Set<States>
	def epsilonClosure(statesE):
		s = set([]) #Set
		p = deque() #Stack

		for edo in statesE:
			p.append(edo)

		while p:
			e = p.pop()
			if (e in(s)):
				continue
			s.add(e)
			for t in e.getTransitions():
				if (t.getSymbol() == epsilon):
					p.append(t.getNext())
		return s

	def move(states, symbol):
		R = set([])
		for e in states:
			R = R.union(e.move(symbol)) 
		return R 

	def goTo(states, symbol):
		moveStates = AFN.move(states, symbol)
		returnStates = AFN.epsilonClosure(moveStates)
		return returnStates