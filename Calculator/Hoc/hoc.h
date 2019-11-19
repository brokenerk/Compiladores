typedef struct Symbol {
	char *name;
	short type;
	union {
		double val;
		double (*ptr)();
	}u;
	struct Symbol *next;
}Symbol;

Symbol *install(), *lookup();
