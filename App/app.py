from flask import Flask, render_template, request, url_for, redirect,flash
from NFA import NFA
from DFA import DFA
from Token import Token
from Lexer import Lexer
from LL1 import LL1
from SyntacticNFA import SyntacticNFA
from SyntacticGrammar import SyntacticGrammar
import WTForms as forms
import os
epsilon = '\u03B5'

#UPLOAD_FOLDER = os.path.abspath(' /uploads/')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app_root = os.path.dirname(os.path.abspath(__file__))
# Manage every AFN that has been created
nfaDictionary = {}
dfaDictionary = {}

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
    return render_template('aboutUs.html')

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

    return render_template('nfas/add.html', add=addForm, nfa=nfa)

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

    return render_template('nfas/join.html', nfaDictionary=nfaDictionary, nfa=nfaJoin)

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

    return render_template('nfas/specialJoin.html', nfaDictionary=nfaDictionary, nfa=automatota)

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

    return render_template('nfas/concat.html', nfaDictionary=nfaDictionary, nfa=nfaConcat)

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

    return render_template('nfas/positiveClosure.html', nfaDictionary=nfaDictionary, nfa=nfaPosClosure)

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

    return render_template('nfas/kleeneClosure.html', nfaDictionary=nfaDictionary, nfa=nfaKleeneClosure)

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

    return render_template('nfas/optional.html', nfaDictionary=nfaDictionary, nfa=nfaOptional)

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

    return render_template('nfas/setToken.html', nfaDictionary=nfaDictionary, addT=addToken, nfa=nfaTok)

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

    return render_template('nfas/convertToDFA.html', nfaDictionary=nfaDictionary, dfa=dfa)

# ---------------------------------------------------------------------
#                       ANALYSIS: LL(1)
# ---------------------------------------------------------------------
@app.route("/LL(1)", methods = ['GET', 'POST'])
def ll1():
    llForm = forms.LL1(request.form)
    afd = makeAfd()
    tableRelations = None
    tableAnalysis = None
    grammar=None
    rules=''
    if request.method == 'POST':
        string = llForm.string.data
        grammarForm = llForm.grammar.data

        stringAux = grammarForm.split('\r\n')
        for s in stringAux:
            rules += s

        print("\nAnalizando cadena: " + string)
        lex = Lexer(afd, rules)
        print("Lexico OK. Analizando sintacticamente...")
        syn = SyntacticGrammar(lex)
        flash("Lexico OK. Analizando sintacticamente...")
        flash('Gramatica Valida')
        print("\nGramatica construida: ")
        grammar = syn.start()
        if(grammar):
            ruleNumber = 1
        for r in grammar:
            print("{} ".format(ruleNumber), end = '')
            r.displayRule()
            ruleNumber += 1

        #Analysis
        print("\nAnalisis LL(1)")
        ll1 = LL1(grammar)
        if(ll1.isLL1()):
            print("Gramatica compatible con LL(1)")

            ll1.displayTable(0)
            res = ll1.analyze(string)
            ll1.displayTable(1)

            tableRelations = ll1.getTable()
            tableAnalysis = ll1.getAnalysisTable()
            print('''
            Relaciones 
            {}
            '''.format(tableRelations))

            print('''
            Analisis 
            {}
            '''.format(tableAnalysis))

            if(res):
                print("\n" + string + " pertenece a la gramatica")
            else:
                print("\n" + string + " no pertenece a la gramatica")
        else:
            print("\nERROR. La gramatica no es compatible con LL(1)")

    return render_template('analysis/ll1.html',ll1=llForm, grammar = grammar,tableRelations=tableRelations,tableAnalysis=tableAnalysis)

def makeAfd():
    afn1 = NFA.createBasic('a', 'z')
    afn2 = NFA.createBasic('A', 'Z')
    afn3 = NFA.createBasic('0', '9')
    afn4 = NFA.createBasic('+')
    afn5 = NFA.createBasic('-')
    afn6 = NFA.createBasic('*')
    afn7 = NFA.createBasic('/')
    afn8 = NFA.createBasic('(')
    afn9 = NFA.createBasic(')')
    afnA = afn1.join(afn2).join(afn3).join(afn4).join(afn5).join(afn6).join(afn7).join(afn8).join(afn9)
    afn11 = NFA.createBasic('A', 'Z')
    afn12 = NFA.createBasic('a', 'z')
    afn13 = NFA.createBasic ("'")
    afn14 = NFA.createBasic('_')
    afnB = afn11.join(afn12).join(afn13).join(afn14)
    afnC = afnB.kleeneClosure()
    afnD = afnA.concat(afnC)
    afnD.setToken(Token.SYMBOL)
    afn15 = NFA.createBasic('-')
    afn16 = NFA.createBasic('>')
    afnE = afn15.concat(afn16)
    afnE.setToken(Token.ARROW)
    afn17 = NFA.createBasic(';')
    afn17.setToken(Token.SEMICOLON)
    afn18 = NFA.createBasic('|')
    afn18.setToken(Token.OR)
    afn19 = NFA.createBasic(' ')
    afn19.setToken(Token.SPACE)
    automatota = NFA.specialJoin(set([afnD, afnE, afn17, afn18, afn19]))
    afd = automatota.convertToDFA()
    return afd

# ---------------------------------------------------------------------
#                        NFA Syntactic
# ---------------------------------------------------------------------
@app.route("/nfaSyn", methods = ['GET', 'POST'])
def nfaSyntactic():
    nfaForm = forms.NFASyn(request.form)
    afns = set([])
    afdER = None
    if request.method == 'POST':
        regularExpressions = nfaForm.regularExpressions.data
        afd = dfaSyntactic()
        regularExpressions = regularExpressions.split('\r\n')
        print(regularExpressions)
        for re in regularExpressions:
            auxRE = re.split(' ')
            lex = Lexer(afd, auxRE[0])
            syn = SyntacticNFA(lex)
            afnAux = syn.start()
            if(afnAux == False):
                print('Error')                
            afnAux.setToken(int(auxRE[1]))
            afns.add(afnAux)
        afnER = NFA.specialJoin(afns)
        afdER = afnER.convertToDFA()
        dfaDictionary[afdER.getId()] = afdER
    
    return render_template('analysis/nfa.html', nfaF = nfaForm, afdER = afdER )

def dfaSyntactic():
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
    afd = automatota.convertToDFA()
    return afd

# ---------------------------------------------------------------------
#                        LEXICAL ANALYSIS
# ---------------------------------------------------------------------
@app.route("/lexic", methods = ['GET', 'POST'])
def lexic():
    lexicForm = forms.Lexic(request.form)
    lexem = None
    auxdfa = request.form.get('dfa')
    
    if request.method == 'POST':
        string = lexicForm.string.data
        dfa = dfaDictionary[int(auxdfa)]
        lexem = Lexer(dfa, string)
        
    return render_template('lexic.html',lex = lexicForm, dfaDictionary=dfaDictionary,lexic=lexem )

if __name__ == '__main__':
    app.run(debug = True, port = 5000)