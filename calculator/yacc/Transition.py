#!python3
from multipledispatch import dispatch

class Transition:
	#Constructor
	@dispatch(str, object)
	def __init__(self, symbol, next):
		self.symbol = symbol	#Char
		self.endSymbol = None 	#Char
		self.next = next 		#State

	@dispatch(str, str, object)
	def __init__(self, symbol, endSymbol, next):
		self.symbol = symbol			#Char
		self.endSymbol = endSymbol  	#Char
		self.next = next				#State

	#Parameters: Nothing
	#Return: Char
	def getSymbol(self):
		return self.symbol

	#Parameters: Nothing
	#Return: Char
	def getEndSymbol(self):
		return self.endSymbol 

	#Parameters: Nothing
	#Return: State
	def getNext(self):
		return self.next
	#Parameters: State
	#Return: Nothing
	def setNext(self, next):
		self.next = next