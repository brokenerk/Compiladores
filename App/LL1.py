#!python3
from Node import Node
from SyntacticGrammatic import SyntacticGrammatic

class LL1:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 			#List<Nodes>
		self.table = []  			#List<List>
		self.dpFirst = {}			#Dictionary
		self.dpFollow = {}			#Dictionary
		self.terminals = set()		#Set<>
		self.noTerminals = set()	#Set<>
		self.visited = set()		#Set<>

	#Parameters:
	#Return: 1 if is possible create a Table
	#		0 if not
	def isLL1(self):
		#For each rule
		#fillTable()	             
		self.setNoTerminal()
		self.setTerminal()
		self.setDPfirst()
		#self.setDPfollow()
		print("Terminals: ", self.terminals)
		print("No terminals: ", self.noTerminals)

		for i in range(0, len(self.rules)):
			print(">>>>>>>> Analizando: ", self.rules[i].next.getSymbol())
			s = self.dpFirst[self.rules[i].next.getSymbol()]
			
			if len(s) <= 1:
				if " " in s or s == 0:
					print("Hago follow de: ", self.rules[i].getSymbol()[0])
					s = self.follow(self.rules[i].getSymbol()[0])
			print("First: ", s)
			#for i in s:
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
	
	def setNoTerminal(self):
		for i in range(0, len(self.rules)):
			self.noTerminals.add(self.rules[i].getSymbol()[0]) 
			
	#Parameters: Nothing
	#Return: Fill Set with not terminal symbols
	def setTerminal(self):
		#print("No terminals")
		for i in range(0, len(self.rules)):
			st = self.rules[i].next.getSymbol()
			for k in range(0, len(st)):
				if st[k] not in self.noTerminals:
					#print(st[k])
					self.terminals.add(st[k])

	def getInitialSymbol(self):
		return self.rules[0].getSymbol()[0]

	#Parameters: Nothing 
	#Return: List<List>
	#Note: Is importat to check if isLL1
	def getTable(self):
		return self.table

	#Parameters: Terminals or No terminals symbols
	#Return: Set of terminals or Epsilon
	def first(self, symbol):
		c = set() 	#Set<>
		for i in range(0, len(symbol)):
			if symbol[i] == " ":
				c.add(symbol[i])
				return c
			if symbol[i] in self.terminals:
				c.add(symbol[i])
				return c
			for j in range(0, len(self.rules)):
				if symbol[i] == self.rules[j].getSymbol()[0]:
					c = c.union(self.first(self.rules[j].next.getSymbol()))
			return c

	#Parameters: No terminal symbol
	#Return: Set or terminals or $
	def follow(self, symbol):
		self.visited.add(symbol)
		print(" ------------------------- FOLLOW DE: ", symbol)
		c = set()
		if symbol == self.getInitialSymbol():
			c.add("$")
		for i in range(0, len(self.rules)):
			st = self.rules[i].next.getSymbol()
			for k in range(0, len(st)):
				if st[k] == symbol:
					#print("Soy: ", st)
					for j in range(k+1, len(st)):
						aux = self.first(st[j])
						if " " in aux:
							if self.rules[i].next.getSymbol()[0] in self.visited:
								c = c.union(set())
							else:
								c = c.union(self.follow(self.rules[i].next.getSymbol()[0]))
							aux = aux - {" "}
						c = c.union(aux)
					break	
		print("Conjunto actual: ", c)	
		for i in range(0, len(self.rules)):
			st = self.rules[i].next.getSymbol()
			for k in range(0, len(st)):
				if st[k] == symbol:

					if self.rules[i].getSymbol()[0] in self.visited:
						print("Somo iguales, al que quiero, entonces NO HAGO FOLLOW")
						c = c.union(set())
					else:
						c = c.union(self.follow(self.rules[i].getSymbol()[0]))
					break
		print("follow de: ", symbol, " es: ", c)
		return c

	def setDPfirst(self):
		for i in range(0, len(self.rules)):
			self.dpFirst[self.rules[i].next.getSymbol()] = self.first(self.rules[i].next.getSymbol())
		for i in range(0, len(self.rules)):
			self.dpFirst[self.rules[i].getSymbol()[0]] = self.first(self.rules[i].getSymbol()[0]) 
		# print("DP:")
		# for i in self.dpFirst.values():
		# 	print(i)	


