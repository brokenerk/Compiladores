#!python3

class NFA:
    def __init__ (self,grammars):
        self.grammars = grammars

    def G (self):
        if(ListaReglas()):
            return true
        return false

    def ListaReglas(self):
	    int Token
	    if(Regla()):
		Token = Lexic.geToken()
		if(Token == PC): 
			if(ListaReglasP()):
				return true
		    return false
	    return false


    def ListaReglasP(self): 
	    EdoAnaliz E
	    int Token
	    E = Lexic.getEdoAnalizador()
	    if(Regla()):
		    Token = Lexic.getToken()
		    if(Token == PC):
			    if(ListaReglasP()):
				    return true
		    return false
	    Lexic.setEdoAnalizador(E)
	    return true

    def Regla(self):
	    int Token
	    String ladoI
	    if(LadoIzquierdo(ladoI)):
		    Token = Lexic.getToken()
		    if(Token == FLECHA):
			    if(LadosDerechos(ladoI)):
				    return true
	    return false

    def LadoIzquierdo(self,String s): 
	    int Token
	    Token = Lexic.getToken()
	    if(Token == SIMBOLO):
		    s = Lexic.getLexema()
		    return true
	    return false

    def LadosDerechos(self,String s):
	    Nodo N
	    if(ListaSimbolos(N)):
		    ArrReglas[IndiceArr].simb = s
		    ArrReglas[IndiceArr].Ap = N
		    IndiceArr+=1
		    if(LadosDerechosP(s)):
			    return true
	    return false

    def LadosDerechosP(self,String s): 
    	int Token
    	Nodo N
    	Token = Lexic.getToken()
    	if(Token == OR):
    		if(ListaSimbolos(N)):
    			ArrReglas[IndiceArr].simb = s
    			ArrReglas[IndiceArr].Ap = N
    			IndiceArr+=1
    			if(LadosDerechosP(s)): 
    				return true
    		return false
    	Lexic.regresarToken()
    	return true

    def ListaSimbolos(self,Nodo N):
    	int Token
    	Nodo N2
    	Token = Lexic.getToken()
    
    	if(Token == SIMBOLO):
    		Nodo N = new Nodo(Lexic.getLexema())
    		if(ListaSimbolosP(N2)):
    			N.sig = N2
    			return true
    	return false

    def ListaSimbolosP(self,Nodo N): 
    	int Token
    	Nodo N2
    	Token = Lexic.getToken()
    	if(Token == SIMBOLO):
    		Nodo N = new Nodo(Lexic.getLexema())
    		if(ListaSimbolosP(N2)):
    			N.sig = N2
    			return true
    	N = NULL
    	Lexic.regresarToken()
    	return false