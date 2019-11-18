#!python3
import ply.lex as lex
# Tokens
tokens = [
    'VAR',
    'BLTIN',
    'UNDEF',
    'CONST',
    'INTEGER',
    'FLOAT',
    'EXPR',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POT',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    ]

# Regular expressions
t_PLUS    = r'\+'
t_MINUS   = r'\-'
t_TIMES   = r'\*'
t_DIVIDE  = r'\/'
t_EQUALS  = r'\='
t_POT     = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_VAR     = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_BLTIN   = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_CONST   = r'[a-zA-Z_][a-zA-Z0-9_]*'
# Ignored characters
t_ignore = ' \t'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()
