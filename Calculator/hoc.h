typedef struct Symbol {
	char *name;
	short type;
	union {
		double val;
		double (*ptr)(double);
	}u;
	struct Symbol *next;
}Symbol;

Symbol *install( char*, int, double), *lookup(char*);

void init(void);

typedef union Datum {
	double val;
	Symbol *sym;
} Datum;

typedef Datum (*Opr)(void);
typedef union Inst{
	Opr opr;
	double val;
	Symbol *sym;
	double (*ptr)(double);
} Inst;

#define STOP (Opr){0}

extern Inst prog[];
Datum pop(void), constpush(void), varpush(void), 
      bltin(void), eval(void), add(void), sub(void), 
	  mul(void), divd(void), mod(void), negate(void), 
	  power(void), assign(void), print(void);


void initcode(void);
void execute(Inst *);

Inst *code(Inst);

int yylex(void);
int warning ( char * , char *t);
int yyerror( char *);
int fpecatch();
void execerror(char *, char *);
