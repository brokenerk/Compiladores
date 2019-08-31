from collections import deque
epsilon = '\u03B5'

class Sets:
	def __init__(self, afnStates):
		self.afnStates = afnStates

	def searchState(self, id):
		for s in self.afnStates:
			if(s.getId() == id):
				return s

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


	def move(self, states, symbol):
		R = set([])
		for e in states:
			for t in e.getTransitions():
				if(t.getSymbol() == symbol):
					id = t.getNext().getId()
					R.add(self.searchState(id))
		return R

	def goTo(self, states, symbol):
		moveStates = self.move(states, symbol);
		returnStates = set([])
		for e in moveStates:
			returnStates = returnStates.union(self.epsilonClosure(e))

		return returnStates

