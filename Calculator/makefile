YFLAGS = -d
OBJS = hoc.o lex.o init.o math.o symbol.o

hoc3: 	$(OBJS)
	cc $(OBJS) -lm -lfl -o hoc3

hoc.o: 	hoc.h

lex.o init.o symbol.o:	hoc.h y.tab.h

pr:
	@pr hoc.y hoc.h init.c math.c symbol.c makefile

clean:
	rm -f $(OBJS) y.tab.[ch]
