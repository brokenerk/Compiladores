#!python3

class Symbol:
    def __init__(self, name,typeS,val,func ,next):
        self.name = name
        self.typeS = typeS
        self.val = val
        self.func = func

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getType(self):
        return self.typeS

    def setType(self, typeS):
        self.typeS = typeS

    def getVal(self):
        return self.val

    def setVal(self, val):
        self.val = val

    def getFunc(self):
        return self.func

    def setFunc(self, func):
        self.func = func

# dictionary of names (for storing variables)
Symbols = {}