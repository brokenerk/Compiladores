#!python3
from State import State
from Transition import Transition
from AFN import AFN

#Main
if __name__ == "__main__":
	e1 = State(1)
	e2 = State(2)
	e3 = State(3)
	e4 = State(4)

	t1 = set([])
	t2 = set([])
	t3 = set([])

	t1.add(Transition('E', e2))
	t2.add(Transition('a', e3))
	t3.add(Transition('E', e4))
	t3.add(Transition('E', e2))

	e1.setTransitions(t1)
	e2.setTransitions(t2)
	e3.setTransitions(t3)

	statesA = set([e1, e2, e3, e4])
	afnA = AFN(statesA, e1, e4)
	afnA.display()

	e3 = State(5)
	e4 = State(6)

	t2 = set([])
	t2.add(Transition('y', e4))
	e3.setTransitions(t2)

	statesB = set([e3, e4])
	afnB = AFN(statesB, e3, e4)
	afnB.display()

	join = afnA.join(afnB)
	join.display()

	afnA.display()
	afnB.display()
