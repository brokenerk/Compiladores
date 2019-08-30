#!python3
Id = 0

class AFD:
    def __init__(self,table,alphabet):
        global Id
        Id += 1
        self.table = table
        self.alphabet = alphabet

    #Parameters: Nothing
    #Return: Integer
    def getId(self):
        return self.id  
    #Parameters: Integer
    #Return: Nothing
    def setId(self, id):
        self.id = id   
    #Parameters: Nothing
    #Return: Integer
    def getToken(self):
        return self.token
    #Parameters: Integer
    #Return: Nothing
    def setToken(self, token):
        self.token = token  
    def display(self):
        for r in self.table:
            print(r)
        