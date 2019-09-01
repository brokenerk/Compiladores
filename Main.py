#!python3
from AFN import AFN
from State import State
from Transition import Transition
from AFD import AFD
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

    print("")
    csConcat = CustomSet(concat.getStates())
    e = concat.getStart()

    statesEpsilon = csConcat.epsilonClosure(e)
    print("Cerradura {} (a|b)+ c* estado inicial".format(epsilon))
    for e in statesEpsilon:
       print("E: {}".format(e.getId()))

    print("")
    print("Convertir (a|b)+ c* a AFD")
    s = concat.convertToAFD(csConcat)

    cont = 0
    for i in range(0, len(s)):
        print("")
        for e in s[i]:
            print("S" + str(i) + ": " + str(e.getId()))

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
