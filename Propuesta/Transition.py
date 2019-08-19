#!python3
class Transition:
    def __init__(self, symbol, next):
        self.symbol = symbol
        self.next = next 

    def getSymbol(self):
        return self.symbol
    def getNext(self):
        return self.next
    def setNext(self, next):
        self.next = next