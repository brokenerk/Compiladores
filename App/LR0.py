#!python3
from Node import Node
from copy import deepcopy
epsilon = '\u03B5'

class LR0:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 				#List<Node>
		self.table = []  				#List<List>
		self.analysisTable = []			#List<List>
		self.terminals = set([])		#Set<String>
		self.noTerminals = set([])		#Set<String>
		self.states = [] 				#List<List<Node>>
		self.visitedRules = set([]) 	#Set<List<Node>>

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill set of no terminals symbols
	def setNoTerminals(self):
		for i in range(0, len(self.rules)):
			self.noTerminals.add(self.rules[i].getSymbol()) 
			
	#Parameters: Nothing
	#Return: Nothing 
	#Note: Fill set of terminal symbols
	def setTerminals(self):
		for i in range(0, len(self.rules)):
			next = self.rules[i].getNext()
			while(next != None):
				st = next.getSymbol()
				if st not in self.noTerminals:
					self.terminals.add(st)
				next = next.getNext()

	#Parameters: Symbol
	#Return: List<Node>
	def searchRule(self, symbol):
		listRules = []
		for rule in self.rules:
			if(rule.getSymbol() == symbol):
				if(rule not in self.visitedRules):
					self.visitedRules.add(rule)
					listRules.append(rule)	
		return listRules

	#Parameters: Symbol, Set<List<Node>>
	#Return: List<String>
	def getSymbolItems(self, state):
		symbolItems = set([])
		for rule in state:
			next = rule.getNext()
			while(next != None):
				if(next.getPointBefore()):
					symbolItems.add(next.getSymbol())
				next = next.getNext()
		l = list(symbolItems)
		l.sort()
		return l

	#Parameters: Set<List<Node>>
	#Return: Boolean
	def exists(self, s):
		self.states.sort() 	#Sort sets list first
		#Iterate the list
		for i in range(0, len(self.states)):
			#If the set exists in list, we return True
			if(self.states[i] == s):
				return True
		#If not, there's a new set
		return False

	#Parametes: List<Node>
	#Return: Set<List<Node>>
	def itemClosure(self, rule):
		s = set([rule])
		next = rule.getNext()

		while(next != None):
			if(next.getPointBefore()):
				if(next.getSymbol() in self.noTerminals):
					nextRules = self.searchRule(next.getSymbol())
					for r in nextRules:
						r.getNext().setPointBefore(True)
						s = s.union(self.itemClosure(r))
			next = next.getNext()
		return s

	#Parametes: Set<Node>, String
	#Return: Set<Node>
	def move(self, state, symbol):
		s = set([])
		for rule in state:
			next = rule.getNext()
			while(next != None):
				if(next.getSymbol() == symbol and next.getPointBefore() == True):
					next.setPointBefore(False)
					n = next.getNext()
					if(n != None):
						n.setPointBefore(True)
					else:
						next.setPointAfter(True)

					s.add(rule)
				next = next.getNext()
		return s

	#Parametes: Set<Node>, String
	#Return: Set<Node>
	def goTo(self, state, symbol):
		moveStates = self.move(state, symbol)
		returnStates = set([])
		for e in moveStates:
			returnStates = returnStates.union(self.itemClosure(e))
		return returnStates

	#Parameters: Nothing
	#Return: Nothing
	#Note: Generate the states for the displacements on the relations table
	def calculateStates(self):
		self.setNoTerminals()
		self.setTerminals()
		firstRule = self.rules[0]
		firstRule.getNext().setPointBefore(True)
		S0 = self.itemClosure(firstRule)
		queue = [S0] 		#Queue<Set>
		self.states.append(S0)
		cont = 1

		print("")
		print("S0")
		for rule in S0:
			rule.displayItems()

		while queue:
			Si = deepcopy(queue.pop(0)) 	#Get first enter
			symbolItems = self.getSymbolItems(Si)
			

			#Iterate over the item symbols
			for symbol in symbolItems:
				self.visitedRules = set([])
				aux = self.goTo(Si, symbol)

				#Set is empty, do nothing
				if(aux == set()):
					continue

				#Verify is set already exists in list
				nSet = self.exists(aux)
				#If it exists, do nothing
				if(nSet == True):
					continue

				#Add new set to the end of the queue
				queue.append(aux)
				#Add the new set to the list
				self.states.append(aux)

				print("")
				print(symbol + " --- S" + str(cont))
				for rule in aux:
					rule.displayItems()
				cont += 1