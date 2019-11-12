#!python3
import ply.yacc as yacc
from calclex import tokens
# Build the lexer


# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names (for storing variables)
names = { }


def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]
    print(names[p[1]])

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_empty(p):
    'statement :'
    p[0] = None

def p_error(p):
	'statement : error'
	try:
		print("Syntax error at '%s'" % p.value)
	except AttributeError:
		print("Syntax error")

def p_expression_binop(p):
    '''
    expression : expression PLUS expression
           	   | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    '''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/':
    	try:
    		p[0] = p[1] / p[3]
    	except ZeroDivisionError:
	        print("Division by zero")
	        p[0] = 0

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_float(p):
    'expression : FLOAT'
    p[0] = p[1]

def p_expression_integer(p):
    'expression : INTEGER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        continue
    yacc.parse(s)