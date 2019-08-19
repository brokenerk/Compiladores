#!python3
from Transition import Transition
class State:
    def __init__(self, id,):
        self.id = id
        self.transitions = set([])

    def getId(self):
	    return self.id

    def setId(self, id):
	    self.id = id

    def getTransitions(self):
	    return self.transitions
    
    def addTransition(self, t):
	    self.transitions.add(t)
	
    def displayTransition(self):
        for t in self.transitions:
	        print ("{} --{}-- > {}".format(self.id, t.getSymbol() , t.getNext().getId()) )