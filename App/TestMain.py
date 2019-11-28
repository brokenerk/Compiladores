#!python3
from NFA import NFA
from DFA import DFA
from Token import Token
from Lexer import Lexer
from LL1 import LL1
from LR0 import LR0
from LR1 import LR1
from SyntacticNFA import SyntacticNFA
from SyntacticGrammar import SyntacticGrammar
epsilon = '\u03B5'

if __name__ == "__main__":
	#DFA for grammars
    afn1 = NFA.createBasic('a', 'z')
    afn2 = NFA.createBasic('A', 'Z')
    afn3 = NFA.createBasic('0', '9')
    afn4 = NFA.createBasic('+')
    afn5 = NFA.createBasic('-')
    afn6 = NFA.createBasic('*')
    afn7 = NFA.createBasic('/')
    afn8 = NFA.createBasic('=')
    afn9 = NFA.createBasic('(')
    afn10 = NFA.createBasic(')')
    afn11 = NFA.createBasic(',')
    afn12 = NFA.createBasic('.')
    afn13 = NFA.createBasic('?')
    afnA = afn1.join(afn2).join(afn3).join(afn4).join(afn5).join(afn6).join(afn7).join(afn8).join(afn9).join(afn10).join(afn11).join(afn12).join(afn13)
    afn13 = NFA.createBasic('A', 'Z')
    afn14 = NFA.createBasic('a', 'z')
    afn15 = NFA.createBasic ("'")
    afn16 = NFA.createBasic('_')
    afnB = afn13.join(afn14).join(afn15).join(afn16)
    afnC = afnB.kleeneClosure()
    afnD = afnA.concat(afnC)
    afnD.setToken(Token.SYMBOL)

    afn17 = NFA.createBasic('-')
    afn18 = NFA.createBasic('>')
    afnE = afn17.concat(afn18)
    afnE.setToken(Token.ARROW)

    afn19 = NFA.createBasic(';')
    afn19.setToken(Token.SEMICOLON)

    afn20 = NFA.createBasic('|')
    afn20.setToken(Token.OR)

    afn21 = NFA.createBasic(' ')
    afn21.setToken(Token.SPACE)

    automatota = NFA.specialJoin(set([afnD, afnE, afn11, afn12, afn19, afn20, afn21]))
    afd = automatota.convertToDFA()
    #afd.displayTable()

    #DFA for strings
    afn1 = NFA.createBasic('A', 'Z')
    afn2 = NFA.createBasic('a', 'z')
    afnB = afn1.join(afn2).kleeneClosure()
    afnB.setToken(Token.SYMBOL)

    afn3 = NFA.createBasic('-')
    afn4 = NFA.createBasic('>')
    afnE = afn3.concat(afn4)
    afnE.setToken(Token.ARROW)

    afn5 = NFA.createBasic(';')
    afn5.setToken(Token.SEMICOLON)

    afn6 = NFA.createBasic('|')
    afn6.setToken(Token.OR)

    afn22 = NFA.createBasic('0', '9')
    afn23 = NFA.createBasic('.')
    afn24 = NFA.createBasic('0', '9')
    afn25 = afn23.concat(afn22.positiveClosure()).optional()
    afnF = afn24.positiveClosure().concat(afn25)
    afnF.setToken(Token.NUM)

    afn26 = NFA.createBasic('&')
    afn26.setToken(Token.CONCAT)

    afn27 = NFA.createBasic(',')
    afn27.setToken(Token.COMMA)

    afn28 = NFA.createBasic('i')
    afn29 = NFA.createBasic('d')
    afnG = afn28.concat(afn29)
    afnG.setToken(Token.ID)

    automatota2 = NFA.specialJoin(set([afnB, afnE, afn5, afn6, afnF, afn26, afn27, afnG]))
    afd2 = automatota2.convertToDFA()
    afd2.displayTable()

    #Las reglas se ingresan todas en 1 sola linea, separadas por punto y coma
    archivo = open("grammar7.txt", "r")

    print("Leeyendo Gramatica...")
    string = ""
    #Epsilon is a space ' '
    for linea in archivo:
        string = string + linea.rstrip("\n")

    archivo.close()
    
    print("\nAnalizando cadena: " + string)
    lex = Lexer(afd, string)
    #lex.display()

    print("Lexico OK. Analizando sintacticamente...")
    syn = SyntacticGrammar(lex)

    print("\nGramatica construida: ")
    grammar = syn.start()
    if(grammar):
        ruleNumber = 1
        for r in grammar:
            print("{} ".format(ruleNumber), end = '')
            r.displayRule()
            ruleNumber += 1

        c = "43315.453*(23.4632153+5501321)"
        lex2 = Lexer(afd2, c)

        lr1 = LR1(grammar, lex2)

        if(lr1.isLR1()):
            print("Es LR1")
            lr1.displayTable(0)

            res = lr1.analyze(c)
            lr1.displayTable(1)
            if(res):
                print("\n" + c + " pertenece a la gramatica")
            else:
                print("\n" + c + " no pertenece a la gramatica")
        else:
            print("No es LR1")

        '''
        #Analysis
        print("\nAnalisis LL(1)")
        c = "435.453+3453*(23.3-550)"
        lex2 = Lexer(afd2, c)
        #lex2.display()

        ll1 = LL1(grammar, lex2)
       
        if(ll1.isLL1()):
            print("Gramatica compatible con LL(1)")

            ll1.displayTable(0)
            res = ll1.analyze(c)
            ll1.displayTable(1)
            if(res):
                print("\n" + c + " pertenece a la gramatica")
            else:
                print("\n" + c + " no pertenece a la gramatica")
        else:
            print("\nERROR. La gramatica no es compatible con LL(1)")
    afn1 = NFA.createBasic('a', 'z')
    afn1.setToken(Token.SYMBOL_LOWER)
    afn2 = NFA.createBasic('A', 'Z')
    afn2.setToken(Token.SYMBOL_UPPER)
    afn3 = NFA.createBasic('0', '9')
    afn3.setToken(Token.NUM)
    afn4 = NFA.createBasic('|')
    afn4.setToken(Token.JOIN)
    afn5 = NFA.createBasic('&')
    afn5.setToken(Token.CONCAT)
    afn6 = NFA.createBasic('+')
    afn6.setToken(Token.POSCLO)
    afn7 = NFA.createBasic('-')
    afn7.setToken(Token.DASH)
    afn8 = NFA.createBasic('.')
    afn8.setToken(Token.POINT)
    afn9 = NFA.createBasic('?')
    afn9.setToken(Token.OPTIONAL)
    afn10 = NFA.createBasic('*')
    afn10.setToken(Token.KLEEN)
    afn11 = NFA.createBasic('(')
    afn11.setToken(Token.PAR_L)
    afn12 = NFA.createBasic(')')
    afn12.setToken(Token.PAR_R)
    afn13 = NFA.createBasic ('[')
    afn13.setToken(Token.SQUBRACK_L)
    afn14 = NFA.createBasic (']')
    afn14.setToken(Token.SQUBRACK_R)
    afnp = NFA.createBasic('"')
    afnq = NFA.createBasic('+')
    afn15 = afnp.concat(afnq)
    afn15.setToken(Token.PLUS)
    afnp3 = NFA.createBasic('"')
    afnq3 = NFA.createBasic('-')
    afn16 = afnp3.concat(afnq3)
    afn16.setToken(Token.MINUS)
    automatota = NFA.specialJoin(set([afn1, afn2, afn3, afn4, afn5, afn6, afn7, afn8, afn9, afn10, afn11, afn12, afn13, afn14, afn15, afn16]))
    afd = automatota.convertToDFA()
    archivo = open("er.txt", "r")
    afns = set([])
    print("Leeyendo ER...")
    print("")
    for linea in archivo:
        print("")
        print(linea)
        stringAux = linea.split(' ')
        lex = Lexer(afd, stringAux[0])
        syn = SyntacticNFA(lex)
        afnAux = syn.start()
        if(afnAux == False):
            exit()
                        
        afnAux.setToken(int(stringAux[1]))
        afns.add(afnAux)
    archivo.close()
    automatotaER = NFA.specialJoin(afns)
    afdER = automatotaER.convertToDFA()
    print("")
    print("AFD Resultante:")
    afdER.displayTable()
    print("")
    stringPrueba = "SSS+965+TTT+74.96STTSLDLDSSLDDDT+++179SSLDLLL"
    print("Lexer: " + stringPrueba)
    lex2 = Lexer(afdER, stringPrueba)
    lex2.display()
    '''