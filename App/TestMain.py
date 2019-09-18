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
    afn7.setToken(Token.MINUS)

    afn71 = NFA.createBasic('=')
    afn71.setToken(Token.EQUALS)

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

    afna = NFA.createBasic ('[')
    afnb = NFA.createBasic ('a', 'z')
    afnc = NFA.createBasic ('-')
    afnd = NFA.createBasic ('a', 'z')
    afne = NFA.createBasic (']')
    afn13 = afna.concat(afnb).concat(afnc).concat(afnd).concat(afne)
    afn13.setToken(Token.RANGELOWER)

    afnf = NFA.createBasic ('[')
    afng = NFA.createBasic ('A', 'Z')
    afnh = NFA.createBasic ('-')
    afni = NFA.createBasic ('A', 'Z')
    afnj = NFA.createBasic (']')
    afn14 = afnf.concat(afng).concat(afnh).concat(afni).concat(afnj)
    afn14.setToken(Token.RANGEUPPER)

    afnk = NFA.createBasic ('[')
    afnl = NFA.createBasic ('0', '9')
    afnm = NFA.createBasic ('-')
    afnn = NFA.createBasic ('0', '9')
    afno = NFA.createBasic (']')
    afn15 = afnk.concat(afnl).concat(afnm).concat(afnn).concat(afno)
    afn15.setToken(Token.RANGENUM)

    afnp = NFA.createBasic('"')
    afnq = NFA.createBasic('+')
    afn16 = afnp.concat(afnq)
    afn16.setToken(Token.PLUS)

    afnp2 = NFA.createBasic('"')
    afnq2 = NFA.createBasic('*')
    afn17 = afnp2.concat(afnq2)
    afn17.setToken(Token.PROD)

    automatota = NFA.specialJoin(set([afn1, afn2, afn3, afn4, afn5, afn6, afn7, afn71, afn8, afn9, afn10, afn11, afn12, afn13, afn14, afn15, afn16, afn17]))
    afd = automatota.convertToDFA()

    try:
        archivo = open("er.txt", "r")
        afns = set([])

        print("Leeyendo ER...")
        print("")

        for linea in archivo:
            print(linea)
            stringAux = linea.split(' ')
            lex = Lexer(afd, stringAux[0])
            lex.analize()

            syn = SyntacticNFA(lex)
            afnAux = syn.start()
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
    except:
        print("Ha ocurrido el siguiente error: ")
        print(traceback.format_exc())