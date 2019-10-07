#!python3
from Node import Node
from SyntacticGrammatic import SyntacticGrammatic

class LL1:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 			#List<Nodes>
		self.table = []  			#List<List>
		self.dpFirst = []			#List<Set>
		self.dpFollow = []			#List<Set>
		self.terminals = set()		#Set<>
		self.noTerminals = set()	#Set<>

	#Parameters:
	#Return: 1 if is possible create a Table
	#		0 if not
	def isLL1(self):
		#For each rule
		print("hi from LL1")
		#fillTable()	             
		ruleNumber = 1
		self.setTerminal()
		self.setNoTerminal()
		#print(terminals)
		for r in self.rules:
			#print("Analizo:")
			#print("{} ".format(ruleNumber), end = '')
			#r.displayRule()
			ruleNumber += 1
			# s = First(rightPart)
			# if(s == empty || s == Epsilon):
			# 	s = Follow(leftPart)
			# for i in s:
			# 	if(table[leftPart][i] != -1):
			# 		return -1
			# 	else:
			# 		table[leftPart][i] = rightPart
		return 1

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill the grammar table with -1
	def fillTable(self):
		#List of 3 list
		#table = [[] for i in range (3)]
		for i in range(n):
			table.append([])
		for i in range(n):
			for j in range(m):
				table[i][j] = -1
	
	def setTerminal(self):
		#print("Terminals")
		for i in range(0, len(self.rules)):
			self.terminals.add(self.rules[i].getSymbol()[0]) 
			#print(self.rules[i].getSymbol()[0])

	#Parameters: Nothing
	#Return: Fill Set with not terminal symbols
	def setNoTerminal(self):
		#print("No terminals")
		for i in range(0, len(self.rules)):
			st = self.rules[i].next.getSymbol()
			#print(st)
			for k in range(0, len(st)):
				if st[k] not in self.terminals:
					#print(st[k])
					self.noTerminals.add(st[k])

	def getInitialSymbol(self):
		return rules[0][0]

	#Parameters: Nothing 
	#Return: List<List>
	#Note: Is importat to check if isLL1
	def getTable(self):
		return self.table

	#Parameters: Terminals or No terminals symbols
	#Return: Set of terminals or Epsilon
	def first(self, symbol):
		c = {} 	#Set<>
		if symbol == Epsilon:
			c.add(symbol)
			return c
		if symbol in terminals:
			c.add(symbol)
			return c
		#if symbol is a not terminal
			#----
		return c

	#Parameters: No terminal symbol
	#Return: Set or terminals or $
	def follow(self, symbol):
		c = {}
		if symbol == getInitialSymbol:
			c.add("$")
		return c

