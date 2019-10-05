#!python3
from NFA import NFA
from DFA import DFA
from Token import Token
from Lexer import Lexer
from SyntacticNFA import SyntacticNFA
from SyntacticGrammatic import SyntacticGrammatic
epsilon = '\u03B5'

if __name__ == "__main__":
    afn1 = NFA.createBasic('a', 'z')
    afn2 = NFA.createBasic('A', 'Z')
    afn3 = NFA.createBasic('+')
    afn4 = NFA.createBasic('-')
    afn5 = NFA.createBasic('*')
    afn6 = NFA.createBasic('/')
    afn61 = NFA.createBasic(' ')
    afnA = afn1.join(afn2).join(afn3).join(afn4).join(afn5).join(afn6).join(afn61)

    afn7 = NFA.createBasic('a', 'z')
    afn8 = NFA.createBasic('A', 'Z')
    afn9 = NFA.createBasic('0', '9')
    afn10 = NFA.createBasic ("'")
    afn11 = NFA.createBasic('_')

    afnB = afn7.join(afn8).join(afn9).join(afn10).join(afn11)
    afnC = afnB.kleeneClosure()

    afnD = afnA.concat(afnC)
    afnD.setToken(Token.SYMBOL)

    afn12 = NFA.createBasic('-')
    afn13 = NFA.createBasic('>')
    afnE = afn12.concat(afn13)
    afnE.setToken(Token.ARROW)

    afn14 = NFA.createBasic(';')
    afn14.setToken(Token.SEMICOLON)

    afn15 = NFA.createBasic('|')
    afn15.setToken(Token.OR)

    automatota = NFA.specialJoin(set([afnD, afnE, afn14, afn15]))
    afd = automatota.convertToDFA()
    afd.displayTable()

    #Las reglas se ingresan todas en 1 sola linea, separadas por punto y coma
    archivo = open("grammatic.txt", "r")

    print("Leeyendo Gramatica...")
    string = ""
    #Epsilon is a space ' '
    for linea in archivo:
        string = string + linea.rstrip("\n")

    archivo.close()
    
    print("\nAnalizando cadena: " + string)
    lex = Lexer(afd, string)

    print("Lexico OK. Analizando sintacticamente...")
    syn = SyntacticGrammatic(lex)

    print("\nGramatica construida: ")
    grammatic = syn.start()
    if(grammatic):
        ruleNumber = 1
        for r in grammatic:
            print("{} ".format(ruleNumber), end = '')
            r.displayRule()
            ruleNumber += 1
        #Analysis
        analysis = LL1(grammatic)
        if(analysis.isLL1()):
            print("Hi from main")
            #To show table in FRONT
            #table = analysis.getTable()
            #if(analysis.check("aaabbb")):
                #YAAAS
            #else:
                #Error
        else:
            print("Upss")
            #Error
        #LL1(grammatic)    
    '''    
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