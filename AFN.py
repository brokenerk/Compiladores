#!python3
from State import State
from Transition import Transition
#from AFD import AFD
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
		for s1 in self.getStates():
			if (s1.equals(self.getAccept()) == False):
				newStates.add(s1)

		for s2 in afnB.getStates():
			if (s2.equals(afnB.getAccept()) == False):
				newStates.add(s2)

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
		for s1 in self.getStates():
			if (s1.equals(self.getAccept()) == False):
				newStates.add(s1)

		for s2 in afnB.getStates():
			if (s2.equals(afnB.getStart()) == False):
				newStates.add(s2)

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
	def epsilonClosure(self,edo):
		s = [] #Set
		p = deque() #Stack
		p.append(edo)
		while p:
			e = p.pop()
			if (e in(s)):
				continue
			s.append(e)
			for t in e.getTransitions():
				if (t.getSymbol() == epsilon):
					p.append(t.getNext())
		return s

	def move(self,states, symbol):
		R = set([])
		for e in states:
			R = R.union(e.move(symbol)) 
		return R 

	def goTo(self,states, symbol):
		returnStates = []
		returnAux=[]
		#print(states)
		moveStates = self.move(states,symbol)
		if moveStates != set():
			for e in moveStates:
				returnStates.append(self.epsilonClosure(e))
			return returnStates
		return set()

	def afd(self):
		S = []
		newStates = []
		aux = []
		table = []
		start = self.getStart()
		S0 = self.epsilonClosure( start )
		S.append(S0)
		for symbol in self.getAlphabet(): 
				aux = self.goTo(S0,symbol)
				if aux in(S) or aux == set():
					continue
				S.append(aux[0])
		
		aux = [" "]
		for l in self.getAlphabet():
			aux.append(l)
		table.append(aux)
		for Si in S:
			row=[]
			origin=S.index(Si)
			row.append(origin)
			for symbol in self.getAlphabet():
				aux = self.goTo(S0,symbol)
				for e in aux:
					for el in e:
						print("aux: {}".format(el.getId()))
				if aux == set():
					row.append('-1')
					continue
				elif (aux in S):
					target=S.index(aux)
					row.append(target)
				else:
					print("Not Found")
			if (self.getAccept in Si):
				row.append('25')
			table.append(row)

		print(table)
		
		for Si in S:
			for e in Si:
				print("Es: {}".format(e.getId()))
		#return AFD (S,self.getAlphabet)