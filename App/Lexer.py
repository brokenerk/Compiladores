#!python3
from AFD import AFD
from Token import Token
from collections import deque
endString = '\0'

class Lexer:
    #Constructor
    def __init__(self, alphabet, table, string):
        self.alphabet = alphabet 				#List<String>
        self.table = table 						#List<List<String>>
        self.string = string + endString        #String
        self.actualSymbolPos = 0                #Integer
        self.reachedAccept = False              #Boolean
        self.actualState = 0                    #Integer
        self.beginLexPos = -1                   #Integer
        self.endLexPos = -1                     #Integer
        self.stack = deque()                    #Stack<Integer>
        self.token = -1                         #Integer
        self.lex = ""                           #String

    #Parameters: Nothing
    #Return: Integer
    def getActualSymbolPos(self):
        return self.actualSymbolPos
    #Parameters: Integer
    #Return: Nothing
    def setActualSymbolPos(self, actualSymbolPos):
        self.actualSymbolPos = actualSymbolPos

    #Parameters: Nothing
    #Return: Boolean
    def getReachedAccept(self):
        return self.reachedAccept
    #Parameters: Boolean
    #Return: Nothing
    def setReachedAccept(self, reachedAccept):
        self.reachedAccept = reachedAccept

    #Parameters: Nothing
    #Return: Integer
    def getBeginLexPos(self):
        return self.beginLexPos
    #Parameters: Integer
    #Return: Nothing
    def setBeginLexPos(self, beginLexPos):
        self.beginLexPos = beginLexPos

    #Parameters: Nothing
    #Return: Integer
    def getEndLexPos(self):
        return self.endLexPos
    #Parameters: Integer
    #Return: Nothing
    def setEndLexPos(self, endLexPos):
        self.endLexPos = endLexPos

    #Parameters: Nothing
    #Return: Integer
    def getToken(self):
        return self.token  
    #Parameters: Integer
    #Return: Nothing
    def setToken(self, token):
        self.token = token 

    def returnToken(self):
        return

    #Parameters: Nothing
    #Return: Integer
    def yylex(self):
        self.actualState = 0
        self.reachedAccept = False

        if(self.string[self.actualSymbolPos] == endString):
            return Token.END

        self.stack.append(self.actualSymbolPos)
        self.beginLexPos = self.actualSymbolPos

        while(self.string[self.actualSymbolPos] != endString):
            self.alphabetIndex = -1

            for i in range(0, len(self.alphabet)):
                if(self.alphabet[i] == self.string[self.actualSymbolPos]):
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

            self.actualState = self.table[self.actualState][self.alphabetIndex]

            if(self.actualState != -1):
                if(self.table[self.actualState][len(self.alphabet)] != 1):
                    self.token = self.table[self.actualState][len(self.alphabet)]
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