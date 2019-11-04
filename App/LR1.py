#!python3
from Node import Node
from copy import deepcopy
epsilon = '\u03B5'

class LR1:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 				#List<Node>
		self.table = []  				#List<List>
		self.analysisTable = []			#List<List>
		self.terminals = set([])		#Set<String>
		self.noTerminals = set([])		#Set<String>
		self.itemSets = [] 				#List<(List<Node>, Set<String>)>
		self.visitedRules = set([]) 	#Set<List<Node>>
		self.ruleSymbols = set([]) 		#Set<String>

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

	#Parameters: Terminals or No terminals symbols
	#Return: Set of terminals or Epsilon
	def first(self, symbol):
		c = set() 	#Set<>
		if symbol == epsilon:
			c.add(symbol)
		if symbol in self.terminals:
			c.add(symbol)
		if symbol == None:
			c.add("$")
		else:
			for j in range(0, len(self.rules)):
				if symbol == self.rules[j].getSymbol():
					c = c.union(self.first(self.rules[j].getNext().getSymbol()))
		return  c

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
				if(next.getPointBefore() and next.getSymbol() != "epsilon"):
					symbolItems.add(next.getSymbol())
				next = next.getNext()
		l = list(symbolItems)
		l.sort()
		return l

	#Parameters: Set<List<Node>>
	#Return: Boolean
	def exists(self, s1):
		#Iterate the item sets
		for s2 in self.itemSets:
			cont1 = 0
			cont2 = 0
			for r1, r2 in zip(s1, s2):
				#If a rule matches, increment cont2
				if(r1.equals(r2) == True):
					cont2 += 1
				cont1 += 1
			#If both conts are the same, it means that item set s1 was already calculated (exists)
			if(cont1 == cont2):
				return True
		#If both conts never matched, it's a new item set
		return False

	def calculateSymbols(self, rule):
		n = rule.getNext().getNext()

		if(n != None):
			symbolFirst = n.getSymbol()
			if(symbolFirst in self.terminals):
				self.ruleSymbols = self.ruleSymbols.union(self.first(symbolFirst))
			else:
				self.ruleSymbols = self.ruleSymbols.union(set(["$"]))
		else:
			self.ruleSymbols = self.ruleSymbols.union(set(["$"]))

		#rule.setLR1Symbols(self.ruleSymbols)
		#return rule

	#Parametes: List<Node>
	#Return: Set<List<Node>>
	def itemClosure(self, rule):
		s = set([rule])
		next = rule.getNext()
		print(str(self.ruleSymbols))

		while(next != None):
			if(next.getPointBefore()):
				n = next.getNext()
				self.calculateSymbols(rule)
				if(next.getSymbol() in self.noTerminals):
					nextRules = self.searchRule(next.getSymbol())

					for r in nextRules:
						#self.ruleSymbols = set([])
						#self.calculateSymbols(r)

						r.getNext().setPointBefore(True)
						s = s.union(self.itemClosure(deepcopy(r)))

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
			symbols = self.dpFollow[e.getSymbol()]
			returnStates = returnStates.union(self.itemClosure(e, symbols))
		return returnStates

	#Parameters: Nothing
	#Return: Nothing
	#Note: Generate the states for the displacements on the relations table
	def generateItemSets(self):
		self.setNoTerminals()
		self.setTerminals()

		firstRule = self.rules[0]
		firstRule.getNext().setPointBefore(True)
		
		#self.ruleSymbols = self.ruleSymbols.union(set(["$"]))
		#firstRule.setLR1Symbols(self.ruleSymbols)
		S0 = self.itemClosure(firstRule)
		#Sort S0 rules
		S0 = sorted(S0, key = lambda rule0: (rule0.getSymbol(), rule0.getNext().getSymbol(), rule0.getNext().getPointBefore())) 

		#queue = [S0] 	#Queue<Set>
		#self.itemSets.append(S0) 	#List<List<Node>>
		cont = 1

		print("")
		print("S0")
		for rule in S0:
			rule.displayItems()
			print(str(rule.getLR1Symbols()))

		'''
		while queue:
			Si = queue.pop(0) 	#Get first enter
			symbolItems = self.getSymbolItems(Si)
			#Iterate over the item symbols
			for symbol in symbolItems:
				self.visitedRules = set([])
				aux = self.goTo(deepcopy(Si), symbol)

				#Set is empty, do nothing
				if(aux == set()):
					continue

				#Sort aux rules
				aux = sorted(aux, key = lambda rule: (rule.getSymbol(), rule.getNext().getSymbol(), rule.getNext().getPointBefore())) 
				#Verify is set already exists in list
				if(self.exists(aux) == True):
					continue

				#Add new set to the end of the queue
				queue.append(aux)
				#Add the new set to the list
				self.itemSets.append(aux)

				print("\n" + "S" + str(cont))
				for rule in aux:
					rule.displayItems()
				cont += 1
		'''