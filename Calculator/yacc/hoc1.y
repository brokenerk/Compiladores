/*	Compile: 
		yacc hoc1.y
		gcc y.tab.c -w -o hoc1
*/
%{
#define YYSTYPE double /* data type of yacc stack */
%}

%token	NUMBER
%left  	'+' '-' /* left associative, same precedende */
%left 	'*' '/' /* lef assoc., higher precedence*/

%%
list: 
		| list '\n'
		| list expr '\n' { printf("\t%.8g", $2); }
		;
expr: 	NUMBER 			{ $$ = $1; }
		| expr '+' expr { $$ = $1 + $3; }
		| expr '-' expr { $$ = $1 - $3; }
		| expr '*' expr { $$ = $1 * $3; }
		| expr '/' expr { $$ = $1 / $3; }
		| '(' expr ')'  { $$ = $2; }
		;
%%
/* end of grammar */

#include <stdio.h>
#include <ctype.h>

char *progname; /* for error messages */
int lineno = 1;

void main(int argc, char* argv[]) {
	progname = argv[0];
	yyparse();
}

yylex() {
	int c;

	while((c = getchar()) == ' ' || c == '\t');
	if(c == EOF)
		return 0;
	if(c == '.' || isdigit(c)) { /* number */
		ungetc(c, stdin);
		scanf("%lf", &yylval);
		return NUMBER;
	}
	if(c == '\n')
		lineno++;
	return c;
}	

/* called for yacc syntax error */
yyerror(char *s) {	
	warning (s, (char *)0);
}

/* print warning message */
warning(char *s, char *t) {	
	fprintf(stderr, "%s: %s", progname, s);
	if(t)
		fprintf(stderr, "%s", t);
	fprintf(stderr, "near line %d\n", lineno);
}