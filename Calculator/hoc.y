%{
#include "hoc.h"
#include<stdio.h>
extern double Pow();
extern int execerror();
%}
%union{
	double val;
	Symbol *sym;
}
%token 	<val> 	NUMBER
%token 	<sym> 	VAR BLTIN UNDEF
%type 	<val>	expr asgn
%right 	'='
%left	'+' '-'
%left 	'*' '/'
%left	UNARYMINUS
%right 	'^'
%%
list :	
	| list '\n'
	| list asgn '\n'
	| list expr '\n'	{printf("\t%.8g\n",$2);}
	| list error '\n'	{yyerrok;}
	;
asgn :	VAR '=' expr { $$=$1->u.val=$3; $1->type = VAR;  }
	;
expr :	NUMBER
	| VAR { if ($1->type == UNDEF) 
		execerror("undefined variable", $1->name );
		$$ = $1->u.val; }
	| asgn
	| BLTIN '(' expr ')' { $$ = (*($1->u.ptr))($3); }
	| expr '+' expr { $$= $1 + $3; }
	| expr '-' expr { $$= $1 - $3; }
	| expr '*' expr { $$= $1 * $3; }
	| expr '/' expr { 
			if ($3 == 0.0)
				execerror("Divisor by zero","");
			$$ = $1 / $3; }
	| expr '^' expr { $$ = Pow($1,$3); }
	| '(' expr ')'	{ $$ = $2; }
	| '-' expr %prec UNARYMINUS { $$ = -$2; }
	;
%%

#include<stdio.h>
#include<ctype.h>
#include<signal.h>
#include<setjmp.h>
jmp_buf begin;
char *progname;
int lineno = 1;
int warning ( char * , char *t);
int execerror( char *, char *);
int yyerror( char *);
int fpecatch();
extern int init();

int main (int argc, char * arcgv[]){
	int fpecatch();

	progname = arcgv[0];
	init();
	setjmp(begin);
	signal(SIGFPE, fpecatch);
	yyparse();
	
	return 0;
}
 
int yyerror(char *s){
	warning(s, (char*) 0);
	return 0;
}

int warning( char *s, char *t){
	fprintf(stderr, "%s: %s", progname, s);
	if (t)
		fprintf(stderr,"%s",t);
	fprintf(stderr," near line %d\n", lineno);
	return 0;
}

int execerror( char *s, char *t){
	warning(s,t);
	longjmp(begin,0);
	return 0;
}

int fpecatch(){
	execerror("floating point exception", (char*) 0);
	return 0;
}
