#!python3

class Node:
    def __init__(self, next,terminal,symbol):
        self.next = next
        self.terminal = terminal
        self.symbol = symbol

    #Parameters: Nothing
    #Return: Integer
    def getNext(self):
        return self.next

    #Parameters: Node
    #Return: Nothing
    def setNext(self, next):
        self.next = next
    
    #Parameters: Nothing
    #Return: Integer
    def getNext(self):
        return self.terminal

    #Parameters: Integer
    #Return: Nothing
    def setNext(self, terminal):
        self.terminal = terminal
        
    #Parameters: Nothing
    #Return: Integer
    def getNext(self):
        return self.symbol

    #Parameters: string
    #Return: Nothing
    def setNext(self, symbol):
        self.symbol = symbol  