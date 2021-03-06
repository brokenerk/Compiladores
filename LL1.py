#!python3
from Node import Node
from Lexer import Lexer
from Token import Token
epsilon = '\u03B5'

class LL1:
	#Constructor
	def __init__(self, rules, stringLex):
		self.rules = rules 			#List<Node>
		self.table = []  			#List<List>
		self.analysisTable = []		#List<List>
		self.dpFirst = {}			#Dictionary
		self.dpFollow = {}			#Dictionary
		self.terminals = set()		#Set<String>
		self.noTerminals = set()	#Set<String>
		self.visited = set()		#Set<String>
		self.index = {}				#Dictionary
		self.stringLex = stringLex	#Lexer

	#Parameters: Nothing
	#Return: True if is possible create a Table
	#		 False if not
	def isLL1(self):             
		self.setNoTerminals()
		self.setTerminals()
		self.setDPFirst()
		print("FIRST")
		for i in self.dpFirst:
			print(i + ": " + str(self.dpFirst[i]))

		print("")
		print("FOLLOW")
		self.setDPFollow()
		for i in self.dpFollow:
			print(i + ": " + str(self.dpFollow[i]))

		self.initTable()
		for i in range(0, len(self.rules)):
			next = self.rules[i].getNext()
			srt = next.getSymbol()
			s = self.dpFirst[srt]
			next = next.getNext()

			while(next != None):
				srt = srt + " " + next.getSymbol()
				next = next.getNext()

			if "epsilon" in s or s == set():
				s = self.dpFollow[self.rules[i].getSymbol()]

			for elem in s:
				x = self.index[self.rules[i].getSymbol()]
				y = self.index[elem] - len(self.noTerminals)
				if(self.table[x][y] == 0):
					if srt == "epsilon":
						self.table[x][y] = epsilon
					else:
						self.table[x][y] = srt
				else:
					return False
		return True

	#Paramaters: String
	#Return: True if is a correct string
	#		 False if not
	def analyze(self, c):
		self.initAnalysisTable()
		p = []
		srt = []
		p.append("$")
		p.append(self.rules[0].getSymbol())
		
		for i in range(0, len(c)):
			srt.append(c[i])

		srt.append("$")
		token = self.stringLex.getToken()
		begin = self.stringLex.getStatus().getBeginLexPos()
		end = self.stringLex.getStatus().getEndLexPos()

		while p:
			if len(srt) == 0:
				return False
			values = []
			lastP = p[len(p) - 1]
			firstC = srt[0]

			x = self.index[lastP]
			'''
			Here we put all the necessaries Tokens

			if(token == Token.SYMBOL):
			if(token == Token.FLECHA):
				.
				.
				.
			'''
			if(firstC in self.terminals or firstC == "$"):
				y = self.index[firstC] - len(self.noTerminals)
			elif(token == Token.ARROW and "FLECHA" in self.terminals):
				y = self.index["FLECHA"] - len(self.noTerminals)
			elif(token == Token.SEMICOLON and "PC" in self.terminals):
				y = self.index["PC"] - len(self.noTerminals)
			elif(token == Token.OR and "OR" in self.terminals):
				y = self.index["OR"] - len(self.noTerminals)
			elif(token == Token.SPACE and "ESPACIO" in self.terminals):
				y = self.index["ESPACIO"] - len(self.noTerminals)
			elif(token == Token.CONCAT and "AND" in self.terminals):
				y = self.index["AND"] - len(self.noTerminals)
			elif(token == Token.COMMA and "coma" in self.terminals):
				y = self.index["coma"] - len(self.noTerminals)
			elif(token == Token.NUM and "num" in self.terminals):
				y = self.index["num"] - len(self.noTerminals)
			elif(token == Token.PLUS and "SIMBOLO" in self.terminals):
				y = self.index["SIMBOLO"] - len(self.noTerminals)
			elif(token == Token.MINUS and "SIMBOLO" in self.terminals):
				y = self.index["SIMBOLO"] - len(self.noTerminals)
			elif(token == Token.PROD and "SIMBOLO" in self.terminals):
				y = self.index["SIMBOLO"] - len(self.noTerminals)
			elif(token == Token.DIV and "SIMBOLO" in self.terminals):
				y = self.index["SIMBOLO"] - len(self.noTerminals)
			elif(token == Token.PAR_L and "SIMBOLO" in self.terminals):
				y = self.index["SIMBOLO"] - len(self.noTerminals)
			elif(token == Token.PAR_R and "SIMBOLO" in self.terminals):
				y = self.index["SIMBOLO"] - len(self.noTerminals)
			elif(token == Token.SYMBOL):
				if("SIMBOLO" in self.terminals):
					y = self.index["SIMBOLO"] - len(self.noTerminals)
				elif("id" in self.terminals and self.stringLex.getLexem() == "id"):
					y = self.index["id"] - len(self.noTerminals)
				else:
					break
			else:
				break

			action = self.table[x][y]
			values.append(self.convertToString(p))
			values.append(self.convertToString(srt))

			if action != 0:
				values.append(action.replace(" ", ""))
			else:
				values.append(action)
			self.analysisTable.append(values)

			if action == 0:
				return False
			elif action == "accept":
				return True
			elif action == "pop":
				p.pop()
				if(token != Token.ERROR and firstC not in self.terminals):
					times = end - begin
					for i in range(0, times + 1):
						srt.pop(0)
				else:
					srt.pop(0)
				token = self.stringLex.getToken()
				begin = self.stringLex.getStatus().getBeginLexPos()
				end = self.stringLex.getStatus().getEndLexPos()
			elif action == epsilon:
				p.pop()
			elif action != 0:
				p.pop()
				actionList = action.split(" ")
				actionList.reverse()
				for i in range(0, len(actionList)):
					p.append(actionList[i])
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
		t = list(self.terminals - {"epsilon"})
		nt = list(self.noTerminals - {"epsilon"})
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

		for i in range(0, len(self.terminals) + len(self.noTerminals) + 1):
			for j in range(0, len(self.terminals) + 1):
				if (i - len(nt)) == j:
					self.table[i][j] = "pop"
				else:
					self.table[i][j] = 0

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
			self.table[0][j] = t[i]
			j += 1
		self.table[0][j] = "$"

	#Parameters: Nothing 
	#Return: List<List>
	#Note: Rule Relations Table
	def getTable(self):
		return self.table

	#Parameters: Nothing 
	#Return: List<List>
	#Note: Analysis Table
	def getAnalysisTable(self):
		return self.analysisTable

	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill DP of first
	def setDPFirst(self):
		for i in self.terminals:
			self.dpFirst[i] = self.first(i)
		for i in self.noTerminals:
			self.visited = set()
			self.dpFirst[i] = self.first(i)
	
	#Parameters: Nothing
	#Return: Nothing
	#Note: Fill DP of follow
	def setDPFollow(self):
		for i in self.noTerminals:
			self.visited = set()
			c = self.follow(i)
			if c != set():
				self.dpFollow[i] = c
	
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
		#print("No terminals")
		for i in range(0, len(self.rules)):
			next = self.rules[i].getNext()
			while(next != None):
				st = next.getSymbol()
				if st not in self.noTerminals:
					self.terminals.add(st)
				next = next.getNext()

	#Parameters: Nothing
	#Return: Nothing
	#Note: Show table of LL1
	def displayTable(self, op):
		if op == 0:
			print("TABLA RELACION DE REGLAS")
			for i in self.table:
				print(i)
		else:
			print("TABLA ANALISIS LL(1)")
			for i in self.analysisTable:
				print(i)

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
		if symbol in self.dpFollow:
			return self.dpFollow[symbol]
		c = set()
		self.visited.add(symbol)
		if symbol == self.rules[0].getSymbol():
			c.add("$")
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
						#while(n != None):
						aux = self.dpFirst[n.getSymbol()]
						if "epsilon" in aux:
							if self.rules[i].getSymbol() not in self.visited:
								c = c.union(self.follow(self.rules[i].getSymbol()))
							aux = aux - {"epsilon"}
						c = c.union(aux)
						#	n = n.getNext()
				next = next.getNext()
		if c != set():
			self.dpFollow[symbol] = c
		return c