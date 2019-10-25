#!python3
#Each Node object is a Grammar Rule!
class Node:
    def __init__(self, symbol, next):
        self.symbol = symbol        #String
        self.next = next            #Node
        self.pointBefore = False    #Boolean
        self.pointAfter = False      #Boolean

    #Parameters: Nothing
    #Return: Node
    def getNext(self):
        return self.next

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