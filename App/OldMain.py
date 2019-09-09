#!python3
from AFN import AFN
from AFD import AFD
from Lexer import Lexer
from CustomSet import CustomSet
epsilon = '\u03B5'

if __name__ == "__main__":
    afn1 = AFN.createBasic('+')
    afn2 = AFN.createBasic('-')
    afn3 = AFN.createBasic('D')
    afn4 = AFN.createBasic('.')
    afn5 = AFN.createBasic('D')
    afnA = afn1.join(afn2).optional().concat(afn3.positiveClosure()).concat(afn4).concat(afn5.positiveClosure())
    afnA.setToken(10)
    afnA.display()

    print("")
    afn6 = AFN.createBasic('+')
    afn7 = AFN.createBasic('-')
    afn8 = AFN.createBasic('D')
    afnB = afn6.join(afn7).optional().concat(afn8.positiveClosure())
    afnA.setToken(20)

    print("")
    afn9 = AFN.createBasic('l')
    afn10 = AFN.createBasic('L')
    afn11 = AFN.createBasic('l')
    afn12 = AFN.createBasic('L')
    afn13 = AFN.createBasic('D')
    afnC = afn9.join(afn10).concat(afn11.join(afn12).join(afn13).kleeneClosure())
    afnA.setToken(30)

    afn14 = AFN.createBasic('+')
    afn15 = AFN.createBasic('+')
    afnD = afn14.concat(afn15)
    afnD.setToken(40)

    afn16 = AFN.createBasic('+')
    afn16.setToken(50)

    automatota = AFN.specialJoin(set([afnA, afnB, afnC, afnD, afn16]))
    automatota.display()

    cs = CustomSet(automatota.getStates())
    afd = automatota.convertToAFD(cs)
    afd.displayTable()







    
'''
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
    '''