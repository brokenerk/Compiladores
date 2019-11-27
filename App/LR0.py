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
		self.itemSets = [] 				#List<List<Node>>
		self.visitedRules = set([]) 	#Set<List<Node>>
		self.index = {}					#Dictionary
		self.numberRules = {}			#Dictionary
		self.t = []						#List<String>
		self.nt = []					#List<String>
		self.dpFirst = {}				#Dictionary
		self.dpFollow = {}				#Dictionary
		self.visited = set()			#Set<String>
		self.rulesDictionary = {}		#Dictionary Rules
		
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

	#Parameters: Nothing
	#Return: Initial symbol of the grammar
	def getInitialSymbol(self):
		return self.rules[0].getSymbol()

	#Parameters: Nothing
	#Return: Counter of the initial symbol
	def getInitialCounter(self):
		return self.rules[0].getCounter()

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fll LR(0) Table
	def initializeTable(self):
		self.nt = list(self.noTerminals)
		self.t = list(self.terminals) 

		self.nt.sort()
		self.t.sort()
		self.table.append([0] * (len(self.t) + len(self.nt) + 2))

		j = 1
		for i in range(0, len(self.t)):
			self.index[self.t[i]] = j
			self.table[0][j] = self.t[i]
			j += 1

		for i in range(0, len(self.nt)):
			self.index[self.nt[i]] = j
			self.table[0][j] = self.nt[i]
			j += 1

		self.index["$"] = j
		self.table[0][j] = "$"
		for i in self.table:
			print(i)
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
		i = 0
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
				return i
			i += 1
		#If both conts never matched, it's a new item set
		return -1

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
			returnStates = returnStates.union(self.itemClosure(e))
		return returnStates

	#Parameters: Nothing
	#Return: Nothing
	#Note: Create a dictionary
	def initializeCounter(self):
		print("Creating counter...")
		i = 0
		for rule in self.rules:
			print("Adding rule:", i)
			rule.setCounter(i)
			self.rulesDictionary[i] = rule
			i += 1

	#Parameters: Nothing
	#Return: Nothing
	#Note: Generate the states for the displacements on the relations table
	def isLR0(self):
		self.setNoTerminals()
		self.setTerminals()
		self.initializeTable()
		self.setDPFirst()
		self.setDPFollow()
		self.initializeCounter()

		firstRule = self.rules[0]

		firstRule.getNext().setPointBefore(True)
		S0 = self.itemClosure(firstRule)
		
		#Sort S0 rules
		S0 = sorted(S0, key = lambda rule0: (rule0.getSymbol(), rule0.getNext().getSymbol(), rule0.getNext().getPointBefore())) 
		queue = [S0] 	#Queue<Set>
		self.itemSets.append(S0) 	#List<List<Node>>
		cont = 1

		print("")
		print("S0")
		for rule in S0:
			rule.displayItems()

		#Table LR(0)
		self.table.append([0] * (len(self.t) + len(self.nt) + 2))
		self.table[0][0] = 0 
		i = 0
		while queue:
			Si = queue.pop(0) 	#Get first enter
			symbolItems = self.getSymbolItems(Si)
			
			#print(symbolItems)
			#Iterate over the item symbols
			for symbol in symbolItems:
				#print("---> Estoy en: ", symbol)
				self.visitedRules = set([])
				aux = self.goTo(deepcopy(Si), symbol)
				
				#Set is empty, do nothing
				if(aux == set()):
					continue

				#Sort aux rules
				aux = sorted(aux, key = lambda rule: (rule.getSymbol(), rule.getNext().getSymbol(), rule.getNext().getPointBefore())) 
					
				pair = []
				pair.insert(0, "d") 		#Insert a pair in the list 
				
				check = self.exists(aux)	#Verify is set already exists in list
				
				if(check >= 0):
					pair.insert(1, check)
					# Check if there is an error
					if(self.table[i + 1][self.index[symbol]] != 0):
						return 0
					else:
						self.table[i + 1][self.index[symbol]] = pair
					continue

				self.table.append([0] * (len(self.t) + len(self.nt) + 2))
				self.table[cont + 1][0] = cont
				pair.insert(1, cont)
				self.table[i + 1][self.index[symbol]] = pair
				
				queue.append(aux)			#Add new set to the end of the queue
				self.itemSets.append(aux) 	#Add the new set to the list

				print("\n" + "S" + str(cont))
				# for rule in aux:
				# 	rule.displayItems()

				#Adding Rules 
				for rule in aux:
					next = rule.getNext()
					while(next != None):
						if(next.getPointAfter()):
							followDP = self.dpFollow[rule.symbol] 	#Get Follow[rule.symbol] to add into Table
							
							for char in followDP:
								ruleTable = [] 	#Add a pair: [r, cont]
								if(self.getInitialCounter() == rule.counter):
									ruleTable.insert(0, 1)
									ruleTable.insert(1, "accept")
								else:
									ruleTable.insert(0, "r")
									ruleTable.insert(1, rule.counter)
								
								# Check if there is an error
								if(self.table[cont + 1][self.index[char]] != 0):
									return 0
								else:
									self.table[cont + 1][self.index[char]] = ruleTable
						next = next.getNext()
				cont += 1
			i += 1

		print("Table:")
		for i in self.table:
			print(i)
	
		return 1

	#Parameters: Nothing
	#Return: Nothing
	#Note: Generate the initial table of the analysis
	def initAnalysisTable(self):
		for i in range(1):
			self.analysisTable.append([0] * 3)
		self.analysisTable[0][0] = "Stack"
		self.analysisTable[0][1] = "String"
		self.analysisTable[0][2] = "Action"

	#Parameters: Rule
	#Return: Number of right symbols of the Rule
	def countSymbols(self, r):
		next = r.getNext()
		i = 0
		while(next != None):
			if(next.getSymbol() == "epsilon"):
				return 0
			i += 1
			next = next.getNext()
		return i

	#Parameters: List
	#Return: String
	def convertToString(self, l):
		s = ""
		for i in range(0, len(l)):
			s = s + str(l[i])
		return s

	#Parameter: Nothing
	#Return: Nothing
	#Note: Show the analysis table
	def printAnalysisTable(self):
		for i in self.analysisTable:
			print(i)


	#Parameters: string
	#Return: True if the string allow to the grammar, false in other case
	def analyze(self, c):
		print("Analizando ...")
		self.initAnalysisTable()
		p = []
		srt = []
		print("Initial counter:", self.getInitialCounter())
		p.append(self.getInitialCounter())
		
		#PUT LEXICO
		c = ["num", "*", "(", "num", "+", "num", ")"]

		#Convert to list
		for i in range(0, len(c)):
			srt.append(c[i])
		srt.append("$")

		while p:
			#There are no symbols to analyze	
			if len(srt) == 0:
				return False
			values = []				#Aux to generate front table
			lastP = p[len(p) - 1] 	#Top of the stack
			strAnalysis = srt[0]	#Symbol to analyze
			
			#Get Coordinates to the first action
			x = lastP + 1
			if strAnalysis in self.index:
				y = self.index[strAnalysis]
			else:
				return False

			#Get action from table of LR0
			action = self.table[x][y]

			#Front table
			values.append(self.convertToString(p))
			values.append(self.convertToString(srt))
			values.append(self.convertToString(action))
			self.analysisTable.append(values)
			
			#Its a displacement
			if action[0] == "d":
				p.append(strAnalysis)	#Add symbol to the Stack
				p.append(action[1])		#Add number of displacement to the Stack
				srt.pop(0)				#Delete symbol from the string to analyze

			#Is a reduction
			elif action[0] == "r":				
				if action[1] in self.rulesDictionary: 								#Verify rule number exist on rulesDictionary					
					toPop = self.countSymbols(self.rulesDictionary[action[1]]) * 2	#Get rule to calculate number of symbols
					
					#Delete from stack the number of symbols calculated
					while(toPop):
						if len(p) > 0:
							p.pop()
						else:
							return False
						toPop -= 1

					#Get Coordinates to the second action
					if len(p) > 0:
						x = p[len(p) - 1] + 1 										#Calculated coordinate X
					else:
						return False

					if self.rulesDictionary[action[1]].getSymbol() in self.index:
						y = self.index[self.rulesDictionary[action[1]].getSymbol()] #Calculate cordinate Y
					else:
						return False

					#Get second action
					secondAction = self.table[x][y]
					if secondAction[0] == "d":
						#Add to the Stack
						p.append(self.rulesDictionary[action[1]].getSymbol())
						p.append(secondAction[1])
					else:
						return False
				#Rule doesnt exist rulesDictionary
				else:
					return False

			#Its an accepted
			elif action[0] == 1:
				return True
			
			#Error
			else:
				return False
		return False

	#Parameters: Nothing
	#Return: Nothing
	#Note: Clear visited
	def initVisited(self):
		self.visited = set()

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill DP of first
	def setDPFirst(self):
		for i in self.terminals:
			self.dpFirst[i] = self.first(i)
		for i in self.noTerminals:
			self.initVisited()
			self.dpFirst[i] = self.first(i)
	
	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill DP of follow
	def setDPFollow(self):
		for i in self.noTerminals:
			self.initVisited()
			c = self.follow(i)
			if c != set():
				self.dpFollow[i] = c

	#Parameters: Terminals or No terminals symbols
	#Return: Set of terminals or Epsilon
	def first(self, symbol):
		if symbol in self.dpFirst:
			return self.dpFirst[symbol]
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
		if c != set():
			self.dpFirst[symbol] = c
		return c

	#Parameters: No terminal symbol
	#Return: Set of terminals or $
	def follow(self, symbol):
		#If follow of Symbol has been calculated before, consult
		if symbol in self.dpFollow:
			return self.dpFollow[symbol]
		c = set()
		self.visited.add(symbol)
		
		#Symbol is the initial symbol of the grammar
		if symbol == self.getInitialSymbol():
			c.add("$")

		#Is a No terminal symbol
		for i in range(0, len(self.rules)):
			next = self.rules[i].getNext()
			while(next != None):
				st = next.getSymbol()
				if st == symbol:
					n = next.getNext()
					if n == None:
						if self.rules[i].getSymbol() not in self.visited:
							c = c.union(self.follow(self.rules[i].getSymbol()))
					else:
						n = next.getNext()
						aux = self.dpFirst[n.getSymbol()]
						if "epsilon" in aux:
							if self.rules[i].getSymbol() not in self.visited:
								c = c.union(self.follow(self.rules[i].getSymbol()))
							aux = aux - {"epsilon"}
						c = c.union(aux);
				next = next.getNext()
		if c != set():
			self.dpFollow[symbol] = c
		return c