#!python3
from Node import Node
epsilon = '\u03B5'

class LL1:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 			#List<Nodes>
		self.table = []  			#List<List>
		self.analysisTable = []		#List<List>
		self.dpFirst = {}			#Dictionary
		self.dpFollow = {}			#Dictionary
		self.terminals = set()		#Set<>
		self.noTerminals = set()	#Set<>
		self.visited = set()		#Set<>
		self.index = {}				#Dictionary

	#Parameters: Nothing
	#Return: True if is possible create a Table
	#		 False if not
	def isLL1(self):             
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
						self.table[x][y] = epsilon
					else:
						self.table[x][y] = srt
				else:
					return False
		return True

	#Paamaters: String
	#Return: True if is a correct string
	#		 False if not
	def analyze(self, c):
		self.initAnalysisTable()
		p = []
		srt = []
		p.append("$")
		p.append(self.getInitialSymbol())
		srt.append("$")
		c = c[::-1]
		for i in range(0, len(c)):
			srt.append(c[i])
		aux = []
		i = 0
		while len(p) > 0:
			if len(srt) == 0:
				return 0
			aux = srt[:]
			aux.reverse()
			values = []
			lastP = p[len(p) - 1]
			lastC = srt[len(srt) - 1]
			if lastC in self.terminals or lastC == "$":
				x = self.index[lastP]
				y = self.index[lastC] - len(self.noTerminals)
				action = self.table[x][y]
				values.append(self.convertToString(p))
				values.append(self.convertToString(aux))
				values.append(action)
				self.analysisTable.append(values)
				if action == 0:
					return False
				elif action == "accept":
					return True
				elif action == "pop":
					p.pop()
					srt.pop()
				elif action == epsilon:
					p.pop()
				elif action != 0:
					p.pop()
					action = action[::-1]
					for i in range(0, len(action)):
						p.append(action[i])
			else:
				return False
		return False

	def initAnalysisTable(self):
		for i in range(1):
			self.analysisTable.append([0] * 3)
		self.analysisTable[0][0] = "Stack"
		self.analysisTable[0][1] = "String"
		self.analysisTable[0][2] = "Action"
		
	def convertToString(self, l):
		s = ""
		for i in range(0, len(l)):
			s = s + l[i]
		return s

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill the grammar table with 0
	def initTable(self):
		t = list(self.terminals - {" "})
		nt = list(self.noTerminals - {" "})
		t.sort()
		nt.sort()
		j = 0
		for i in range(0, len(nt)):
			self.index[nt[i]] = j + 1
			j += 1
		for i in range(0, len(t)):
			self.index[t[i]] = j + 1
			j += 1
		self.index["$"] = j + 1
		for i in range(len(self.terminals) + len(self.noTerminals) + 1):
			self.table.append([0] * (len(self.terminals) + 1))

		for i in range(0, len(self.terminals) + len(self.noTerminals)):
			for j in range(0, len(self.terminals)):
				if (i - len(nt)) == j:
					self.table[i][j] = "pop"
				else:
					self.table[i][j] =0

		self.table[0][0] = " "
		self.table[len(self.terminals) + len(self.noTerminals) - 1][0] = "$"
		self.table[0][len(self.terminals) - 1] = "$"
		self.table[len(self.terminals) + len(self.noTerminals)][len(self.terminals)] = "accept"
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

	#Parameters: Nothing
	#Return: Nothing
	#Note: Clear visited
	def initVisited(self):
		self.visited = set()

	#Parameters: Nothing
	#Return: Initial symbol of the grammar
	def getInitialSymbol(self):
		return self.rules[0].getSymbol()[0]

	#Parameters: Nothing 
	#Return: List<List>
	#Note: Is importat to analysis if isLL1
	def getTable(self):
		return self.table

	def getAnalysisTable(self):
		return self.analysisTable

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill DP of first
	def setDPfirst(self):
		for i in self.terminals:
			self.dpFirst[i] = self.first(i)
		for i in self.noTerminals:
			self.dpFirst[i] = self.first(i)
	
	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill DP of follow
	def setDPfollow(self):
		for i in self.noTerminals:
			self.initVisited()
			self.dpFollow[i] = self.follow(i)
	
	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill set of no terminals symbols
	def setNoTerminal(self):
		for i in range(0, len(self.rules)):
			self.noTerminals.add(self.rules[i].getSymbol()[0]) 
			
	#Parameters: Nothing
	#Return: Nothing 
	#Note: Fill set of terminal symbols
	def setTerminal(self):
		#print("No terminals")
		for i in range(0, len(self.rules)):
			st = self.rules[i].next.getSymbol()
			for k in range(0, len(st)):
				if st[k] not in self.noTerminals:
					self.terminals.add(st[k])

	#Parameters: Nothing
	#Return: Nothing
	#Note: Show table of LL1
	def displayTable(self, op):
		if op == 0:
			print("\nTABLA RELACION DE REGLAS")
			for i in self.table:
				print(i)
		else:
			print("\nTABLA ANALISIS LL(1)")
			for i in self.analysisTable:
				print(i)

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