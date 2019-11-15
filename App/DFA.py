#!python3
Id = 0

class DFA:
    #Constructor
    def __init__(self, table, alphabet):
        global Id
        Id += 1
        self.id = Id;
        self.table = table
        self.alphabet = alphabet

    #Parameters: Nothing
    #Return: Nothing
    def restartId():
        global Id 
        Id = 0

    #Parameters: Nothing
    #Return: Integer
    def getId(self):
        return self.id  
    #Parameters: Integer
    #Return: Nothing
    def setId(self, id):
        self.id = id   

    #Parameters: Nothing
    #Return: List<List>
    def getTable(self):
        return self.table  
    #Parameters: List<List>
    #Return: Nothing
    def setTable(self, table):
        self.table = table   

    #Parameters: Nothing
    #Return: Set<Char>
    def getAlphabet(self):
        return sorted(self.alphabet)   
    #Parameters: Set<Char>
    #Return: Nothing
    def setAlphabet(self, alphabet):
        self.alphabet = alphabet

    def displayTable(self):
        print("Id: {}".format(self.id))
        print("  {}[Token]".format(self.alphabet))
        for i in range(0, len(self.table)):
            print("{} {}".format(i, self.table[i]))