#!python3
from AFN import AFN
from AFD import AFD
from Lexer import Lexer
from CustomSet import CustomSet
epsilon = '\u03B5'

if __name__ == "__main__":

    

    print("")
    afn1 = AFN.createBasic('S')
    afn2 = AFN.createBasic('D')
    afnA = afn1.optional().concat(afn2.positiveClosure())
    afnA.display()
    afnA.setToken(1500)

    print("")
    afn3 = AFN.createBasic('S')
    afn4 = AFN.createBasic('D')
    afn5 = AFN.createBasic('D')
    afn6 = AFN.createBasic('.')
    afnB = afn3.optional().concat(afn4.positiveClosure()).concat(afn6).concat(afn5.positiveClosure())
    afnB.display()
    afnB.setToken(2000)

    print("")
    afn7 = AFN.createBasic('L')
    afn8 = AFN.createBasic('L')
    afn9 = AFN.createBasic('D')
    afnC = afn7.concat(afn8.join(afn9).kleeneClosure())
    afnC.display()
    afnC.setToken(2500)

    print("")
    afn10 = AFN.createBasic('=')
    afn11 = AFN.createBasic('=')
    afnD = afn10.concat(afn11)
    afnD.display()
    afnD.setToken(3000)

    print("")
    afnE = AFN.createBasic('+')
    afnE.setToken(3500)
    afnE.display()

    print("")
    automatota = AFN.specialJoin(set([afnA, afnB, afnC, afnD, afnE]))
    automatota.display()

    print("")
    print("AFD: ")
    cs = CustomSet(automatota.getStates())
    afd = automatota.convertToAFD(cs)
    afd.displayTable()

    print("")
    print("Lexer: ")
    lex = Lexer(afd, "SDD.D+DD==SDD.D++LDL+LDD")
    res = lex.yylex()
    if(res != -1):
        print(str(res))
    print(str(lex.getToken()))