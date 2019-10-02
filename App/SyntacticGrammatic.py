#!python3
from Node import Node
from Token import Token
from Lexer import Lexer

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
        if(self.ListaReglas()):
            return True
        return False

    def ListaReglas(self):
        if(self.Regla()):
            token = self.lex.getToken()

            if(token == Token.SEMICOLON): 
                if(self.ListaReglasP()):
                    return True
        return False

    def ListaReglasP(self): 
        E = self.lex.getStatus()

        if(self.Regla()):
            token = self.lex.getToken()

            if(token == Token.SEMICOLON):
                if(self.ListaReglasP()):
                    return True
            return False

        self.lex.setStatus(E)
        return True

    def Regla(self):
        ladoI = (False, None)
        ladoI = self.LadoIzquierdo(ladoI) #Boolean - String

        if(ladoI[0]):
            token = self.lex.getToken()

            if(token == Token.ARROW):
                ladoI = self.LadosDerechos(ladoI) #Boolean - String

                if(ladoI[0]):
                    return True
        return False

    def LadoIzquierdo(self, s): #Boolean - String
        token = self.lex.getToken()

        if(token == Token.SYMBOL):
            return (True, self.lex.getLexem())
        return (False, s[1])

    def LadosDerechos(self, s): #Boolen - String
        N = (False, None)
        N = self.ListaSimbolos(N) #Boolean - Node

        if(N[0]):
            self.arrRules.append(Node(s[1], N[1]))
            s = self.LadosDerechosP(s)

            if(s[0]):
                return (True, s[1])
        return (False, s[1])

    def LadosDerechosP(self, s): #Boolean - String
        token = self.lex.getToken()

        if(token == Token.OR):
            N = (False, None)
            N = self.ListaSimbolos(N) #Boolean - Node

            if(N[0]):
                self.arrRules.append(Node(s[1], N[1]))
                s = self.LadosDerechosP(s) #Boolean - String

                if(s[0]): 
                    return (True, s[1])
            return (False, s[1])

        self.lex.returnToken()
        return (True, s[1])

    def ListaSimbolos(self, N): #Boolean - Node
        N2 = (False, None)
        token = self.lex.getToken()
    
        if(token == Token.SYMBOL):
            N = (N[0], Node(self.lex.getLexem(), None))
            N2 = self.ListaSimbolosP(N2) #Boolean - Node

            if(N2[0]):
                N[1].setNext(N2[1])
                return (True, N[1])
        return (False, N[1])

    def ListaSimbolosP(self, N):  #Boolean - Node
        N2 = (False, None)
        token = self.lex.getToken()

        if(token == Token.SYMBOL):
            N = (N[0], Node(self.lex.getLexem(), None))
            N2 = self.ListaSimbolosP(N2) #Boolean - Node

            if(N2[0]):
                N[1].setNext(N2[1])
                return (True, N[1])
            return (False, N[1])

        self.lex.returnToken()
        return (True, None)