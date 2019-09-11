# !/python3
from AFN import AFN
from Token import Token
from Lexer import Lexer

epsilon = '\u03B5'

class SyntacticAfn:
    #Constructor
    def __init__(self):
        self.nonterminalSymbols = set( ['E','Ep','T','Tp','C','Cp','F'] )
        self.terminalSymbols = set ( ['OR','&','+','*','?','SIMB',espsilon] )
        
    def E ( self, F ):
        if ( T(F) ):
            if ( Ep(F) ):
                return True
        return False

    def Ep (self, F):
        f2 = AFN()
        tok = Lexer.getToken()
        if tok == 'OR':
            if ( T(f2) ):
                F.join(f2)
                if ( Ep(f) ):
                    return True
            return False
        Lexer.returnToken()
        return True

    def T (self, F):
        if ( C(F) ):
            if ( Tp(F) ):
                return True
        return False

    def Tp (self, F):
        f2 = AFN()
        tok = Lexer.getToken()
        if ( tok == 'CONC'):
            if ( C(f2) ):
                F.concat(f2)
                if(Tp(F)):
                    return True
            return False
        Lexer.getToken()
        return True
