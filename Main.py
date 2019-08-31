#!python3
from AFN import AFN
from State import State
from Transition import Transition
from AFD import AFD
from copy import deepcopy
epsilon = '\u03B5'

if __name__ == "__main__":
    print("")
    afn1 = AFN.createBasic('a')
    print("AFN 1:")
    afn1.display()

    print("")
    afn2 = AFN.createBasic('b')
    print("AFN 2:")
    afn2.display()

    print("")
    afn3 = AFN.createBasic('c')
    print("AFN 3:")
    afn3.display()

    print("")
    join = afn1.join(afn2)
    join.display();

    print("")
    posClosure = join.positiveClosure()
    posClosure.display();
    print("")
    kleen = afn3.kleeneClosure()
    kleen.display()
    print("")
    concat = posClosure.concat(kleen)
    concat.display()

    print("")
    e = concat.getStart()
    statesEpsilon = AFN.epsilonClosure(e)
    print("Cerradura {} (a|b)+ c* estado inicial".format(epsilon))
    ne = None
    for e in statesEpsilon:
       print("E: {}".format(e.getId()))

    s = concat.convertToAFD()
    for i in range(0,len(s)):
        for e in s[i]:
            print("S" + str(i) + " " +str(e.getId()))

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

    print("")
    goTo = AFN.goTo(statesEpsilon, "d")
    print("Go to de 'b' cerradura {}".format(epsilon))
    for e in goTo:
       print("E: {}".format(e.getId()))
'''
