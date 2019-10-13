from flask import Flask, render_template, request, url_for, redirect
from NFA import NFA
from DFA import DFA
from Token import Token
from Lexer import Lexer
from LL1 import LL1
from SyntacticNFA import SyntacticNFA
from SyntacticGrammar import SyntacticGrammar
import WTForms as forms
epsilon = '\u03B5'

app = Flask(__name__)
# Manage every AFN that has been created
nfaDictionary = {}

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
        del nfaDictionary[int(nfa)]

    return render_template('nfas/convertToDFA.html', nfaDictionary=nfaDictionary, dfa=dfa)

# ---------------------------------------------------------------------
#                       ANALYSIS: LL(1)
# ---------------------------------------------------------------------
@app.route("/LL(1)", methods = ['GET', 'POST'])
def ll1():
    return render_template('analysis/ll1.html')

# ---------------------------------------------------------------------
#                        LEXICAL ANALYSIS
# ---------------------------------------------------------------------
@app.route("/lexic")
def lexic():
    return render_template('lexic.html')

if __name__ == '__main__':
    app.run(debug = True, port = 5000)