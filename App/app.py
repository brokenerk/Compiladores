from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

from AFN import AFN
from AFD import AFD
from CustomSet import CustomSet
epsilon = '\u03B5'

import forms

app = Flask(__name__)

# Manage every AFN that has been created
afnAvailable = {}
alphabet = {}
idAfnAvailable = {}
cont = 0

@app.route("/")
def index():
	return render_template('home.html')

@app.route("/aboutUs")
def aboutUs():
	return render_template('aboutus.html')

@app.route("/convert", methods = ['GET', 'POST'])
def convert():
	flag = 0
	addForm = forms.AddForm(request.form)
	addToken = forms.AddToken(request.form)
	afn1 = request.form.get('afn1')
	afn2 = request.form.get('afn2')
	opt = request.form.get('option')
	afdNew = 0
	print("-------------------------------------------------- OPTION:", opt)

	# Option: ADD 
	if request.method == 'POST' and opt == "0":
			c = addForm.char.data
			if c not in alphabet:
				afn = AFN.createBasic(c)
				afnAvailable[afn.getId()] = afn
				alphabet[c] = afn.getId()
				idAfnAvailable[afn.getId()] = afn.getId()
				print("SIZE:", len(afnAvailable))
	
	# Option: JOIN	
	elif request.method == 'POST' and opt == "1":
		if len(afn1) > 0 and len(afn2) > 0:
			newAfn = afnAvailable[int(afn1)].join(afnAvailable[int(afn2)])
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	# Option: CONCAT 
	elif request.method == 'POST' and opt == "2":
		if len(afn1) > 0 and len(afn2) > 0:
			newAfn = afnAvailable[int(afn1)].concat(afnAvailable[int(afn2)])
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	# Option: +CLOSURE
	elif request.method == 'POST' and opt == "3":
		if len(afn1) > 0:
			newAfn = afnAvailable[int(afn1)].positiveClosure()
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	# Option: *CLOSURE
	elif request.method == 'POST' and opt == "4":
		if len(afn1) > 0:
			newAfn = afnAvailable[int(afn1)].kleeneClosure()
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	# Option: ?Optional
	elif request.method == 'POST' and opt == "5":
		if len(afn1) > 0:
			aux = CustomSet(afnAvailable[int(afn1)].getStates())
			e = afnAvailable[int(afn1)].getStart()
			statesEpsilon = aux.epsilonClosure(e)
			#for e in statesEpsilon:
			#	print("E: {}".format(e.getId()))
			print("SIZE:", len(afnAvailable))

	# Option: SET TOKEN
	elif request.method == 'POST' and opt == "6":
		if len(afn1) > 0:
			number = addToken.token.data
			#print("Add toke to:", afn1)
			#print("Token:", number)
			afnAvailable[int(afn1)].setToken(number)

	# Option: TO AFD
	elif request.method == 'POST' and opt == "7":
		if len(afn1) > 0:
			aux = CustomSet(afnAvailable[int(afn1)].getStates())
			e = afnAvailable[int(afn1)].getStart()
			afdNew = afnAvailable[int(afn1)].convertToAFD(aux)
			afdNew.displayTable()

	return render_template('convert.html', add=addForm, addT=addToken, idAfn=idAfnAvailable, showBool=flag, afd=afdNew)


if __name__ == '__main__':
	app.run(debug = True, port = 5000)