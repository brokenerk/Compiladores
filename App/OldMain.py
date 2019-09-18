#!python3
from AFN import AFN
from AFD import AFD
from Lexer import Lexer
from CustomSet import CustomSet
from Syntactic import SyntacticAfn
from Lexer import Lexer

epsilon = '\u03B5'

if __name__ == "__main__":

    afn1 = AFN.createBasic('a','z')
    afn1.setToken(100)

    afn2 = AFN.createBasic('A','Z')
    afn2.setToken(110)

    afn3 = AFN.createBasic('0','9')
    afn3.setToken(120)

    afn4 = AFN.createBasic('|')
    afn4.setToken(130)

    afn5 = AFN.createBasic('&')
    afn5.setToken(140)

    afn6 = AFN.createBasic('+')
    afn6.setToken(150)

    afn7 = AFN.createBasic('-')
    afn7.setToken(160)

    afn8 = AFN.createBasic('.')
    afn8.setToken(170)
    afn9 = AFN.createBasic('?')
    afn9.setToken(180)

    afn10 = AFN.createBasic('*')
    afn10.setToken(190)

    afn11 = AFN.createBasic('(')
    afn11.setToken(200)

    afn12 = AFN.createBasic(')')
    afn12.setToken(210)

    afna = AFN.createBasic ('[')
    afnb = AFN.createBasic ('a','z')
    afnc = AFN.createBasic ('-')
    afnd = AFN.createBasic ('a','z')
    afne = AFN.createBasic (']')
    afn13 = afna.concat(afnb).concat(afnc).concat(afnd).concat(afne)
    afn13.setToken(101)

    afnf = AFN.createBasic ('[')
    afng = AFN.createBasic ('A','Z')
    afnh = AFN.createBasic ('-')
    afni = AFN.createBasic ('A','Z')
    afnj = AFN.createBasic (']')
    afn14 = afnf.concat(afng).concat(afnh).concat(afni).concat(afnj)
    afn14.setToken(111)

    afnk = AFN.createBasic ('[')
    afnl = AFN.createBasic ('0','9')
    afnm = AFN.createBasic ('-')
    afnn = AFN.createBasic ('0','9')
    afno = AFN.createBasic (']')
    afn15 = afnk.concat(afnl).concat(afnm).concat(afnn).concat(afno)
    afn15.setToken(121)

    automatota = AFN.specialJoin(set([afn1, afn2, afn3, afn4, afn5,afn6,afn7,afn8,afn9,afn10,afn11,afn12,afn13,afn14,afn15]))
    automatota.display()

    cs = CustomSet(automatota.getStates())
    afd = automatota.convertToAFD(cs)
    print("")
    print("AFD: ")
    afd.displayTable()

    print("")
    string = "[0-9]+&.&[0-9]+" #(a|b)+&d*  [0-9]+&.&[0-9]+  ([a-z]|[A-Z])&([a-z]|[A-Z]|[0-9])*
    print("Lexer: " + string)
    
    lex = Lexer(afd, string)
    lex.analize()

    Sin = SyntacticAfn (lex)
    afn13 = Sin.start()
    afn13.display()

    '''
    afn1 = AFN.createBasic('+')
    afn2 = AFN.createBasic('-')
    afn3 = AFN.createBasic('0','9')
    afn4 = AFN.createBasic('.')
    afn5 = AFN.createBasic('0','9')
    afnA = afn1.join(afn2).optional().concat(afn3.positiveClosure()).concat(afn4).concat(afn5.positiveClosure())
    afnA.setToken(10)

    print("")
    afn6 = AFN.createBasic('+')
    afn7 = AFN.createBasic('-')
    afn8 = AFN.createBasic('0','9')
    afnB = afn6.join(afn7).optional().concat(afn8.positiveClosure())
    afnB.setToken(20)

    print("")
    afn9 = AFN.createBasic('a','z')
    afn10 = AFN.createBasic('A','Z')
    afn11 = AFN.createBasic('a','z')
    afn12 = AFN.createBasic('A','Z')
    afn13 = AFN.createBasic('0','9')
    afnC = afn9.join(afn10).concat(afn11.join(afn12).join(afn13).kleeneClosure())
    afnC.setToken(30)

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
    print("")
    print("AFD: ")
    afd.displayTable()

    print("")
    string = "+54.7+77++-81.4Ab0raN+++Dyv99i"
    print("Lexer: " + string)
    
    lex = Lexer(afd, string)
    lex.analize()
    print("")

    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    
    print("")
    afn1 = AFN.createBasic('S')
    afn2 = AFN.createBasic('D')
    afnA = afn1.optional().concat(afn2.positiveClosure())
    afnA.display()
    afnA.setToken(15)

    print("")
    afn3 = AFN.createBasic('S')
    afn4 = AFN.createBasic('D')
    afn5 = AFN.createBasic('D')
    afn6 = AFN.createBasic('.')
    afnB = afn3.optional().concat(afn4.positiveClosure()).concat(afn6).concat(afn5.positiveClosure())
    afnB.display()
    afnB.setToken(20)

    print("")
    afn7 = AFN.createBasic('L')
    afn8 = AFN.createBasic('L')
    afn9 = AFN.createBasic('D')
    afnC = afn7.concat(afn8.join(afn9).kleeneClosure())
    afnC.display()
    afnC.setToken(25)

    print("")
    afn10 = AFN.createBasic('=')
    afn11 = AFN.createBasic('=')
    afnD = afn10.concat(afn11)
    afnD.display()
    afnD.setToken(30)

    print("")
    afnE = AFN.createBasic('+')
    afnE.setToken(35)
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
    string = "SDD.D+DD==SDD.D++LDL+LDD"
    print("Lexer: " + string)
    
    lex = Lexer(afd, string)
    lex.analize()
    print("")

    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    lex.returnToken()
    lex.returnLexem()
    print("Ctrl Z")
    print("Repite: " + str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    lex.returnToken()
    lex.returnLexem()
    print("Ctrl Z")
    print("Repite: " + str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    print(str(lex.getToken()) + ": " + lex.getLexem())
    '''