#!python3
from State import State
from Transition import Transition
from copy import deepcopy
epsilon = '\u03B5'

class AFN:
    #Constructor
    def __init__(self, id, states, start, accept):
    	self.id = id 				#Integer
    	self.states = states 		#Set<State>
    	self.start = start 			#State
    	self.accept = accept 		#State    
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
    	print("Id: {}".format(self.getId()))
    	print("Estado inicial: {}".format(self.getStart().getId()))
    	print("Estado Final: {}".format(self.getAccept().getId()))
    	for e in self.states:
    		e.displayTransitions()    
    #Parameters: Id, Symbol
    #Return AFN
    def createBasic(id,symbol):
        e1 = State(id)
        e2 = State(id+1)
        t1 = Transition(symbol,e2)
        e1.addTransition(t1)
        states = set([e1,e2])
        return AFN(id,states,e1,e2)
    
    #Parameters: AFN, Integer
    #Return: AFN
    def join(self, afnB, id):
    	#Create a deepcopy of start states from both afns
    	startA = deepcopy(self.getStart())
    	startB = deepcopy(afnB.getStart())
    	#Create a deepcopy of accept states
    	acceptA = deepcopy(self.getAccept()) 
    	acceptB = deepcopy(afnB.getAccept())     
    	#Create new start, accept state and new states set
    	newStart = State(0)
    	newAccept = State(len(self.getStates()) + len(afnB.getStates()) + 1)
    	
    	#Add epsilon transitions to new start state
    	newStart.addTransition(Transition(epsilon, startA))
    	newStart.addTransition(Transition(epsilon, startB))    
    	#Add epsilon transition to new accept state
    	acceptA.addTransition(Transition(epsilon, newAccept))
    	acceptB.addTransition(Transition(epsilon, newAccept))    
    	#Add updated "accept" states (no longer accepted), new start and new accept
    	newStates = set([newStart, acceptA, acceptB, newAccept])    
    	#Add all states to new set, except original accept states
    	for s1, s2 in zip(self.getStates(), afnB.getStates()):
    		if(s1.equals(self.getAccept()) == False):
    			newStates.add(s1)
    		if(s2.equals(afnB.getAccept()) == False):
    			newStates.add(s2)
    	
    	return AFN(id, newStates, newStart, newAccept)    
    #Parameters: AFN, Integer
    #Return: AFN
    def concat(self, afnB, id):
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
    	#Add updated AFNA "accept" state (no longer an accepted state)
    	newStates = set([acceptA])    
    	#Add all states to new set, 
    	#except original AFNA accept state and AFNB start state
    	for s1, s2 in zip(self.getStates(), afnB.getStates()):
    		if (s1.equals(self.getAccept()) == False):
    			newStates.add(s1)
    		if (s2.equals(afnB.getStart()) == False):
    			newStates.add(s2)    
    	return AFN(id, newStates, startA, acceptB)    
    #Parameters: Integer
    #Return: AFN
    def positiveClosure(self, id):
    	#Create new start state
    	newStart = State(0)
    	#Create new accept state
    	newAccept = State(len(self.getStates()) + 1)
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
    	return AFN(id, newStates, newStart, newAccept)

    #Parameters: Integer
    #Return: AFN
    def kleeneClosure(self, id):
		#Get positive closure
	    posClosure = self.positiveClosure(id);    
		#Just add epsilon transition from start to accept state
	    for s in posClosure.getStates():
		    if(s.equals(posClosure.getStart()) == True):
			    s.addTransition(Transition(epsilon, posClosure.getAccept()))    
	    return posClosure

    def optional(self,id):
        newStart = State(0)
        newAccept = State(len(self.getStates()) + 1)
        start = deepcopy(self.getStart())
        accept = deepcopy(self.getAccept()) 
        newStart.addTransition(Transition(epsilon, start))
        newStart.addTransition(Transition(epsilon, newAccept))
        accept.addTransition(Transition(epsilon, newAccept)) 
        newStates = set([newStart, start, accept, newAccept])    
        for s in self.getStates():
            if(s.equals(start) == False and s.equals(accept) == False):
                newStates.add(s)    
        return AFN(id, newStates, newStart, newAccept)

    def epsilonClosure(self,state):
        S = []
        P = []
        P.append(state)				
        while P != []:
            e = P.pop()
            if e in(S):
                continue
            S.append(e)
            for t in e.getTransitions():
                if  t.getSymbol() == epsilon:
                    P.append(t.getNext())
        return S

    def epsilonClosureS(statesE):
        S = []
        P = []
        for e in statesE:
            P.append(e)				
        while P != []:
            e = P.pop()
            if e in(S):
                continue
            S.append(e)
            for t in e.getTransitions():
                if  t.getSymbol() == epsilon:
                    P.append(t.getNext())
        return S
    
    def move (states,symbol):
        R = []
        for e in states:
            R.append(State.move(e,symbol))
        return R 

    def goTo (states,symbol):
        return AFN.epsilonClosureS(AFN.move(states,symbol))