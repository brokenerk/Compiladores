#!python3
from AFN import AFN
from AFD import AFD
from Lexer import Lexer
from CustomSet import CustomSet
epsilon = '\u03B5'

if __name__ == "__main__":
    print("")
    afn1 = AFN.createBasic('a')
    afn1.display()

    print("")
    afn2 = AFN.createBasic('b')
    afn2.display()

    print("")
    afn3 = AFN.createBasic('c')
    afn3.display()

    print("")
    join = afn1.join(afn2)
    #join.display();

    print("")
    posClosure = join.positiveClosure()
    #posClosure.display();

    print("")
    kleen = afn3.kleeneClosure()
    #kleen.display()

    print("")
    concat = posClosure.concat(kleen)
    print("AFN para la ER (a|b)+ c*")
    concat.display()
    concat.setToken(10)

    print("")
    cs = CustomSet(concat.getStates())
    e = concat.getStart()

    statesEpsilon = cs.epsilonClosure(e)
    print("Cerradura {} (a|b)+ c* estado inicial".format(epsilon))
    for e in statesEpsilon:
       print("E: {}".format(e.getId()))

    print("")
    print("AFD de la ER (a|b)+ c*")
    afd1 = concat.convertToAFD(cs)
    afd1.displayTable()

    print("")
    print("Lexer")
    lex = Lexer(afd1, "abc")
    res = lex.yylex()

    if(res != None):
        print(str(res))
    print(str(lex.getToken()))
    

'''
    print("")
    concat = afn1.concat(afn2)
    print("Concat AFN1 and AFN2:")
    concat.display()

    print("")
    posClosureA = afn1.positiveClosure()
    print("Cerradura + AFN 1:")
    posClosureA.display()

    print("")
    kleeneA = afn1.kleeneClosure()
    print("Cerradura Kleene * AFN 1:")
    kleeneA.display()

    print("")
    optional = afn1.optional()
    print("Opcional ? AFN1:")
    optional.display()

    automatota = AFN.addNewStart(set([afn1, afn3, concat, optional]))
    automatota.display()

    print("")
    e = automatota.getStart()
    statesEpsilon = AFN.epsilonClosure(e)
    print("Cerradura {} Automatota estado inicial".format(epsilon))
    for e in statesEpsilon:
       print("E: {}".format(e.getId()))

'''
