#!python3
#Each Node object is a Grammar Rule!
class Node:
    def __init__(self, symbol, next):
        self.symbol = symbol    #String
        self.next = next        #Node
        self.terminal = False   #Boolean

    #Parameters: Nothing
    #Return: Node
    def getNext(self):
        return self.next

    #Parameters: Node
    #Return: Nothing
    def setNext(self, next):
        self.next = next
    
    #Parameters: Nothing
    #Return: Boolean
    def getTerminal(self):
        return self.terminal

    #Parameters: Integer
    #Return: Boolean
    def setTerminal(self, terminal):
        self.terminal = terminal
            
    #Parameters: Nothing
    #Return: String
    def getSymbol(self):
        return self.symbol

    #Parameters: String
    #Return: Nothing
    def setSymbol(self, symbol):
        self.symbol = symbol

    def getRule(self):
        rule = []
        rule.append(self.symbol)
        rule.append("--->")

        next = self.getNext()

        while(next != None):
            rule.append(next.getSymbol())
            next = next.getNext()
        return rule

    #Parameters: Nothing
    #Return: Nothing
    def displayRule(self):
        print("{} -->".format(self.symbol), end = '')
        next = self.getNext()

        while(next != None):
            print(" {}".format(next.getSymbol()), end = '')
            next = next.getNext()
        print("")