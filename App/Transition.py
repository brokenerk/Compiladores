#!python3
from multipledispatch import dispatch

class Transition:
	#Constructor
	@dispatch(str, object)
	def __init__(self, symbol, next):
		self.symbol = symbol	#Char
		self.next = next 		#State
		self.symbolEnd = None 	#Char

	@dispatch(str, str, object)
	def __init__(self, symbol, symbolEnd, next):
		self.symbol = symbol		#Char
		self.symbolEnd = symbolEnd 	#Char
		self.next = next			#State

	#Parameters: Nothing
	#Return: Char
	def getSymbol(self):
		return self.symbol

	#Parameters: Nothing
	#Return: Char
	def getSymbolEnd(self):
		return self.symbolEnd

	#Parameters: Nothing
	#Return: State
	def getNext(self):
		return self.next
	#Parameters: State
	#Return: Nothing
	def setNext(self, next):
		self.next = next