#!python3
import ply.yacc as yacc
from calclex import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    ('right','POT'),
    )

# dictionary of names (for storing variables)
names = { }

def p_empty(p):
    'list :'
    p[0] = None

def p_list_expr(p):
    'list : expr'
    print(p[1])

def p_list_asgn(p):
    'list : asgn'
    p[0] = p[1]

def p_list_error(p):
	'list : error'
	try:
		print("Syntax error at '%s'" % p.value)
	except AttributeError:
		print("Syntax error")

def p_asgn(p):
    'asgn : VAR EQUALS expr'
    names[p[0]] = p[3]

def p_expr_float(p):
    'expr : FLOAT'
    p[0] = p[1]

def p_expr_integer(p):
    'expr : INTEGER'
    p[0] = p[1]

def p_expr_var(p):
    'expr : VAR'
    p[0] = p[1]

def p_expr_asgn(p):
    'expr : asgn'
    p[0] = p[1]

def p_expr_BLTIN(p):
    'expr : BLTIN LPAREN expr RPAREN'
    print(p[1])

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr(p):
    '''
    expr : expr PLUS expr
           	   | expr MINUS expr
               | expr TIMES expr
               | expr DIVIDE expr
               | expr POT expr
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
    elif p[2] == '^': p[0] = p[1] ** p[3]

def p_expr_uminus(p):
    'expr : MINUS expr %prec UMINUS'
    p[0] = -p[2]

yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        continue
    yacc.parse(s)
