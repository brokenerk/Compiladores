#!python3
from AFN import AFN
from State import State
from Transition import Transition

if __name__ == "__main__":
    e1=State(1)
    e2=State(2)
    e3=State(3)

    t1 = Transition ('a',e2)
    t2 = Transition ('b',e3)
    t3 = Transition ('c',e1)

    e1.addTransition(t1)
    e2.addTransition(t2)
    e3.addTransition(t3)

    c1=State(4)
    c2=State(5)
    c3=State(6)

    tr1 = Transition ('x',c2)
    tr2 = Transition ('y',c3)
    tr3 = Transition ('z',c1)

    c1.addTransition(tr1)
    c2.addTransition(tr2)
    c3.addTransition(tr3)

    statesA = set([e1,e2,e3])
    statesB = set([c1,c2,c3])

    afnA = AFN(statesA,e1,e3)
    print("AFN A:")
    afnA.displayAfn()
    afnB = AFN(statesB,c1,c3)
    print("AFN B:")
    afnB.displayAfn()
