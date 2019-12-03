#include <stdio.h>
#include <stdlib.h>

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

typedef union Datum {
	double val;
	Symbol *sym;
} Datum;

typedef int (*Inst)(void);
#define STOP (Inst){0}

extern Inst prog[], *progp,*code();
Datum pop(void);
extern void constpush(void), varpush(void), 
      bltin(void), eval(void), add(void), sub(void), 
	  mul(void), divd(void), mod(void), negate(void), 
	  power(void), assign(void), print(void);

extern void prexpr(void);
extern void gt(void),	lt(void), eq(void),ge(void), le(void),
 	  ne(void), and(void),or(void), not(void);
extern void ifcode(void),whilecode(void),forcode(void),
			switchcode(),casecode();

extern void initcode(void);
extern void execute(Inst *);
void init(void);

int yylex(void);
void warning ( char * , char *t);
void yyerror( char *);
int fpecatch();
void execerror(char *, char *);
int follow(int,int,int);
