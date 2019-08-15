#!python3
class Transition:
	#Constructor
	def __init__(self, character, next):
		self.character = character 	#Symbol
		self.next = next 			#Next state

	def getCharacter(self):
		return self.character

	def setCharacter(self, character):
		self.character = character

	def getNext(self):
		return self.next

	def setNext(self, next):
		self.next = next