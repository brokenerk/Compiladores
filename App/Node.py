#!python3
#Each Node object is a Grammar Rule!
class Node:
    def __init__(self, symbol, next):
        self.symbol = symbol                #String
        self.next = next                    #Node
        self.pointBefore = False            #Boolean
        self.pointAfter = False             #Boolean
        self.lr1Symbols = set([])           #Set<String>
        self.counter = 0                    #Integer

    #Return: Node
    def getNext(self):
        return self.next
    
    #Parameters: Integer
    #Return: Nothing
    def setCounter(self, c):
        self.counter = c

    #Parameters: Nothing
    #Return: Integer
    def getCounter(self):
        return self.counter

    #Parameters: Node
    #Return: Nothing
    def setNext(self, next):
        self.next = next
    
    #Parameters: Nothing
    #Return: String
    def getSymbol(self):
        return self.symbol
    
    #Parameters: String
    #Return: Nothing
    def setSymbol(self, symbol):
        self.symbol = symbol

    #Parameters: Nothing
    #Return: Boolean
    def getPointBefore(self):
        return self.pointBefore
    
    #Parameters: Boolean
    #Return: Nothing
    def setPointBefore(self, pointBefore):
        self.pointBefore = pointBefore

    #Parameters: Nothing
    #Return: Boolean
    def getPointAfter(self):
        return self.pointAfter
    
    #Parameters: Boolean
    #Return: Nothing
    def setPointAfter(self, pointAfter):
        self.pointAfter = pointAfter

    #Parameters: Nothing
    #Return: Set<String>
    def getLR1Symbols(self):
        return self.lr1Symbols
    
    #Parameters: Set<String>
    #Return: Nothing
    def setLR1Symbols(self, lr1Symbols):
        self.lr1Symbols = lr1Symbols

    #Parameters: Nothing
    #Return: Integer
    #Note: Number of next nodes connected
    def size(self):
        next = self.getNext()
        cont = 0
        while(next != None):
            if(next.getSymbol() == "epsilon"):
                return 0
            cont += 1
            next = next.getNext()
        return cont

    #Parameters: Nothing
    #Return: Boolean
    def isLeftRecursive(self):
        next = self.getNext()
        return next.getSymbol() == self.symbol

    #Parameters: Node
    #Return: Boolean
    def equals(self, other):
        if(self.symbol != other.getSymbol()):
            return False
        else:
            if(self.size() != other.size()):
                return False
            else:
                next = self.getNext()
                n = other.getNext()

                while(n != None and next != None):
                    if(next.getSymbol() != n.getSymbol()):
                        return False
                    else:
                        if(next.getPointBefore() != n.getPointBefore()):
                            return False
                        else:
                            if(next.getPointAfter() != n.getPointAfter()):
                                return False
                    next = next.getNext()
                    n = n.getNext()
        return True

    #Parameters: Nothing
    #Return: List<Node>
    def getRule(self):
        rule = [self.symbol, "--->"]
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

    #Parameters: Nothing
    #Return: Nothing
    def displayItems(self):
        print("{} -->".format(self.symbol), end = '')
        next = self.getNext()

        while(next != None):
            if(next.getPointBefore()):
                print(" °{}".format(next.getSymbol()), end = '')
            elif(next.getPointAfter()):
                print(" {}°".format(next.getSymbol()), end = '')
            else:
                print(" {}".format(next.getSymbol()), end = '')
            next = next.getNext()
        print("")