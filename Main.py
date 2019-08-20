#!python3
from AFN import AFN
from State import State
from Transition import Transition

if __name__ == "__main__":
    e1 = State(1)
    e2 = State(2)
    e3 = State(3)

    t1 = Transition ('a', e2)
    t2 = Transition ('b', e3)

    e1.addTransition(t1)
    e2.addTransition(t2)

    e4 = State(4)
    e5 = State(5)
    e6 = State(6)
    e7 = State(7)

    t4 = Transition ('x', e5)
    t5 = Transition ('y', e6)
    t6 = Transition ('z', e7)

    e4.addTransition(t4)
    e5.addTransition(t5)
    e6.addTransition(t6)

    statesA = set([e1, e2, e3])
    statesB = set([e4, e5, e6, e7])

    afnA = AFN(statesA, e1, e3)
    print("AFN A:")
    afnA.display()

    print("")
    afnB = AFN(statesB, e4, e7)
    print("AFN B:")
    afnB.display()

    print("")
    join = afnA.join(afnB)
    print("Join AFN A and AFN B:")
    join.display()

    print("")
    concat = afnA.concat(afnB)
    print("Concat AFN A and AFN B:")
    concat.display()