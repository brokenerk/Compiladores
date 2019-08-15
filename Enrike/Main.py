#!python3
from State import State
from Transition import Transition
from Automata import Automata

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
	t1.add(Transition('E', e4))

	t2.add(Transition('a', e3))
	t2.add(Transition('b', e2))
	t3.add(Transition('E', e4))

	e1.setTransitions(t1)
	e2.setTransitions(t2)
	e3.setTransitions(t3)

	for t in e1.getTransitions():
		print(str(e1.getId()) + " -- " + t.getCharacter() + " ---> " + str(t.getNext().getId()))

	for t in e2.getTransitions():
		print(str(e2.getId()) + " -- " + t.getCharacter() + " ---> " + str(t.getNext().getId()))

	for t in e3.getTransitions():
		print(str(e3.getId()) + " -- " + t.getCharacter() + " ---> " + str(t.getNext().getId()))

	states = set([e1, e2, e3, e4])
	automata = Automata(states, e1, e4)

	print("Estado inicial: " + str(automata.getStart().getId()))
	print("Estado aceptacion: " + str(automata.getAccepted().getId()))