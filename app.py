from flask import Flask, render_template, request, url_for, redirect
from NFA import NFA
from DFA import DFA
from Token import Token
from Lexer import Lexer
from LL1 import LL1
from LR0 import LR0
from LR1 import LR1
from LALR import LALR
from SyntacticNFA import SyntacticNFA
from SyntacticGrammar import SyntacticGrammar
import WTForms as forms
import os
epsilon = '\u03B5'

app = Flask(__name__)
# Manage every NFA that has been created
nfaDictionary = {}
dfaDictionary = {}

# ---------------------------------------------------------------------
#                        DFA FOR NFA LEXER
# ---------------------------------------------------------------------
afn1 = NFA.createBasic('a', 'z')
afn1.setToken(Token.SYMBOL_LOWER)
afn2 = NFA.createBasic('A', 'Z')
afn2.setToken(Token.SYMBOL_UPPER)
afn3 = NFA.createBasic('0', '9')
afn3.setToken(Token.NUM)
afn4 = NFA.createBasic('|')
afn4.setToken(Token.JOIN)
afn5 = NFA.createBasic('&')
afn5.setToken(Token.CONCAT)
afn6 = NFA.createBasic('+')
afn6.setToken(Token.POSCLO)
afn7 = NFA.createBasic('-')
afn7.setToken(Token.DASH)
afn8 = NFA.createBasic('.')
afn8.setToken(Token.POINT)
afn9 = NFA.createBasic('?')
afn9.setToken(Token.OPTIONAL)
afn10 = NFA.createBasic('*')
afn10.setToken(Token.KLEEN)
afn11 = NFA.createBasic('(')
afn11.setToken(Token.PAR_L)
afn12 = NFA.createBasic(')')
afn12.setToken(Token.PAR_R)
afn13 = NFA.createBasic ('[')
afn13.setToken(Token.SQUBRACK_L)
afn14 = NFA.createBasic (']')
afn14.setToken(Token.SQUBRACK_R)
afnp = NFA.createBasic('"')
afnq = NFA.createBasic('+')
afn15 = afnp.concat(afnq)
afn15.setToken(Token.PLUS)
afnp3 = NFA.createBasic('"')
afnq3 = NFA.createBasic('-')
afn16 = afnp3.concat(afnq3)
afn16.setToken(Token.MINUS)
automatota = NFA.specialJoin(set([afn1, afn2, afn3, afn4, afn5, afn6, afn7, afn8, afn9, afn10, afn11, afn12, afn13, afn14, afn15, afn16]))
syntacticDFA = automatota.convertToDFA()

# ---------------------------------------------------------------------
#                        DFA FOR GRAMMAR LEXER
# ---------------------------------------------------------------------
afn1 = NFA.createBasic('a', 'z')
afn2 = NFA.createBasic('A', 'Z')
afn3 = NFA.createBasic('0', '9')
afn4 = NFA.createBasic('+')
afn5 = NFA.createBasic('-')
afn6 = NFA.createBasic('*')
afn7 = NFA.createBasic('/')
afn8 = NFA.createBasic('=')
afn9 = NFA.createBasic('(')
afn10 = NFA.createBasic(')')
afn11 = NFA.createBasic(',')
afn12 = NFA.createBasic('.')
afn13 = NFA.createBasic('?')
afn13_1 = NFA.createBasic('^')
afnA = afn1.join(afn2).join(afn3).join(afn4).join(afn5).join(afn6).join(afn7).join(afn8).join(afn9).join(afn10).join(afn11).join(afn12).join(afn13).join(afn13_1)
afn13 = NFA.createBasic('A', 'Z')
afn14 = NFA.createBasic('a', 'z')
afn15 = NFA.createBasic ("'")
afn16 = NFA.createBasic('_')
afnB = afn13.join(afn14).join(afn15).join(afn16)
afnC = afnB.kleeneClosure()
afnD = afnA.concat(afnC)
afnD.setToken(Token.SYMBOL)

afn17 = NFA.createBasic('-')
afn18 = NFA.createBasic('>')
afnE = afn17.concat(afn18)
afnE.setToken(Token.ARROW)

afn19 = NFA.createBasic(';')
afn19.setToken(Token.SEMICOLON)

afn20 = NFA.createBasic('|')
afn20.setToken(Token.OR)

afn21 = NFA.createBasic(' ')
afn21.setToken(Token.SPACE)

automatota2 = NFA.specialJoin(set([afnD, afnE, afn11, afn12, afn19, afn20, afn21]))
grammarDFA = automatota2.convertToDFA()

# ---------------------------------------------------------------------
#                        DFA FOR STRING LEXER
# ---------------------------------------------------------------------
afn1 = NFA.createBasic('A', 'Z')
afn2 = NFA.createBasic('a', 'z')
afn2_1 = NFA.createBasic("'")
afnB = afn1.join(afn2).join(afn2_1).kleeneClosure()
afnB.setToken(Token.SYMBOL)

afn3 = NFA.createBasic('-')
afn4 = NFA.createBasic('>')
afnE = afn3.concat(afn4)
afnE.setToken(Token.ARROW)

afn5 = NFA.createBasic(';')
afn5.setToken(Token.SEMICOLON)

afn6 = NFA.createBasic('|')
afn6.setToken(Token.OR)

afn22 = NFA.createBasic('0', '9')
afn23 = NFA.createBasic('.')
afn24 = NFA.createBasic('0', '9')
afn25 = afn23.concat(afn22.positiveClosure()).optional()
afnF = afn24.positiveClosure().concat(afn25)
afnF.setToken(Token.NUM)

afn26 = NFA.createBasic('&')
afn26.setToken(Token.CONCAT)

afn27 = NFA.createBasic(',')
afn27.setToken(Token.COMMA)

afn28 = NFA.createBasic(' ')
afn28.setToken(Token.SPACE)

afn27_1 = NFA.createBasic('+')
afn27_1.setToken(Token.PLUS)

afn27_2 = NFA.createBasic('-')
afn27_2.setToken(Token.MINUS)

afn27_3 = NFA.createBasic('*')
afn27_3.setToken(Token.PROD)

afn27_4 = NFA.createBasic('/')
afn27_4.setToken(Token.DIV)

afn27_5 = NFA.createBasic('(')
afn27_5.setToken(Token.PAR_L)

afn27_6 = NFA.createBasic(')')
afn27_6.setToken(Token.PAR_R)

automatota3 = NFA.specialJoin(set([afnB, afnE, afn5, afn6, afnF, afn26, afn27, afn28, afn27_1, afn27_2, afn27_3, afn27_4, afn27_5, afn27_6]))
#automatota3 = NFA.specialJoin(set([afnB, afnE, afn5, afn6, afnF, afn26, afn27, afn28]))
stringDFA = automatota3.convertToDFA()

# ---------------------------------------------------------------------
#                               INDEX
# ---------------------------------------------------------------------
@app.route("/")
def index():
    return render_template('index.html')

# ---------------------------------------------------------------------
#                               ABOUT US
# ---------------------------------------------------------------------
@app.route("/aboutUs")
def aboutUs():
    return render_template('aboutus.html')

# ---------------------------------------------------------------------
#                       NFA: ADD
# ---------------------------------------------------------------------
@app.route("/add", methods = ['GET', 'POST'])
def add():
    addForm = forms.AddNFA(request.form)
    nfa = None

    if request.method == 'POST':
        symbol = addForm.symbol.data
        if(len(symbol) > 2):
            nfa = NFA.createBasic(symbol[0], symbol[2])
        else:
            nfa = NFA.createBasic(symbol)
        nfa.display()
        nfaDictionary[nfa.getId()] = nfa
        addForm.symbol.data = ""

    return render_template('nfas/add.html', add = addForm, nfa = nfa)

# ---------------------------------------------------------------------
#                       NFA: JOIN
# ---------------------------------------------------------------------
@app.route("/join", methods = ['GET', 'POST'])
def join():
    nfa1 = request.form.get('nfa1')
    nfa2 = request.form.get('nfa2')
    nfaJoin = None
        
    if request.method == 'POST':
        nfaJoin = nfaDictionary[int(nfa1)].join(nfaDictionary[int(nfa2)])
        nfaJoin.display()
        nfaDictionary[nfaJoin.getId()] = nfaJoin
        # Remove AFN1 and AFN2
        del nfaDictionary[int(nfa1)]
        del nfaDictionary[int(nfa2)]

    return render_template('nfas/join.html', nfaDictionary = nfaDictionary, nfa = nfaJoin)

# ---------------------------------------------------------------------
#                       NFA: SPECIAL JOIN
# ---------------------------------------------------------------------
@app.route("/specialJoin", methods = ['GET', 'POST'])
def specialJoin():
    nfasList = request.form.getlist('nfasList')
    automatota = None
    if request.method == 'POST':
        nfaSet = set([])
        for nfa in nfasList:
            nfaSet.add(nfaDictionary[int(nfa)])
            del nfaDictionary[int(nfa)]

        automatota = NFA.specialJoin(nfaSet)
        automatota.display()
        nfaDictionary[automatota.getId()] = automatota

    return render_template('nfas/specialJoin.html', nfaDictionary = nfaDictionary, nfa = automatota)

# ---------------------------------------------------------------------
#                       NFA: CONCAT
# ---------------------------------------------------------------------
@app.route("/concat", methods = ['GET', 'POST'])
def concat():
    nfa1 = request.form.get('nfa1')
    nfa2 = request.form.get('nfa2')
    nfaConcat = None
        
    if request.method == 'POST':
        nfaConcat = nfaDictionary[int(nfa1)].concat(nfaDictionary[int(nfa2)])
        nfaConcat.display()
        nfaDictionary[nfaConcat.getId()] = nfaConcat
        # Remove AFN1 and AFN2
        del nfaDictionary[int(nfa1)]
        del nfaDictionary[int(nfa2)]

    return render_template('nfas/concat.html', nfaDictionary = nfaDictionary, nfa = nfaConcat)

# ---------------------------------------------------------------------
#                       NFA: +CLOSURE
# ---------------------------------------------------------------------
@app.route("/positiveClosure", methods = ['GET', 'POST'])
def positiveClosure():
    nfa = request.form.get('nfa')
    nfaPosClosure = None

    if request.method == 'POST':
        nfaPosClosure = nfaDictionary[int(nfa)].positiveClosure()
        nfaPosClosure.display()
        nfaDictionary[nfaPosClosure.getId()] = nfaPosClosure
        # Remove AFN
        del nfaDictionary[int(nfa)]

    return render_template('nfas/positiveClosure.html', nfaDictionary = nfaDictionary, nfa = nfaPosClosure)

# ---------------------------------------------------------------------
#                       NFA: *CLOSURE
# ---------------------------------------------------------------------
@app.route("/kleeneClosure", methods = ['GET', 'POST'])
def kleeneClosure():
    nfa = request.form.get('nfa')
    nfaKleeneClosure = None

    if request.method == 'POST':
        nfaKleeneClosure = nfaDictionary[int(nfa)].kleeneClosure()
        nfaKleeneClosure.display()
        nfaDictionary[nfaKleeneClosure.getId()] = nfaKleeneClosure
        # Remove AFN
        del nfaDictionary[int(nfa)]

    return render_template('nfas/kleeneClosure.html', nfaDictionary = nfaDictionary, nfa = nfaKleeneClosure)

# ---------------------------------------------------------------------
#                       NFA: OPTIONAL
# ---------------------------------------------------------------------
@app.route("/optional", methods = ['GET', 'POST'])
def optional():
    nfa = request.form.get('nfa')
    nfaOptional = None

    if request.method == 'POST':
        nfaOptional = nfaDictionary[int(nfa)].optional()
        nfaOptional.display()
        nfaDictionary[nfaOptional.getId()] = nfaOptional
        # Remove AFN
        del nfaDictionary[int(nfa)]

    return render_template('nfas/optional.html', nfaDictionary = nfaDictionary, nfa = nfaOptional)

# ---------------------------------------------------------------------
#                       NFA: SET TOKEN
# ---------------------------------------------------------------------
@app.route("/setToken", methods = ['GET', 'POST'])
def setToken():
    addToken = forms.SetToken(request.form)
    nfa = request.form.get('nfa')
    nfaTok = None

    if request.method == 'POST':        
        tok = addToken.token.data
        nfaDictionary[int(nfa)].setToken(int(tok))
        nfaTok = nfaDictionary[int(nfa)]
        print("NFA Id: " + str(nfa) + " with token: " + str(tok))
        addToken.token.data = ""

    return render_template('nfas/setToken.html', nfaDictionary = nfaDictionary, addT = addToken, nfa = nfaTok)

# ---------------------------------------------------------------------
#                       NFA: CONVERT TO AFD
# ---------------------------------------------------------------------
@app.route("/convertToDFA", methods = ['GET', 'POST'])
def convertToDFA():
    nfa = request.form.get('nfa')
    dfa = None #Aux to save the new AFD
    
    if request.method == 'POST':
        dfa = nfaDictionary[int(nfa)].convertToDFA()
        dfa.displayTable()
        dfaDictionary[dfa.getId()] = dfa
        del nfaDictionary[int(nfa)]

    return render_template('nfas/convertToDFA.html', nfaDictionary = nfaDictionary, dfa = dfa)

# ---------------------------------------------------------------------
#                       ANALYSIS: LL(1)
# ---------------------------------------------------------------------
@app.route("/LL(1)", methods = ['GET', 'POST'])
def ll1():
    llForm = forms.LL1(request.form)
    relationsTable = None
    analysisTable = None
    grammar = None
    msg = None
    msgS = None
    rules = ""
    if request.method == 'POST':
        string = llForm.string.data
        grammarForm = llForm.grammar.data

        stringAux = grammarForm.split('\r\n')
        for s in stringAux:
            rules += s

        print("\nAnalizando cadena: " + string)
        lex = Lexer(grammarDFA, rules)
        print("Lexico OK. Analizando sintacticamente...")
        
        syn = SyntacticGrammar(lex)
        print("\nGramatica construida: ")
        
        grammar = syn.start()
        if(grammar):
            print("Gramatica valida")
            msg = 5

            for r in grammar:
                r.displayRule()
                if(r.isLeftRecursive()):
                    print("La gramatica es recursiva por la izquierda")
                    msg = 4
                    break
            if(msg != 4):
                #Analysis
                print("\nAnalisis LL(1)")
                lex2 = Lexer(stringDFA, string) #Lexic for numbers in string
                ll1 = LL1(grammar, lex2)
                if(msg != 4):
                    if(ll1.isLL1()):
                        print("Gramatica compatible con LL(1)")
                        msg = 1
                    else:
                        print("\nERROR. La gramatica no es compatible con LL(1)")
                        msg = 2

                    ll1.displayTable(0)
                    relationsTable = ll1.getTable()
            
                    if(string != ""):
                        res = ll1.analyze(string)
                        ll1.displayTable(1)
                        analysisTable = ll1.getAnalysisTable()

                        if(res):
                            print("\n" + string + " pertenece a la gramatica")
                            msgS = 1
                        else:
                            print("\n" + string + " no pertenece a la gramatica")
                            msgS = 2
        else:
            print("Gramatica no valida")
            msg = 3
    NFA.restartId()
    DFA.restartId()
    return render_template('analysis/ll1.html', ll1 = llForm, grammar = grammar, relationsTable = relationsTable, analysisTable = analysisTable, msg = msg, msgS = msgS)

# ---------------------------------------------------------------------
#                       ANALYSIS: LR(0)
# ---------------------------------------------------------------------
@app.route("/LR(0)", methods = ['GET', 'POST'])
def lr0():
    lr0Form = forms.LR0(request.form)
    relationsTable = None
    analysisTable = None
    grammar = None
    msg = None
    msgS = None
    rules = ""
    if request.method == 'POST':
        string = lr0Form.string.data
        grammarForm = lr0Form.grammar.data

        stringAux = grammarForm.split('\r\n')
        for s in stringAux:
            rules += s

        print("\nAnalizando cadena: " + string)
        lex = Lexer(grammarDFA, rules)
        print("Lexico OK. Analizando sintacticamente...")
        
        syn = SyntacticGrammar(lex)
        print("\nGramatica construida: ")
        
        grammar = syn.start()
        if(grammar):
            print("Gramatica valida")
            msg = 5
            for r in grammar:
                r.displayRule()
            
            #Analysis
            print("\nAnalisis LR(0)")
            lex2 = Lexer(stringDFA, string) #Lexic for numbers in string
            #lex2.display()
            lr0 = LR0(grammar, lex2)

            if(lr0.isLR0()):
                print("Gramatica compatible con LR(0)")
                msg = 1
            else:
                print("\nERROR. La gramatica no es compatible con LR(0)")
                msg = 2

            lr0.displayTable(0)
            relationsTable = lr0.getTable()
            
            if(string != ""):
                res = lr0.analyze(string)
                lr0.displayTable(1)
                analysisTable = lr0.getAnalysisTable()

                if(res):
                    print("\n" + string + " pertenece a la gramatica")
                    msgS = 1
                else:
                    print("\n" + string + " no pertenece a la gramatica")
                    msgS = 2
        else:
            print("Gramatica no valida")
            msg = 3
    return render_template('analysis/lr0.html', lr0 = lr0Form, grammar = grammar, relationsTable = relationsTable, analysisTable = analysisTable, msg = msg, msgS = msgS)

# ---------------------------------------------------------------------
#                       ANALYSIS: LR(1)
# ---------------------------------------------------------------------
@app.route("/LR(1)", methods = ['GET', 'POST'])
def lr1():
    lr1Form = forms.LR1(request.form)
    relationsTable = None
    analysisTable = None
    grammar = None
    msg = None
    msgS = None
    lex2 = None
    rules = ""
    if request.method == 'POST':
        string = lr1Form.string.data
        grammarForm = lr1Form.grammar.data

        stringAux = grammarForm.split('\r\n')
        for s in stringAux:
            rules += s

        print("\nAnalizando cadena: " + string)
        lex = Lexer(grammarDFA, rules)
        print("Lexico OK. Analizando sintacticamente...")
        
        syn = SyntacticGrammar(lex)
        print("\nGramatica construida: ")
        
        grammar = syn.start()
        if(grammar):
            print("Gramatica valida")
            msg = 5
            for r in grammar:
                r.displayRule()

            #Analysis
            print("\nAnalisis LR(1)")
            lex2 = Lexer(stringDFA, string) #Lexic for numbers in string
            #lex2.display()
            lr1 = LR1(grammar, lex2)

            if(lr1.isLR1()):
                print("Gramatica compatible con LR(1)")
                msg = 1
            else:
                print("\nERROR. La gramatica no es compatible con LR(1)")
                msg = 2

            lr1.displayTable(0)
            relationsTable = lr1.getTable()
            
            if(string != ""):
                res = lr1.analyze(string)
                lr1.displayTable(1)
                analysisTable = lr1.getAnalysisTable()

                if(res):
                    print("\n" + string + " pertenece a la gramatica")
                    msgS = 1
                else:
                    print("\n" + string + " no pertenece a la gramatica")
                    msgS = 2
        else:
            print("Gramatica no valida")
            msg = 3
    return render_template('analysis/lr1.html', lr1 = lr1Form, grammar = grammar, relationsTable = relationsTable, analysisTable = analysisTable, msg = msg, msgS = msgS)


# ---------------------------------------------------------------------
#                       ANALYSIS: LR(1)
# ---------------------------------------------------------------------
@app.route("/LALR", methods = ['GET', 'POST'])
def lalr():
    lalrForm = forms.LALR(request.form)
    relationsTable = None
    analysisTable = None
    grammar = None
    msg = None
    msgS = None
    rules = ""
    if request.method == 'POST':
        string = lalrForm.string.data
        grammarForm = lalrForm.grammar.data

        stringAux = grammarForm.split('\r\n')
        for s in stringAux:
            rules += s

        print("\nAnalizando cadena: " + string)
        lex = Lexer(grammarDFA, rules)
        print("Lexico OK. Analizando sintacticamente...")
        
        syn = SyntacticGrammar(lex)
        print("\nGramatica construida: ")
        
        grammar = syn.start()
        if(grammar):
            print("Gramatica valida")
            msg = 5
            for r in grammar:
                r.displayRule()
            
            #Analysis
            print("\nAnalisis LALR")
            lex2 = Lexer(stringDFA, string) #Lexic for numbers in string
            #lex2.display()
            lalr = LALR(grammar, lex2)

            if(lalr.isLALR()):
                print("Gramatica compatible con LALR")
                msg = 1
            else:
                print("\nERROR. La gramatica no es compatible con LALR")
                msg = 2

            lalr.displayTable(0)
            relationsTable = lalr.getTable()
            
            if(string != ""):
                res = lalr.analyze(string)
                lalr.displayTable(1)
                analysisTable = lalr.getAnalysisTable()

                if(res):
                    print("\n" + string + " pertenece a la gramatica")
                    msgS = 1
                else:
                    print("\n" + string + " no pertenece a la gramatica")
                    msgS = 2
        else:
            print("Gramatica no valida")
            msg = 3
    return render_template('analysis/lalr.html', lalr = lalrForm, grammar = grammar, relationsTable = relationsTable, analysisTable = analysisTable, msg = msg, msgS = msgS)

# ---------------------------------------------------------------------
#                        NFA Syntactic
# ---------------------------------------------------------------------
@app.route("/nfaSyn", methods = ['GET', 'POST'])
def nfaSyntactic():
    nfaForm = forms.NFASyn(request.form)
    nfas = set([])
    dfaER = None
    msg = None
    if request.method == 'POST':
        regularExpressions = nfaForm.regularExpressions.data
        regularExpressions = regularExpressions.split('\r\n')
        print(regularExpressions)
        try:
            for re in regularExpressions:
                auxRE = re.split(' ')
                lex = Lexer(syntacticDFA, auxRE[0])
                syn = SyntacticNFA(lex)
                nfaAux = syn.start()
                if(nfaAux == None):
                    print('Error')
                    msg = 2
                    break      
                nfaAux.setToken(int(auxRE[1]))
                nfas.add(nfaAux)

            if(msg != 2):
                nfaER = NFA.specialJoin(nfas)
                dfaER = nfaER.convertToDFA()
                dfaDictionary[dfaER.getId()] = dfaER
                msg = 1
        except:
            msg = 2
    NFA.restartId()
    DFA.restartId()
    return render_template('analysis/nfa.html', nfaF = nfaForm, dfaER = dfaER, msg = msg)

# ---------------------------------------------------------------------
#                        LEXICAL ANALYSIS
# ---------------------------------------------------------------------
@app.route("/lexic", methods = ['GET', 'POST'])
def lexic():
    lexicForm = forms.Lexic(request.form)
    lexem = None
    lexemes = None
    auxdfa = request.form.get('dfa')
    
    if request.method == 'POST':
        string = lexicForm.string.data
        dfa = dfaDictionary[int(auxdfa)]
        lexem = Lexer(dfa, string)
        lexemes = lexem.getLexemList()
        
    return render_template('lexic.html',lex = lexicForm, dfaDictionary=dfaDictionary,lexic=lexem,lexemes=lexemes)

if __name__ == '__main__':
    app.run()