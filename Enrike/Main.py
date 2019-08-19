#!python3
from State import State
from Transition import Transition
from AFN import AFN

#Main
if __name__ == "__main__":
	e1 = State(1)
	e2 = State(2)

	t1 = set([])
	t1.add(Transition('a', e2))
	e1.setTransitions(t1)

	statesA = set([e1, e2])
	afnA = AFN(statesA, e1, e2)
	print("Automata A: ")
	afnA.display()

	e3 = State(3)
	e4 = State(4)

	t2 = set([])
	t2.add(Transition('y', e4))
	e3.setTransitions(t2)

	statesB = set([e3, e4])
	afnB = AFN(statesB, e3, e4)
	print("Automata B: ")
	afnB.display()

	join = afnA.join(afnB)
	print("Union A | B: ")
	join.display()

	#Check if original automates didnt get modified
	print("Automata A: ")
	afnA.display()
	print("Automata B: ")
	afnB.display()
