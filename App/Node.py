#!python3

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

    #Parameters: Nothing
    #Return: Nothing
    def displayRule(self):
        havNext = True
        print("{} ---> ".format(self.symbol), end = '')
        while havNext:
            havNext = False
            print("{}".format(self.next.getSymbol()))
            if(self.next.getNext() != None):
                havNext = True