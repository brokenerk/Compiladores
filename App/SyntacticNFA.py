# !/python3
from NFA import NFA
from Token import Token
from Lexer import Lexer

class SyntacticNFA:
    #Constructor
    def __init__(self, lex):
        self.lex = lex                                                                
    
    def start(self):
        f = (False, NFA(None, None, None, None))
        f = self.E(f)
        if(f[0]):
            print('... AFN construido')
            return f[1]
        else:
            print('... ER No valida, saliendo.')
            return False

    def E(self, f):
        f = self.T(f)
        if(f[0]):
            f = self.Ep(f)
            if(f[0]):
                return (True, f[1])
        return (False, f)

    def Ep(self, f):
        f2 = (False, NFA(None, None, None, None))
        tok = self.lex.getToken()  
        lexema = self.lex.getLexem()  
        if(tok == Token.JOIN): #OR
            f2 = self.T(f2)
            if(f2[0]):
                afna = f[1].join(f2[1])
                f = (f[0], afna)
                f = self.Ep(f)
                if(f[0]):
                    return (True, f[1])
            return (False, f[1])
        self.lex.returnLexem()
        self.lex.returnToken()
        return (True, f[1])

    def T(self, f):
        f = self.C(f)
        if(f[0]):
            f = self.Tp(f)
            if(f[0]):
                return (True, f[1])
        return (False, f[1])

    def Tp(self, f):
        fn2 = (False, NFA(None, None, None, None))
        tok = self.lex.getToken()
        lexema = self.lex.getLexem()
        if(tok == Token.CONCAT): #'CONC'
            fn2 = self.C(fn2)
            if(fn2[0]):
                afna = f[1].concat(fn2[1])
                f = (f[0], afna)
                f = self.Tp(f)
                if(f[0]):
                    return (True, f[1])
            return (False, f[1])
        self.lex.returnToken()
        self.lex.returnLexem()
        return (True, f[1])

    def C(self, f) :
        f = self.F(f)
        if(f[0]):
            f = self.Cp(f)
            if(f[0]): 
                return (True, f[1])
        return (False, f[1])

    def Cp (self, f):
        tok = self.lex.getToken() 
        lexema = self.lex.getLexem() 
        if(tok == Token.KLEEN): #kleen
            afna = f[1].kleeneClosure()
            f = (f[0], afna)
            f = self.Cp(f)
            if(f[1]):
                return (True, f[1])
            return (False, f[1])
        elif(tok == Token.POSCLO): #Positive
            afna = f[1].positiveClosure()
            f = (f[0], afna)
            f = self.Cp(f)
            if(f[0]):
                return (True, f[1])
            return (False, f[1])
        elif(tok == Token.OPTIONAL): #'OPC'
            afna = f[1].optional()
            f = (f[0], afna)
            f = self.Cp(f)
            if (f[0]):
                return (True, f[1])
            return (False, f[1])
        self.lex.returnToken()
        self.lex.returnLexem()
        return (True, f[1])

    def F(self, f):
        tok = self.lex.getToken()
        lexema = self.lex.getLexem()

        if(tok == Token.PAR_L): #'PAR_I' 
            f = self.E(f)
            if(f[0]):
                tk = self.lex.getToken()
                lexem = self.lex.getLexem()
                if(tk == Token.PAR_R): #'PAR_D'
                    return (True, f[1])

        elif(tok == Token.SQUBRACK_L): #[
            tk = self.lex.getToken()
            lxm = self.lex.getLexem()

            if(tk == Token.SYMBOL_LOWER): #a
                tk2 = self.lex.getToken()
                lxm2 = self.lex.getLexem()

                if(tk2 == Token.DASH): # -
                    tk3 = self.lex.getToken()
                    lxm3 = self.lex.getLexem()

                    if(tk3 == Token.SYMBOL_LOWER): #z
                        tk4 = self.lex.getToken()
                        lxm4 = self.lex.getLexem()

                        if(tk4 == Token.SQUBRACK_R): #]
                            af = NFA.createBasic(lxm, lxm3) #[a-z]
                            return (True, af)

            elif(tk == Token.SYMBOL_UPPER): #A
                tk2 = self.lex.getToken()
                lxm2 = self.lex.getLexem()

                if(tk2 == Token.DASH): # -
                    tk3 = self.lex.getToken()
                    lxm3 = self.lex.getLexem()

                    if(tk3 == Token.SYMBOL_UPPER): #Z
                        tk4 = self.lex.getToken()
                        lxm4 = self.lex.getLexem()

                        if(tk4 == Token.SQUBRACK_R): #]
                            af = NFA.createBasic(lxm, lxm3) #[A-Z]
                            return (True, af)

            elif(tk == Token.NUM): #0
                tk2 = self.lex.getToken()
                lxm2 = self.lex.getLexem()

                if(tk2 == Token.DASH): # -
                    tk3 = self.lex.getToken()
                    lxm3 = self.lex.getLexem()

                    if(tk3 == Token.NUM): #9
                        tk4 = self.lex.getToken()
                        lxm4 = self.lex.getLexem()

                        if(tk4 == Token.SQUBRACK_R): #]
                            af = NFA.createBasic(lxm, lxm3) #[0-9]
                            return (True, af)

        elif(tok == Token.SYMBOL_UPPER or tok == Token.SYMBOL_LOWER): # Letters
            af = NFA.createBasic(lexema)
            return (True, af)

        elif(tok == Token.NUM): # 0123
            af = NFA.createBasic(lexema)
            return (True, af)

        elif(tok == Token.POINT): # .
                af = NFA.createBasic(lexema)
                return (True, af)

        elif(tok == Token.PLUS): # "+
                af = NFA.createBasic(lexema[1])
                return (True, af)

        elif(tok == Token.PROD): # "*
                af = NFA.createBasic(lexema[1])
                return (True, af)

        elif(tok == Token.MINUS): # "-
                af = NFA.createBasic(lexema[1])
                return (True, af)

        elif(tok == Token.DIV): # /
                af = NFA.createBasic(lexema)
                return (True, af)

        elif(tok == Token.EQUALS): # =
                af = NFA.createBasic(lexema)
                return (True, af)

        return (False, f[1])