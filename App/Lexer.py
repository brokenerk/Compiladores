#!python3
from AFD import AFD
from Token import Token
from collections import deque
end = '\0'

class Lexer:
    #Constructor
    def __init__(self, afd, string):
        self.afd = afd                  #AFD
        self.string = string + end      #String
        self.reachedAccept = False      #Boolean
        self.actualState = 0            #Integer
        self.actualSymbolPos = 0        #Integer
        self.beginLexPos = -1           #Integer
        self.endLexPos = -1             #Integer
        self.stack = deque()            #Stack<Integer>
        self.status = -1                
        self.token = -1                 #Integer
        self.lex = ""                   #String

    def getToken(self):
        return self.token   

    def returnToken(self):
        return

    def getStatus(self):
        return

    def setStatus(self):
        return

    def yylex(self):
        alphabet = self.afd.getAlphabet()
        table = self.afd.getTable()

        if(self.string[self.actualSymbolPos] == end):
            return Token.END

        self.stack.append(self.actualSymbolPos)
        self.beginLexPos = self.actualSymbolPos

        while(self.string[self.actualSymbolPos] != end):
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
                print(self.lex)
                self.actualSymbolPos += self.endLexPos
                return self.token



                

        


            






