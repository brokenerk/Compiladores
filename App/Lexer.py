#!python3
from AFD import AFD
from Token import Token
from collections import deque
endString = '\0'

class Lexer:
    #Constructor
    def __init__(self, afd, string):
        self.afd = afd                          #AFD
        self.string = string + endString        #String
        self.actualSymbolPos = 0                #Integer
        self.reachedAccept = False              #Boolean
        self.actualState = 0                    #Integer
        self.beginLexPos = -1                   #Integer
        self.endLexPos = -1                     #Integer
        self.stack = deque()                    #Stack<Integer>
        self.token = -1                         #Integer
        self.lex = ""                           #String

    def getToken(self):
        return self.token   

    def returnToken(self):
        return

    def getStatus(self):
        return

    def setStatus(self):
        return

    #Parameters: Nothing
    #Return: Integer
    def yylex(self):
        self.reachedAccept = False
        self.actualState = 0
        alphabet = self.afd.getAlphabet()
        table = self.afd.getTable()

        if(self.string[self.actualSymbolPos] == endString):
            return Token.END

        self.stack.append(self.actualSymbolPos)
        self.beginLexPos = self.actualSymbolPos

        while(self.string[self.actualSymbolPos] != endString):
            self.alphabetIndex = -1

            for i in range(0, len(alphabet)):
                if(alphabet[i] == self.string[self.actualSymbolPos]):
                    self.alphabetIndex = i
                    break

            if(self.alphabetIndex == -1):
                if(self.reachedAccept == False):
                    self.lex = self.string[self.actualSymbolPos:self.actualSymbolPos]
                    self.actualSymbolPos += self.beginLexPos
                    return Token.ERROR

                self.lex = self.string[self.beginLexPos:self.endLexPos]
                self.actualSymbolPos += self.endLexPos
                return self.token

            self.actualState = table[self.actualState][self.alphabetIndex]

            if(self.actualState != -1):
                if(table[self.actualState][len(alphabet)] != 1):
                    self.token = table[self.actualState][len(alphabet)]
                    self.reachedAccept = True
                    self.endLexPos = self.actualSymbolPos
                self.actualSymbolPos += 1
            else:
                if(self.reachedAccept == False):
                    self.lex = self.string[self.actualSymbolPos:self.actualSymbolPos]
                    self.actualSymbolPos += self.beginLexPos
                    return Token.ERROR

                self.lex = self.string[self.beginLexPos:self.endLexPos]
                self.actualSymbolPos += self.endLexPos
                return self.token