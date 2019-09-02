#!python3
from Transition import Transition
Id = 0

class State:
    #Constructor
    def __init__(self, token):
        global Id
        Id += 1
        self.id = Id 					#Integer
        self.transitions = set([]) 		#Set<Transition> 
        #self.token = token 			#Integer

    #Parameters: Nothing
    #Return: Integer
    def getId(self):
    	return self.id  
    #Parameters: Integer
    #Return: Nothing
    def setId(self, id):
    	self.id = id  

    '''
    #Parameters: Nothing
    #Return: Integer
    def getToken(self):
    	return self.token
    #Parameters: Integer
    #Return: Nothing
    def setToken(self, token):
    	self.token = token  
    '''

    #Parameters: Nothing
    #Return: Set<Transition>
    def getTransitions(self):
    	return self.transitions  
    #Parameters: Transition
    #Return: Nothing
    def addTransition(self, t):
        self.transitions.add(t)  

    #Parameters: Nothing
    #Return: Hash
    def hash(self):
    	return hash(self.id)    
    #Parameters: State
    #Return: Boolean
    def equals(self, other):
    	return (self.__class__ == other.__class__ and self.id == other.id)  

    #Parameters: Nothing
    #Return: Nothing
    def displayTransitions(self):
    	for t in self.transitions:
    		print("{} --{}-- > {}".format(self.id, t.getSymbol(), t.getNext().getId())) 