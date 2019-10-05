#!python3
from Node import Node
from Token import Token
from Lexer import Lexer
#Epsilon is a space ' '
class SyntacticGrammatic:
    #Constructor
    def __init__(self, lex):
        self.lex = lex      #Lexer
        self.arrRules = []  #List<Node>

    def start(self):
        if(self.G()):
            return self.arrRules
        else:
            print("... Error al construir la gramatica, saliendo.")
            return False

    def G(self):
        if(self.RulesList()):
            return True
        return False

    def RulesList(self):
        if(self.Rule()):
            token = self.lex.getToken()

            if(token == Token.SEMICOLON): 
                if(self.RulesListP()):
                    return True
        return False

    def RulesListP(self): 
        status = self.lex.getStatus()

        if(self.Rule()):
            token = self.lex.getToken()

            if(token == Token.SEMICOLON):
                if(self.RulesListP()):
                    return True
            return False

        self.lex.setStatus(status)
        return True

    def Rule(self):
        leftS = (False, None)
        leftS = self.LeftSide(leftS) #Boolean - String

        if(leftS[0]):
            token = self.lex.getToken()

            if(token == Token.ARROW):
                leftS = self.RightSides(leftS) #Boolean - String

                if(leftS[0]):
                    return True
        return False

    def LeftSide(self, s): #Boolean - String
        token = self.lex.getToken()

        if(token == Token.SYMBOL):
            return (True, self.lex.getLexem())
        return (False, s[1])

    def RightSides(self, s): #Boolen - String
        N = (False, None)
        N = self.SymbolsList(N) #Boolean - Node

        if(N[0]):
            self.arrRules.append(Node(s[1], N[1]))
            s = self.RightSidesP(s)

            if(s[0]):
                return (True, s[1])
        return (False, s[1])

    def RightSidesP(self, s): #Boolean - String
        token = self.lex.getToken()

        if(token == Token.OR):
            N = (False, None)
            N = self.SymbolsList(N) #Boolean - Node

            if(N[0]):
                self.arrRules.append(Node(s[1], N[1]))
                s = self.RightSidesP(s) #Boolean - String

                if(s[0]): 
                    return (True, s[1])
            return (False, s[1])

        self.lex.returnToken()
        return (True, s[1])

    def SymbolsList(self, N): #Boolean - Node
        N2 = (False, None)
        token = self.lex.getToken()
    
        if(token == Token.SYMBOL):
            N = (N[0], Node(self.lex.getLexem(), None))
            N2 = self.SymbolsListP(N2) #Boolean - Node

            if(N2[0]):
                N[1].setNext(N2[1])
                return (True, N[1])
        return (False, N[1])

    def SymbolsListP(self, N):  #Boolean - Node
        N2 = (False, None)
        token = self.lex.getToken()

        if(token == Token.SYMBOL):
            N = (N[0], Node(self.lex.getLexem(), None))
            N2 = self.SymbolsListP(N2) #Boolean - Node

            if(N2[0]):
                N[1].setNext(N2[1])
                return (True, N[1])
            return (False, N[1])

        self.lex.returnToken()
        return (True, None)