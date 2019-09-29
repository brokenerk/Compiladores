from collections import deque

class LexerStatus:
    def __init__(self, actualSymbolPos, reachedAccept, actualState, beginLexPos, endLexPos, stack, token, lexem):
        self.actualSymbolPos = actualSymbolPos      #Integer
        self.reachedAccept = reachedAccept          #Boolean
        self.actualState = actualState              #Integer
        self.beginLexPos = beginLexPos              #Integer
        self.endLexPos = endLexPos                  #Integer
        self.stack = stack                          #Stack<Integer>
        self.token = token                          #Integer
        self.lexem = lexem                          #String

    def getActualSymbolPos(self):
        return self.actualSymbolPos

    def getReachedAccept(self):
        return self.reachedAccept

    def getActualState(self):
        return self.actualState

    def getBeginLexPos(self):
        return self.beginLexPos

    def getEndLexPos(self):
        return self.endLexPos

    def getStack(self):
        return self.stack

    def getToken(self):
        return self.token

    def getLexem(self):
        return self.lexem
