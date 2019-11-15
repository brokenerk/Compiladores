#!python3
from Node import Node
from copy import deepcopy
epsilon = '\u03B5'

class LR1:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 				#List<Node>
		self.auxListItem = []			#List<List<Node>>
		self.table = []  				#List<List>
		self.analysisTable = []			#List<List>
		self.terminals = set([])		#Set<String>
		self.noTerminals = set([])		#Set<String>
		self.itemSets = [] 				#List<(List<Node>, Set<String>)>
		self.visitedRules = set([]) 	#Set<List<Node>>
		self.visited = set([])			#Set<String>

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
		self.visited.add(symbol)
		if symbol == "epsilon":
			c.add(symbol)
		if symbol in self.terminals:
			c.add(symbol)
		else:
			for j in range(0, len(self.rules)):
				if symbol == self.rules[j].getSymbol():
					if self.rules[j].getNext().getSymbol() not in self.visited:
						c = c.union(self.first(self.rules[j].getNext().getSymbol()))
		return c

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
				if(r1.equals(r2) == True and r1.getLR1Symbols() == r2.getLR1Symbols()):
					cont2 += 1
				cont1 += 1
			#If both conts are the same, it means that item set s1 was already calculated (exists)
			if(cont1 == cont2):
				return True
		#If both conts never matched, it's a new item set
		return False

	def calculateSymbols(self):
		symbols = set([])
		newSet = set([])
		self.visited = set([])	
		cont = 1

		for rule in self.auxListItem:
			auxSymbols = rule.getLR1Symbols()
			next = rule.getNext()

			while(next != None):
				if(next.getPointBefore()):
					n = next.getNext()
					firstAux = set([])

					if(n != None):
						firstAux = self.first(n.getSymbol())

					if(rule.getOriginal()):
						rule.setLR1Symbols(auxSymbols)
						if(firstAux == set([])):
							symbols = auxSymbols
						else:
							symbols = firstAux
							if(rule.isRigthRecursive()):
								symbols = symbols.union(auxSymbols)
					else:
						if(rule.isLeftRecursive()):
							symbols = symbols.union(firstAux)
							rule.setLR1Symbols(symbols)
						else:
							rule.setLR1Symbols(symbols)
							if(cont != len(self.auxListItem) - 1):
								symbols = symbols.union(firstAux)
						
				next = next.getNext()
			cont += 1
			newSet.add(rule)
		return newSet

	#Parametes: List<Node>
	#Return: Set<List<Node>>
	def itemClosure(self, rule):
		s = set([rule])
		self.auxListItem.append(rule)
		next = rule.getNext()

		while(next != None):
			if(next.getPointBefore()):
				if(next.getSymbol() in self.noTerminals):
					nextRules = self.searchRule(next.getSymbol())
					for r in nextRules:
						r.getNext().setPointBefore(True)
						s = s.union(self.itemClosure(deepcopy(r)))
			next = next.getNext()
		return s

	#Parametes: Set<Node>, String
	#Return: Set<Node>
	def move(self, state, symbol):
		s = set([])
		for rule in state:
			rule.setOriginal(False)
			next = rule.getNext()
			while(next != None):
				if(next.getSymbol() == symbol and next.getPointBefore() == True):
					next.setPointBefore(False)
					n = next.getNext()
					if(n != None):
						n.setPointBefore(True)
					else:
						next.setPointAfter(True)

					rule.setOriginal(True)
					s.add(rule)
				next = next.getNext()
		return s

	#Parametes: Set<Node>, String
	#Return: Set<Node>
	def goTo(self, state, symbol):
		self.auxListItem = [] 	#Clear list
		moveStates = self.move(state, symbol)
		returnStates = set([])
		for e in moveStates:
			returnStates = returnStates.union(self.itemClosure(e))
		return self.calculateSymbols()

	#Parameters: Nothing
	#Return: Nothing
	#Note: Generate the states for the displacements on the relations table
	def generateItemSets(self):
		self.setNoTerminals()
		self.setTerminals()
		firstRule = self.rules[0]
		firstRule.setLR1Symbols(set(["$"]))
		firstRule.setOriginal(True)
		firstRule.getNext().setPointBefore(True)

		S0 = self.itemClosure(firstRule)
		S0 = self.calculateSymbols()
		#Sort S0 rules
		S0 = sorted(S0, key = lambda rule0: (rule0.getSymbol(), rule0.getNext().getSymbol(), rule0.getNext().getPointBefore()))  

		queue = [S0] 	#Queue<Set>
		self.itemSets.append(S0) 	#List<List<Node>>
		cont = 1

		print("")
		print("S0")
		for rule in S0:
			rule.displayItems()
			print(str(rule.getLR1Symbols()))

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
					print(str(rule.getLR1Symbols()))
				cont += 1
