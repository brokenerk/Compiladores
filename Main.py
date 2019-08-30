#!python3
from AFN import AFN
from State import State
from Transition import Transition
from AFD import AFD
epsilon = '\u03B5'

if __name__ == "__main__":
    #print("")
    #afn1 = AFN.createBasic('a')
    #print("AFN 1:")
    #afn1.display()
##
    #print("")
    #afn2 = AFN.createBasic('b')
    #print("AFN 2:")
    #afn2.display()
    #
    #print("")
    #join = afn1.join(afn2)
    #print("Join AFN 1 and AFN 2:")
    #join.display()
##
    #print("")
    #e = join.getStart()
    ##If there's only 1 state, here just send set([e]), and with that we just implement 1 method CE
    #statesEpsilon = join.epsilonClosure(e)
    #print("Cerradura {} AFN1|AFN2 estado inicial".format(epsilon))
    #for e in statesEpsilon:
    #    print("E: {}".format(e.getId()))
    
    #print("IR_A 'a' en AFN1|AFN2")
    #statesGo = AFN.goTo(statesEpsilon,'a')
    #for e in statesGo:
    #    print("E: {}".format(e.getId()))
#
    #print("")
    #concat = afn1.concat(afn2)
    #print("Concat AFN 1 and AFN 2:")
    #concat.display()
#
    #print("")
    #posClosureA = afn1.positiveClosure()
    #print("Cerradura + AFN 1:")
    #posClosureA.display()
#
    #print("")
    #kleeneA = afn1.kleeneClosure()
    #print("Cerradura Kleene * AFN 1:")
    #kleeneA.display()
#
    #print("")
    #optional = afn1.optional()
    #print("Opcional ? AFN 1:")
    #optional.display()

    afn1 = AFN.createBasic("a")
    afn2 = AFN.createBasic("b")
    afn3 = AFN.createBasic("c")
    join = afn1.join(afn2)
    kleenA = join.kleeneClosure()
    con = kleenA.concat(afn3)
    con.display()
    print("")
    afd1 = con.afd()
    afd1.display()
