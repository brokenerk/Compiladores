%{
#include "hoc.h"
#include<stdio.h>
#define code2(c1,c2) code(c1); code(c2);
#define code3(c1,c2,c3) code(c1); code(c2); code(c3);
%}
%union{
	double val;
	Symbol *sym;
	Inst *inst;
}
%token 	<val> 	NUMBER
%token 	<sym> 	VAR BLTIN UNDEF CONST

%right 	'='
%left	'+' '-'
%left 	'*' '/'
%left	UNARYMINUS
%right 	'^'
%%
list :	
	| list '\n'
	| list asgn '\n'	{ code2( (Inst){.opr =pop} , (Inst){.opr = STOP} ); return 1;}
	| list expr '\n'	{ code2( (Inst){.opr =print}, (Inst){.opr =STOP}); return 1;}
	| list error '\n'	{yyerrok;}
	;
asgn :	VAR '=' expr 	{ code3( (Inst){.opr =varpush}, (Inst){.sym = $1} ,(Inst){.opr =assign} ); }
	;
expr :	NUMBER			{ code2( (Inst){.opr=constpush},(Inst){.val=$1} ); }
	| VAR 				{ code3( (Inst){.opr=varpush}, (Inst){.sym=$1} , (Inst){.opr=eval} ); }
	| CONST				{ code3( (Inst){.opr=varpush}, (Inst){.sym=$1} , (Inst){.opr=eval} ); }
	| asgn				
	| BLTIN '(' expr ')' { code2( (Inst){.opr=bltin} , (Inst){.ptr=$1->u.ptr} ); }
	| expr '+' expr 	 { code( (Inst){.opr=add} ); }
	| expr '-' expr 	 { code( (Inst){.opr=sub} ); }
	| expr '*' expr 	 { code( (Inst){.opr=mul} ); }
	| expr '/' expr 	 { code( (Inst){.opr=divd} ); }
	| expr '^' expr 	 { code( (Inst){.opr=power} ); }
	| '(' expr ')'		 
	| '-' expr %prec UNARYMINUS { code( (Inst){.opr=negate} ); }
	;
%%

#include<stdio.h>
#include<ctype.h>
#include<signal.h>
#include<setjmp.h>
jmp_buf begin;

char *progname;
int lineno = 1;

int main (int argc, char * arcgv[]){
	int fpecatch();

	progname = arcgv[0];
	init();
	setjmp(begin);
	signal(SIGFPE, fpecatch);

	for (initcode(); yyparse(); initcode())
		execute(prog);
	
	return 0;
}
 
yylex(void)
{
	int c;

	while ((c=getchar()) == ' ' || c == '\t')
		;
	if (c == EOF)
		return 0;
	if (c == '.' || isdigit(c)) {
		ungetc(c, stdin);
		scanf("%lf", &yylval.val);
		return NUMBER;
	}
	if (isalpha(c)) {
		Symbol *s;
		char sbuf[100], *p = sbuf;
		do{
			*p++ = c;
		}while((c=getchar()) != EOF && isalnum(c) );
		ungetc(c,stdin);
		*p='\0';
		if ( (s=lookup(sbuf)) == 0 )
			s= install(sbuf,UNDEF,0.0);
		yylval.sym =s;
		return s->type == UNDEF ? VAR : s->type;
	}
	if (c == '\n')
		lineno++;
	
	return c;
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

void execerror( char *s, char *t){
	warning(s,t);
	longjmp(begin,0);
}

int fpecatch(){
	execerror("floating point exception", (char*) 0);
	return 0;
}
