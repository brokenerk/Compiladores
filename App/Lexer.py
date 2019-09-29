#!python3
from DFA import DFA
from Token import Token
from LexerStatus import LexerStatus
from collections import deque
endString = '\0'

class Lexer:
    #Constructor
    def __init__(self, afd, string):
        self.alphabet = afd.getAlphabet()       #List<String>
        self.table = afd.getTable()				#List<List<String>>
        self.string = string + endString        #String
        self.actualSymbolPos = 0                #Integer
        self.reachedAccept = False              #Boolean
        self.actualState = 0                    #Integer
        self.beginLexPos = 0                    #Integer
        self.endLexPos = 0                      #Integer
        self.stack = deque()                    #Stack<Integer>
        self.token = -1                         #Integer
        self.lexem = ""                         #String

    #Parameters: Nothing
    #Return: Integer
    def getToken(self):
        self.yylex()
        return self.token

    #Parameters: Nothing
    #Return: Nothing
    def returnToken(self):
        self.actualSymbolPos = self.stack.pop()

    #Parameters: Nothing
    #Return: String
    def getLexem(self):
        return self.lexem

    #Parameters: Nothing
    #Return: Status
    def getStatus(self):
        return LexerStatus(self.actualSymbolPos, self.reachedAccept, self.actualState, self.beginLexPos, self.endLexPos, self.stack.copy(), self.token, self.lexem)
        
    #Parameters: Status
    #Return: Nothing
    def setStatus(self, s):
        self.actualSymbolPos = s.getActualSymbolPos()
        self.reachedAccept = s.getReachedAccept()
        self.actualState = s.getActualState()
        self.beginLexPos = s.getBeginLexPos()
        self.endLexPos = s.getEndLexPos()
        self.stack = s.getStack()
        self.token = s.getToken()
        self.lexem = s.getLexem()

   	#Parameters: Nothing
    #Return: Nothing
    def display(self):
        res = self.yylex()
        while(res != Token.END):
            print(str(self.token) + ": " + self.lexem)
            res = self.yylex()
            
    #Parameters: Nothing
    #Return: Integer
    def yylex(self):
        self.actualState = 0
        self.reachedAccept = False

        if(self.string[self.actualSymbolPos] == endString):
            self.token = Token.END
            return Token.END

        self.stack.append(self.actualSymbolPos)
        self.beginLexPos = self.actualSymbolPos

        while self.string[self.actualSymbolPos] != endString:
            alphabetIndex = -1
            for i in range(0, len(self.alphabet)):
                if(len(self.alphabet[i]) > 2):
                    if(self.alphabet[i][0] <= self.string[self.actualSymbolPos] <= self.alphabet[i][2]):
                        alphabetIndex = i
                        break   
                else:
                    if(self.string[self.actualSymbolPos] == self.alphabet[i]):
                        alphabetIndex = i
                        break

            if(alphabetIndex == -1):
                if(self.reachedAccept == False):
                    self.lexem = self.string[self.actualSymbolPos:self.actualSymbolPos + 1] #substring
                    self.actualSymbolPos = self.beginLexPos + 1
                    self.token = Token.ERROR
                    return Token.ERROR

                self.lexem = self.string[self.beginLexPos:self.endLexPos + 1] #substring
                self.actualSymbolPos = self.endLexPos + 1
                return self.token

            self.actualState = self.table[self.actualState][alphabetIndex]

            if(self.actualState != -1):
                if(self.table[self.actualState][len(self.alphabet)] != 1):
                    self.token = self.table[self.actualState][len(self.alphabet)]
                    self.reachedAccept = True
                    self.endLexPos = self.actualSymbolPos

                self.actualSymbolPos += 1
                self.lexem = self.string[self.beginLexPos:self.endLexPos + 1] #substring
            else:
                if(self.reachedAccept == False):
                    self.lexem = self.string[self.actualSymbolPos:self.actualSymbolPos + 1] #substring
                    self.actualSymbolPos = self.beginLexPos + 1
                    self.token = Token.ERROR
                    return Token.ERROR

                self.lexem = self.string[self.beginLexPos:self.endLexPos + 1] #substring
                self.actualSymbolPos = self.endLexPos + 1
                return self.token