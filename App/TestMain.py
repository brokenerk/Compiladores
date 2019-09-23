#!python3
from NFA import NFA
from DFA import DFA
from Token import Token
from Lexer import Lexer
from SyntacticNFA import SyntacticNFA
from Lexer import Lexer
import traceback
epsilon = '\u03B5'

if __name__ == "__main__":
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
            lex.analize()

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
        lex2.analize()
        lex2.display()