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

#include<Python.h>
#include<stdio.h>
#include<ctype.h>	

char *progname;
PyObject *objeto,*retorno, *modulo, *clase, *metodo, *argumentos;
int lineno =1;

main(argc,argv) char *argv[];{
	progname=argv[0];
	int * p, c, t=0,pos;
    p = (int*) malloc(sizeof(int));
    while((c=getchar()) != '\n')
    {
        p[t++] = c; 
        p = (int*) realloc(p, (t+1)*sizeof(int));
        if(p == NULL)
        {
            printf("\nNo hay espacio en memoria.");
            return 1;
        }
    }
    c=0;
    pos=0;
    char cadena[t];

    while(c<t) {
        cadena[c]=putchar(p[c++]);
    } 
    
	Py_Initialize();

	PyLexer *FileScript;
	FileScript = PyFile_FromString("Lexer.py","r");
	PyRun_SimpleFile(PyFile_AsFile(FileScript),"r");

    modulo = PyImport_ImportModule("Lexer");
	clase = PyObject_GetAttrString(modulo, "Lexer");
	argumentos = Py_BuildValue("ii",cadena);
	objeto = PyEval_CallObject(clase, argumentos);

	Py_Finalize();
	yyparse();
}

yylex(){
	Py_Initialize();
		metodo = PyObject_GetAttrString(objeto,"yylex");
		argumentos = Py_BuildValue("()");
		retorno = PyEval_CallObject(metodo,argumentos);
		PyArg_Parse(retorno,"i",&resultado);
		return resultado;
	Py_Finalize(); 
}	

yyerror(s)
char *s;
{
	warning (s,(char *)0);
}

warning (s,t) 
char *s, *t;
{
	fprintf(stderr,"%s: %s",progname,s);
	if(t)
		fprintf(stderr,"%s",t);
	fprintf(stderr,"near line %d\n",lineno);
}
