#!python3
from Node import Node
from SyntacticGrammatic import SyntacticGrammatic

class LL1:
	#Constructor
	def __init__(self, rules):
		self.rules = rules 		#List<Nodes>
		self.table = []  		#List<List>
		self.dpFirst = {}		#Set<Set>
		self.dpFollow = {}		#Set<Set>

	#Parameters:
	#Return: 1 if is possible create a Table
	#		0 if not
	def isLL1(self):
		#For each rule
		print("hi from LL1")
		return 1

	#Parameters: Nothing
	#Return: List<List>
	#Note: Is importat to check if isLL1
	def getTable(self):
		return self.table

	def first(self):
		c = {} 	#Set<>
		return c

	def follow(self):
		c = {}
		return c

