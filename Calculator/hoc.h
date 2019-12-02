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

typedef int (*Inst)(void);

#define STOP (Inst){0}

extern Inst prog[], *progp,*code();
Datum pop(void);
void constpush(void), varpush(void), 
      bltin(void), eval(void), add(void), sub(void), 
	  mul(void), divd(void), mod(void), negate(void), 
	  power(void), assign(void), print(void);

void prexpr(void);
void gt(void),	lt(void), eq(void),ge(void), le(void),
 	  ne(void), and(void),or(void), not(void);
void ifcode(void),whilecode(void);

void initcode(void);
void execute(Inst *);

int yylex(void);
int warning ( char * , char *t);
int yyerror( char *);
int fpecatch();
void execerror(char *, char *);
int follow(int,int,int);
