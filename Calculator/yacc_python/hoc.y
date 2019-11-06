/*	Compile: 
		yacc hoc.y
		gcc y.tab.c -lpython3.7m -w -o hoc
*/
%{
#define YYSTYPE double
%}

%token	NUMBER
%left  	'+' '-'
%left 	'*' '/'

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

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *progname;
int resultado;
PyObject *objeto, *retorno, *modulo, *clase, *metodo, *argumentos;
int lineno = 1;

void main(int argc, char* argv[]) {
	printf("main\n");
	progname = argv[0];

    char* cadena = (char*)calloc(20,sizeof(char));
    scanf("%s", cadena);

    //lex = Lexer(cadena)
	Py_Initialize();
		PyObject *file = PyUnicode_FromString("Lexer");
	    modulo = PyImport_ImportModule(file);
		clase = PyObject_GetAttrString(modulo, "Lexer");
		argumentos = Py_BuildValue("s", cadena);
		objeto = PyEval_CallObject(clase, argumentos);
	Py_Finalize();
	printf("Lexer creado\n");
	yyparse();
}

//lex.yylex()
yylex() {
	printf("yylex\n");
	Py_Initialize();
		metodo = PyObject_GetAttrString(objeto, "yylex");
		argumentos = Py_BuildValue("");
		retorno = PyEval_CallObject(metodo, argumentos);
		PyArg_Parse(retorno, "i", &resultado);
	Py_Finalize();
	return resultado;
}	

yyerror(char *s) {	
	warning (s, (char *)0);
}

warning (char *s, char *t) {	
	fprintf(stderr, "%s: %s", progname,s);
	if(t)
		fprintf(stderr, "%s", t);
	fprintf(stderr, "near line %d\n", lineno);
}