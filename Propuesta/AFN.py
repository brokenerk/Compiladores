#!python3
from State import State
from Transition import Transition
class AFN:
    def __init__(self, states,start, accept):
        self.states = states 
        self.start = start
        self.accept = accept

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


    def displayAfn(self):
	    print("Estado inicial: {}".format( self.getStart().getId() ) )
	    print("Estado Final: {}".format( self.getAccept().getId() ) )
	    for e in self.states:
	        e.displayTransition()

    


        
