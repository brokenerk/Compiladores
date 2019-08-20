#!python3
class Transition:
	#Constructor
	def __init__(self, symbol, next):
		self.symbol = symbol 			#Char
		self.next = next 				#State

	#Parameters: Nothing
	#Return: Char
	def getSymbol(self):
		return self.symbol

	#Parameters: Nothing
	#Return: State
	def getNext(self):
		return self.next

	#Parameters: State
	#Return: Nothing
	def setNext(self, next):
		self.next = next