#!python3
from AFN import AFN
from State import State
from Transition import Transition
epsilon = '\u03B5'

if __name__ == "__main__":
    
    afn1 = AFN.createBasic(1,'a')
    afn1.display()
    print('')

    afn2=AFN.createBasic(3,'b')
    afn2.display()
    print('')

    afn3=AFN.createBasic(5,'c')
    afn3.display()
    print('')

    afn4=AFN.createBasic(7,'d')
    afn4.display()
    print('')

    print("")
    join = afn1.join(afn2, 3)
    print("Join AFN 1 and AFN 2:")
    join.display()

    print("")
    e = join.getStart()
    statesEpsilon = join.epsilonClosure(e)
    print("Cerradura {}".format(epsilon))
    for e in statesEpsilon:
        print("E:{}".format( e.getId() ))

    print("")
    concat = afn1.concat(afn3, 4)
    print("Concat AFN 1 and AFN 3:")
    concat.display()

    print("")
    Optional = afn1.optional(4)
    print("Opcional ? AFN A:")
    Optional.display()

    print("")
    posClosureA = afn1.positiveClosure(5)
    print("Cerradura + AFN A:")
    posClosureA.display()

    print("")
    kleeneA = afn1.kleeneClosure(6)
    print("Cerradura Kleene * AFN A:")
    kleeneA.display()