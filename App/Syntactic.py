# !/python3
from AFN import AFN
from Token import Token
from Lexer import Lexer

class SyntacticAfn:
    #Constructor
    def __init__(self , lex):
        self.nonterminalSymbols = set( ['E','Ep','T','Tp','C','Cp','F'] ) 
        self.lex = lex                                                                
    
    def start (self):
        F = ( False , AFN(None,None,None,None) )
        F = self.E( F )
        if F[0]:
            return F[1]
        else:
            print('ER No valida')

    def E ( self , F ):
        F = self.T ( F )
        if F[0]:
            F = self.Ep( F )
            if F[0]:
                return (True,F[1])
        return (False,F)

    def Ep ( self, F):
        f2 = ( False, AFN(None,None,None,None) )
        tok = self.lex.getToken()  
        lexema = self.lex.getLexem()  
        if tok == 130: #OR
            f2 = self.T ( f2 )
            if f2[0]:
                print('JOIN')
                afna =F[1].join( f2[1] )
                F = ( F[0] , afna)
                F = self.Ep(F)
                if F[0]:
                    return (True,F[1])
            return (False,F[1])
        self.lex.returnLexem()
        self.lex.returnToken()
        return (True,F[1]) #False

    def T (self ,F):
        F = self.C (F)
        if F[0]:
            F = self.Tp(F)
            if F[0]:
                return ( True,F[1] )
        return (False,F[1])

    def Tp (self , F):
        fn2 = ( False, AFN ( None,None,None,None ) )
        tok = self.lex.getToken()
        lexema = self.lex.getLexem()
        if tok == 140: #'CONC'
            fn2 = self.C(fn2)
            if fn2[0]:
                print('Concat')
                afna = F[1].concat(fn2[1])
                F = ( F[0] , afna)
                F = self.Tp(F)
                if F[0]:
                    return ( True,F[1] )
            return ( False,F[1] )
        self.lex.returnToken()
        self.lex.returnLexem()
        return  ( True,F[1] )

    def C ( self,F ) :
        F = self.F(F)
        if F[0]:
            F = self.Cp( F )
            if F[0]: 
                return (True,F[1])
        return ( False,F[1] )

    def Cp (self,F):
        tok = self.lex.getToken() 
        lexema = self.lex.getLexem() 
        if tok == 190: #kleen
            afna = F[1].kleeneClosure()
            F = ( F[0] , afna)
            F = self.Cp(F)
            if F[1]:
                return ( True,F[1] )
            return ( False, F[1] )
        if tok == 150: #Positive
            afna = F[1].positiveClosure()
            F = ( F[0] , afna)
            F = self.Cp( F )
            if F[0]:
                return ( True,F[1] )
            return ( False,F[1] )
        if tok == 180: #'OPC'
            print('Optional')
            afna = F[1].optional()
            F = ( F[0] , afna)
            F = self.Cp(F)
            if F[0]:
                return ( True,F[1] )
            return ( False, F[1] )

        self.lex.returnToken()
        self.lex.returnLexem()
        return ( True, F[1] )

    def F (self,F):
        tok = self.lex.getToken()
        lexema = self.lex.getLexem()
        if ( tok == 200): #'PAR_I' 
            F = self.E(F)
            if F[0] :
                tk = self.lex.getToken()
                lexem = self.lex.getLexem()
                if ( tk == 210): #'PAR_D'
                    return ( True,F[1] )
            return ( False, F[1] )

        if ( tok == 100): #SIMB
            af = AFN.createBasic(lexema)
            return ( True, af )
        
        if ( tok == 110): #SIMB UPPER
            af = AFN.createBasic(lexema)
            return ( True, af )

        if ( tok == 101): #[a-z]
            af = AFN.createBasic(lexema[1],lexema[3])
            return ( True, af )

        if ( tok == 111): #[A-Z]
            af = AFN.createBasic(lexema[1],lexema[3])
            return ( True, af )

        if ( tok == 120): #NUM
            af = AFN.createBasic(lexema)
            return ( True, af )

        if ( tok == 121): #[0-9]
            af = AFN.createBasic(lexema[1],lexema[3])
            return ( True, af )

        if ( tok == 170): # .
            af = AFN.createBasic(lexema)
            return ( True, af )