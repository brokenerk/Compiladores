#!python3
from State import State
from Transition import Transition
from DFA import DFA
from copy import deepcopy
from multipledispatch import dispatch
from collections import deque

epsilon = '\u03B5'
Id = 0

class NFA:
	#Constructor
	def __init__(self, states, alphabet, start, accepts):
		global Id
		Id += 1
		self.id = Id 						#Integer
		self.states = states 				#Set<State>
		self.statesList = [] 				#List<States>
		self.alphabet = alphabet			#Set<Char>
		self.start = start 					#State
		self.accepts = accepts 				#Set<State>

	#Parameters: Nothing
	#Return: Nothing
	def resetId():
		State.restartId()
		global Id 
		Id = 0

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
		return sorted(self.alphabet)   
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
	def getAccepts(self):
		return self.accepts 
	#Parameters: State
	#Return: Nothing
	def addAccept(self, a):
		self.accepts.add(a)

	#Parameters: Nothing
	#Return: Nothing
	def display(self):
		print("Id: {}".format(self.id))
		print("Alfabeto: {}".format(self.alphabet))
		print("Estado inicial: {}".format(self.start.getId()))
		print("Estados Finales: ", end = '')
		for a in self.accepts:
			print("{}, ".format(a.getId()), end = '')
		print("")

		for e in self.states:
			e.displayTransitions()   

	#Parameters: Character
	#Return: NFA
	@dispatch(str)
	def createBasic(symbol):
		e1 = State()
		e2 = State()
		t1 = Transition(symbol, e2)
		e1.addTransition(t1)
		states = set([e1, e2])
		alphabet = set([symbol])
		return NFA(states, alphabet, e1, set([e2]))

	#Parameters: Character, Character
	#Return: NFA
	@dispatch(str, str)
	def createBasic(symbol, endSymbol):
		e1 = State()
		e2 = State()
		t1 = Transition(symbol, endSymbol, e2)
		e1.addTransition(t1)
		states = set([e1, e2])
		alphabet = set([symbol + '-' + endSymbol])
		return NFA(states, alphabet, e1, set([e2]))

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
					if (t.getEndSymbol() == None):
						newAlphabet.add(symbol)
					else:
						end = t.getEndSymbol()
						newAlphabet.add(symbol + '-' + end)
		return sorted(newAlphabet)

	#Parameters: Set<NFA>
	#Return: NFA
	def specialJoin(nfas):
		newStart = State()
		newStates = set([])
		accepts = set([])

		for nfa in nfas:
			start = deepcopy(nfa.getStart())
			newStart.addTransition(Transition(epsilon, start))
			for e in nfa.getAccepts():
				accepts.add(e)
			newStates = newStates.union(nfa.getStates())
			del start

		newStates.add(newStart)
		return NFA(newStates, NFA.addNewAlphabet(newStates), newStart, accepts)

	#Parameters: NFA
	#Return: NFA
	def join(self, nfaB):
		#Create a deepcopy of start states from both NFAs
		startA = deepcopy(self.start)
		startB = deepcopy(nfaB.getStart())
		#Create a deepcopy of accept states
		acceptsA = deepcopy(self.accepts) 
		acceptsB = deepcopy(nfaB.getAccepts())     
		#Create new start, accept state and new states set
		newStart = State()
		newAccept = State()
		
		#Add epsilon transitions to new start state
		newStart.addTransition(Transition(epsilon, startA))
		newStart.addTransition(Transition(epsilon, startB))    
		#Add epsilon transition to new accept state
		for a in acceptsA:
			a.setToken(-1)
			a.addTransition(Transition(epsilon, newAccept))

		for b in acceptsB:
			b.setToken(-1)
			b.addTransition(Transition(epsilon, newAccept)) 

		#Add updated "accept" states (no longer accepted), new start and new accept
		newStates = set([newStart, newAccept])

		for a in acceptsA:
			newStates.add(a)

		for b in acceptsB:
			newStates.add(b)

		#Add the remaining states
		for e1 in self.states:
			for a in self.accepts:
				if(e1.equals(a) == False):
					newStates.add(e1)

		for e2 in nfaB.getStates():
			for b in nfaB.getAccepts():
				if(e2.equals(b) == False):
					newStates.add(e2)

		#Free memory
		del startA
		del startB
		del acceptsA
		del acceptsB
		return NFA(newStates, NFA.addNewAlphabet(newStates), newStart, set([newAccept]))   

	#Parameters: NFA
	#Return: NFA
	def concat(self, nfaB):
		#Create a deepcopy of start states from both NFAs
		startA = deepcopy(self.start)
		startB = deepcopy(nfaB.getStart())

		#Create a deepcopy of accept states
		acceptsA = deepcopy(self.accepts) 
		acceptsB = deepcopy(nfaB.getAccepts())  

		#Add NFAB start state's transitions to NFAA accept state
		#Merge states
		for t in startB.getTransitions():
			for a in acceptsA:
				a.setToken(-1)
				a.addTransition(t)    

		#Add updated NFAA "accept" state (no longer an accepted state)
		newStates = set([])
		for a in acceptsA:
			newStates.add(a)

		#Add all states to new set, 
		#except original NFAA accept state and NFAB start state
		for e1 in self.states:
			for a in self.accepts:
				if(e1.equals(a) == False):
					newStates.add(e1)

		for e2 in nfaB.getStates():
			if(e2.equals(nfaB.getStart()) == False):
				newStates.add(e2)

		#Free memory
		del startB
		del acceptsA
		return NFA(newStates, NFA.addNewAlphabet(newStates), startA, acceptsB)    

	#Parameters: Nothing
	#Return: NFA
	def positiveClosure(self):
		#Create new start state
		newStart = State()
		#Create new accept state
		newAccept = State()

		#Create a deepcopy of actual start and accept state
		start = deepcopy(self.start)
		accepts = deepcopy(self.accepts) 

		#Add epsilon transitions
		newStart.addTransition(Transition(epsilon, start))

		for a in accepts:
			a.setToken(-1)
			a.addTransition(Transition(epsilon, newAccept))
			a.addTransition(Transition(epsilon, start))

		#Add updated states on new set
		newStates = set([newStart, start, newAccept])  

		for a in accepts:
			newStates.add(a)

		#Add remaining states to new set
		for s in self.states:
			if(s.equals(start) == False):
				for a in self.accepts:
					if(s.equals(a) == False):
						newStates.add(s) 

		#Free memory
		del start
		del accepts 
		return NFA(newStates, NFA.addNewAlphabet(newStates), newStart, set([newAccept]))

	#Parameters: Nothing
	#Return: NFA
	def kleeneClosure(self):
		#Get positive closure
	    posClosure = self.positiveClosure()

		#Just add epsilon transition from start to accept state
	    for s in posClosure.getStates():
		    if(s.equals(posClosure.getStart()) == True):
		    	for a in posClosure.getAccepts():
			    	s.addTransition(Transition(epsilon, a)) 
	    return posClosure

	#Parameters: Nothing
	#Return: NFA
	def optional(self):
		newStart = State()
		newAccept = State()
		start = deepcopy(self.start)
		accepts = deepcopy(self.accepts) 

		newStart.addTransition(Transition(epsilon, start))
		newStart.addTransition(Transition(epsilon, newAccept))

		for a in accepts:
			a.setToken(-1)
			a.addTransition(Transition(epsilon, newAccept)) 

		newStates = set([newStart, start, newAccept])

		for a in accepts:
			newStates.add(a)  

		for s in self.states:
			if(s.equals(start) == False):
				for a in self.accepts:
					if(s.equals(a) == False):
						newStates.add(s)

		#Free memory
		del start
		del accepts
		return NFA(newStates, NFA.addNewAlphabet(newStates), newStart, set([newAccept]))
	
	#Parameters: Integer
	#Return: Nothing
	def setToken(self, token):
		for e in self.accepts:
			e.setToken(int(token))

	#Parameters: Integer
	#Return: State
	def searchState(self, id):
		#Binary search
		n = len(self.states)
		inf = 0
		sup = n - 1
		center = 0

		while inf <= sup:
			center = int(((sup + inf) / 2))
			if(self.statesList[center].getId() == id):
				return self.statesList[center]
			elif(id < self.statesList[center].getId()):
				sup = center - 1
			else:
				inf = center + 1

	#Parameters: State
	#Return: Set<State>
	def epsilonClosure(self, state):
		s = set([]) #Set
		p = deque() #Stack
		p.append(state)

		while p:
			e = p.pop()

			if(e in(s)):
				continue
			s.add(e)

			for t in e.getTransitions():
				if (t.getSymbol() == epsilon):
					id = t.getNext().getId()	#Search by Id
					p.append(self.searchState(id))
		return s

	#Parameters: Set<State>, Char
	#Return: Set<State>
	@dispatch(object, str)
	def move(self, states, symbol):
		R = set([])
		for e in states:
			for t in e.getTransitions():
				if(t.getSymbol() == symbol):
					id = t.getNext().getId()	#Search by Id
					R.add(self.searchState(id))
		return R

	#Parameters: Set<State>, Char , Char
	#Return: Set<State>
	@dispatch(object, str, str)
	def move(self, states, symbol, endSymbol):
		R = set([])
		for e in states:
			for t in e.getTransitions():
				if(symbol == t.getSymbol() and t.getEndSymbol() == endSymbol):
					id = t.getNext().getId()	#Search by Id
					R.add(self.searchState(id))
		return R

	#Parameters: Set<State>, Char
	#Return: Set<State>
	@dispatch(set, str)
	def goTo(self, states, symbol):
		moveStates = self.move(states, symbol)
		returnStates = set([])
		for e in moveStates:
			returnStates = returnStates.union(self.epsilonClosure(e))
		return returnStates

	#Parameters: Set<State>, Char , Char
	#Return: Set<State>
	@dispatch(set, str, str)
	def goTo(self, states, symbol, endSymbol):
		moveStates = self.move(states, symbol, endSymbol)
		returnStates = set([])
		for e in moveStates:
			returnStates = returnStates.union(self.epsilonClosure(e))
		return returnStates

	#Parameters: List<Set>, Set
	#Return: Integer
	def exists(self, list, s):
		list.sort() 	#Sort sets list first
		#Iterate the list
		for i in range(0, len(list)):
			#If the set exists in list, we return the set Id
			if(list[i] == s):
				return i
		#If not, there's a new set
		return -1

	#Parameters: CustomSet
	#Return: DFA
	def convertToDFA(self):
		self.statesList = sorted(self.states, key=lambda edo: edo.getId()) #Sort states
		S0 = self.epsilonClosure(self.start)
		queue = [S0] 		#Queue<Set>
		list = [S0] 		#List<Set>
		table = []			#List<List>
		cont = 0

		while queue:
			Si = queue.pop(0)					#Get first enter
			row = []							#Row - List

			#Iterate over the alphabet
			for symbol in self.alphabet:
				#Apply goTo function to the popped set
				if(len(symbol) > 1):
					aux = self.goTo(Si, symbol[0], symbol[2])
				else:
					aux = self.goTo(Si, symbol)

				#Set is empty, we append -1 to the row
				if(aux == set()):
					row.append(-1)
					continue

				#Verify is set already exists in list
				nSet = self.exists(list, aux)
				#If it exists, we need to add their Id on the row
				if(nSet != -1):
					row.append(nSet)
					continue

				#The set is new, so we incremente the Id and add it to the row
				cont += 1
				row.append(cont)
				#Add new set to the end of the queue
				queue.append(aux)
				#Add the new set to the list
				list.append(aux)

			#Check tokens in accepted states
			tok = -1
			for e1 in Si:
				for e2 in self.accepts:
					if(e1.equals(e2) == True):
						tok = e2.getToken()
						break
	
			#Add the token to the row
			row.append(tok)
			#Finally, add the row w data to the table
			table.append(row)

		#Free memory
		del S0
		del queue
		del list
		del cont
		del row
		del Si
		del aux
		self.statesList = []
		return DFA(table, self.alphabet)