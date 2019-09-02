#!python3
from State import State
from Transition import Transition
from AFD import AFD
from CustomSet import CustomSet
from copy import deepcopy
epsilon = '\u03B5'
Id = 0
noAccepted = -1

class AFN:
	#Constructor
	def __init__(self, states, alphabet, start, accepts):
		global Id
		Id += 1
		self.id = Id 						#Integer
		self.states = states 				#Set<State>
		self.alphabet = alphabet			#Set<Char>
		self.start = start 					#State
		self.accepts = accepts 				#Set<State>
		#self.tokens = tokens 				#Set<Integer

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
		print("Id: {}".format(self.getId()))
		print("Alfabeto: {}".format(self.getAlphabet()))
		print("Estado inicial: {}".format(self.getStart().getId()))
		print("Estados Finales: ")
		for a in self.getAccepts():
			print("{} ".format(a.getId()))
		for e in self.states:
			e.displayTransitions()   

	#Parameters: Character
	#Return: AFN
	def createBasic(symbol):
		e1 = State( )
		e2 = State( )
		t1 = Transition(symbol, e2)
		e1.addTransition(t1)
		states = set([e1, e2])
		alphabet = set([symbol])
		return AFN(states, alphabet, e1, set([e2]))

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
		return sorted(newAlphabet)

	#Parameters: Set<AFN>
	#Return: AFN
	def addNewStart(afns):
		newStart = State( )
		newStates = set([])
		accepts = set([])

		for afn in afns:
			start = deepcopy(afn.getStart())
			newStart.addTransition(Transition(epsilon, start))
			for e in afn.getAccepts():
				accepts.add(e)
			newStates = newStates.union(afn.getStates())
			del start

		newStates.add(newStart)
		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, accepts)

	#Parameters: AFN
	#Return: AFN
	def join(self, afnB):
		#Create a deepcopy of start states from both afns
		startA = deepcopy(self.getStart())
		startB = deepcopy(afnB.getStart())
		#Create a deepcopy of accept states
		acceptsA = deepcopy(self.getAccepts()) 
		acceptsB = deepcopy(afnB.getAccepts())     
		#Create new start, accept state and new states set
		newStart = State( )
		newAccept = State( )
		
		#Add epsilon transitions to new start state
		newStart.addTransition(Transition(epsilon, startA))
		newStart.addTransition(Transition(epsilon, startB))    
		#Add epsilon transition to new accept state
		for a in acceptsA:
			a.addTransition(Transition(epsilon, newAccept))

		for b in acceptsB:
			b.addTransition(Transition(epsilon, newAccept)) 

		#Add updated "accept" states (no longer accepted), new start and new accept
		newStates = set([newStart, newAccept])

		for a in acceptsA:
			newStates.add(a)

		for b in acceptsB:
			newStates.add(b)

		#Add the remaining states
		for e1 in self.getStates():
			for a in self.getAccepts():
				if(e1.equals(a) == False):
					newStates.add(e1)

		for e2 in afnB.getStates():
			for b in afnB.getAccepts():
				if(e2.equals(b) == False):
					newStates.add(e2)

		#Free memory
		del startA
		del startB
		del acceptsA
		del acceptsB
		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, set([newAccept]))   

	#Parameters: AFN
	#Return: AFN
	def concat(self, afnB):
		#Create a deepcopy of start states from both afns
		startA = deepcopy(self.getStart())
		startB = deepcopy(afnB.getStart())

		#Create a deepcopy of accept states
		acceptsA = deepcopy(self.getAccepts()) 
		acceptsB = deepcopy(afnB.getAccepts())  

		#Add AFNB start state's transitions to AFNA accept state
		#Merge states
		for t in startB.getTransitions():
			for a in acceptsA:
				a.addTransition(t)    

		#Add updated AFNA "accept" state (no longer an accepted state)
		newStates = set([])
		for a in acceptsA:
			newStates.add(a)

		#Add all states to new set, 
		#except original AFNA accept state and AFNB start state
		for e1 in self.getStates():
			for a in self.getAccepts():
				if(e1.equals(a) == False):
					newStates.add(e1)

		for e2 in afnB.getStates():
			if(e2.equals(afnB.getStart()) == False):
				newStates.add(e2)

		#Free memory
		del startB
		del acceptsA
		return AFN(newStates, AFN.addNewAlphabet(newStates), startA, acceptsB)    

	#Parameters: Nothing
	#Return: AFN
	def positiveClosure(self):
		#Create new start state
		newStart = State( )
		#Create new accept state
		newAccept = State( )

		#Create a deepcopy of actual start and accept state
		start = deepcopy(self.getStart())
		accepts = deepcopy(self.getAccepts()) 

		#Add epsilon transitions
		newStart.addTransition(Transition(epsilon, start))
		for a in accepts:
			a.setToken ( noAccepted )
			a.addTransition(Transition(epsilon, newAccept))
			a.addTransition(Transition(epsilon, start))

		#Add updated states on new set
		newStates = set([newStart, start, newAccept])  
		for a in accepts:
			newStates.add(a)

		#Add remaining states to new set
		for s in self.getStates():
			if(s.equals(start) == False):
				for a in self.getAccepts():
					if(s.equals(a) == False):
						newStates.add(s) 

		#Free memory
		del start
		del accepts 
		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, set([newAccept]))

	#Parameters: Nothing
	#Return: AFN
	def kleeneClosure(self):
		#Get positive closure
	    posClosure = self.positiveClosure(); 

		#Just add epsilon transition from start to accept state
	    for s in posClosure.getStates():
		    if(s.equals(posClosure.getStart()) == True):
		    	for a in posClosure.getAccepts():
			    	s.addTransition(Transition(epsilon, a)) 
	    return posClosure

	#Parameters: Nothing
	#Return: AFN
	def optional(self):
		newStart = State( )
		newAccept = State( )
		start = deepcopy(self.getStart())
		accepts = deepcopy(self.getAccepts()) 

		newStart.addTransition(Transition(epsilon, start))
		newStart.addTransition(Transition(epsilon, newAccept))
		for a in accepts:
			a.setToken( noAccepted )
			a.addTransition(Transition(epsilon, newAccept)) 
		newStates = set([newStart, start, newAccept])
		for a in accepts:
			newStates.add(a)  

		for s in self.getStates():
			if(s.equals(start) == False):
				for a in self.getAccepts():
					if(s.equals(a) == False):
						newStates.add(s)

		#Free memory
		del start
		del accepts
		return AFN(newStates, AFN.addNewAlphabet(newStates), newStart, set([newAccept]))
	
	#Parameters: Token
	#Return: Nothing
	def setToken(self,token):
		statesAceppted = self.getAccepts()
		for e in statesAceppted:
			e.setToken(token)

	#Parameters: CustomSet
	#Return: AFD
	def convertToAFD(self, setsUtil):
		S0 = setsUtil.epsilonClosure(self.getStart())
		queue = [S0] 		#Queue<Set>
		list = [S0] 		#List<Set>
		table = []			#List<List>
		cont = 0
		tok = -1

		while queue:
			Si = queue.pop(0)					#Get first enter
			row = []							#Row - List

			#Iterate over the alphabet
			for symbol in self.getAlphabet():
				#Apply goTo function to the popped set
				aux = setsUtil.goTo(Si, symbol)

				#Set is empty, we append -1 to the row
				if(aux == set()):
					row.append(-1)
					continue

				#Verify is set already exists in list
				nSet = setsUtil.exists(list, aux)
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

			
			#Check if there's an accept state in the new set
			for e1 in self.getAccepts():
				for e2 in aux:
					if(e1.equals(e2) == True):
						tok = e1.getToken()
						break

			#Add the result to the row
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
		return AFD(table, self.getAlphabet());