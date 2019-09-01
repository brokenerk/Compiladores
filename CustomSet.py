from collections import deque
epsilon = '\u03B5'

class CustomSet:
	def __init__(self, afnStates):
		self.afnStates = afnStates

	#Parameters: Integer
	#Return: State
	def searchState(self, id):
		for e in self.afnStates:
			if(e.getId() == id):
				return e

	#Parameters: List<Set>, Set
	#Return: Boolean
	def exists(self, list, s):
		for i in list:
			if(i == s):
				return True
		return False

	#Parameters: State
	#Return: Set<State>
	def epsilonClosure(self, edo):
		s = set([]) #Set
		p = deque() #Stack
		p.append(edo)

		while p:
			e = p.pop()

			if(e in(s)):
				continue
			s.add(e)

			for t in e.getTransitions():
				if (t.getSymbol() == epsilon):
					id = t.getNext().getId()
					p.append(self.searchState(id))
		return s

	#Parameters: Set<State>, Char
	#Return: Set<State>
	def move(self, states, symbol):
		R = set([])
		for e in states:
			for t in e.getTransitions():
				if(t.getSymbol() == symbol):
					id = t.getNext().getId()
					R.add(self.searchState(id))
		return R

	#Parameters: Set<State>, Char
	#Return: Set<State>
	def goTo(self, states, symbol):
		moveStates = self.move(states, symbol);
		returnStates = set([])
		for e in moveStates:
			returnStates = returnStates.union(self.epsilonClosure(e))
		return returnStates