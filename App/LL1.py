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
		self.index = {}				#Dictionary

	#Parameters:
	#Return: 1 if is possible create a Table
	#		0 if not
	def isLL1(self):
		#For each rule
		#fillTable()	             
		self.setNoTerminal()
		self.setTerminal()
		self.setDPfirst()
		self.setDPfollow()
		self.initTable()
		for i in range(0, len(self.rules)):
			srt = self.rules[i].next.getSymbol()
			s = self.dpFirst[srt[0]]
			if len(s) <= 1:
				if " " in s or s == 0:
					s = self.follow(self.rules[i].getSymbol()[0])
			l = list(s)
			for j in range(0, len(l)):
				x = self.index[self.rules[i].getSymbol()[0]]
				y = self.index[l[j]] - len(self.noTerminals)
				if self.table[x][y] == 0:
					if srt == " ":
						self.table[x][y] = "Epsilon"
					else:
						self.table[x][y] = srt
				else:
					return -1

		print("")
		print("TABLA")
		for i in self.table:
			print(i)
		return 1

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill the grammar table with -1
	def initTable(self):
		#List of 3 list
		#table = [[] for i in range (3)]
		t = list(self.terminals - {" "})
		nt = list(self.noTerminals - {" "})

		print(t)
		j = 0
		for i in range(0, len(nt)):
			self.index[nt[i]] = j + 1
			j += 1
		for i in range(0, len(t)):
			self.index[t[i]] = j + 1
			j += 1

		for i in range(len(self.terminals) + len(self.noTerminals) + 1):
			self.table.append([0] * (len(self.terminals) + 1))

		for i in range(0, len(self.terminals) + len(self.noTerminals)):
			for j in range(0, len(self.terminals)):
				if (i - len(t) + 2) == j:
					self.table[i][j] = "pop"
				else:
					self.table[i][j] =0

		self.table[0][0] = " "
		self.table[len(self.terminals) + len(self.noTerminals) - 1][0] = "$"
		self.table[0][len(self.terminals) - 1] = "$"
		self.table[len(self.terminals) + len(self.noTerminals)][len(self.terminals)] = "AC"
		# Fill with No terminals
		j = 1
		for i in range(0, len(nt)):
			self.table[j][0] = nt[i]
			j += 1
		# Fill with terminals
		for i in range(0, len(t)):	
			self.table[j][0] = t[i]
			j += 1
		self.table[j][0] = "$"
		j = 1
		for i in range(0, len(t)):
			self.table[0][j] = t[i];
			j += 1
		self.table[0][j] = "$"
	
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
		if symbol in self.dpFirst:
			return self.dpFirst[symbol]
		c = set() 	#Set<>
		if symbol == " ":
			c.add(symbol)
		if symbol in self.terminals:
			c.add(symbol)
		else:
			for j in range(0, len(self.rules)):
				if symbol == self.rules[j].getSymbol()[0]:
					c = c.union(self.first(self.rules[j].next.getSymbol()[0]))
		self.dpFirst[symbol] = c
		return  c

	#Parameters: No terminal symbol
	#Return: Set or terminals or $
	def follow(self, symbol):
		if symbol in self.dpFollow:
			return self.dpFollow[symbol]
		c = set()
		self.visited.add(symbol)
		if symbol == self.getInitialSymbol():
			c.add("$")
		for i in range(0, len(self.rules)):
			st = self.rules[i].next.getSymbol()
			for k in range(0, len(st)):
				if st[k] == symbol:
					if k == (len(st) - 1):
						if self.rules[i].getSymbol()[0] not in self.visited:
							c = c.union(self.follow(self.rules[i].getSymbol()[0]))
					else:				
						for j in range(k + 1, len(st)):
							aux = self.first(st[j])
							if " " in aux:
								if self.rules[i].getSymbol()[0] not in self.visited:
									c = c.union(self.follow(self.rules[i].getSymbol()[0]))
								aux = aux - {" "}
							c = c.union(aux);
		if len(c) > 0:
			self.dpFollow[symbol] = c
		return c

	def setDPfirst(self):
		for i in self.terminals:
			self.dpFirst[i] = self.first(i)
		for i in self.noTerminals:
			self.dpFirst[i] = self.first(i)		

	def setDPfollow(self):
		for i in self.noTerminals:
			self.initVisited()
			self.dpFollow[i] = self.follow(i)

		# print("follows")
		# for i in self.dpFollow.values():
		# 	print(i)
	
	def initVisited(self):
		self.visited = set()