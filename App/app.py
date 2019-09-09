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
@app.route('/convert')

@app.route("/convert", methods = ['GET', 'POST'])
def convert():
	addForm = forms.AddForm(request.form)
	addToken = forms.AddToken(request.form)
	createSpecialJoin = forms.CreateSpecialJoin(request.form)
	afn1 = request.form.get('afn1')
	afn2 = request.form.get('afn2')
	opt = request.form.get('option')
	selectSJ = request.form.getlist('sjArray[]')
	afdNew = 0 #Aux to save the new AFD
	table = [[]] #Save the table
	n = 0
	nSelect = 0
	show = 0
	print("-------------------------------------------------- OPTION:", opt)

	# Option: ADD 
	if request.method == 'POST' and opt == "0":
		c = addForm.char.data
		afn = AFN.createBasic(c)
		afnAvailable[afn.getId()] = afn
		idAfnAvailable[afn.getId()] = afn.getId()
		print("SIZE:", len(afnAvailable))

	# Option: JOIN	
	elif request.method == 'POST' and opt == "1":
		newAfn = afnAvailable[int(afn1)].join(afnAvailable[int(afn2)])
		afnAvailable[newAfn.getId()] = newAfn
		idAfnAvailable[newAfn.getId()] = newAfn.getId()
		# Remove AFN1 and AFN2
		idAfnAvailable[int(afn1)] = -1
		idAfnAvailable[int(afn2)] = -1
		print("--------------------------")
		print("SIZE:", len(afnAvailable))

	# Option: CONCAT 
	elif request.method == 'POST' and opt == "2":
		newAfn = afnAvailable[int(afn1)].concat(afnAvailable[int(afn2)])
		afnAvailable[newAfn.getId()] = newAfn
		idAfnAvailable[newAfn.getId()] = newAfn.getId()
		# Remove AFN1 and AFN2
		idAfnAvailable[int(afn1)] = -1
		idAfnAvailable[int(afn2)] = -1
		print("SIZE:", len(afnAvailable))

	# Option: +CLOSURE
	elif request.method == 'POST' and opt == "3":
		newAfn = afnAvailable[int(afn1)].positiveClosure()
		afnAvailable[newAfn.getId()] = newAfn
		idAfnAvailable[newAfn.getId()] = newAfn.getId()
		# Remove AFN1 
		idAfnAvailable[int(afn1)] = -1
		print("SIZE:", len(afnAvailable))

	# Option: *CLOSURE
	elif request.method == 'POST' and opt == "4":
		newAfn = afnAvailable[int(afn1)].kleeneClosure()
		afnAvailable[newAfn.getId()] = newAfn
		idAfnAvailable[newAfn.getId()] = newAfn.getId()
		# Remove AFN1 
		idAfnAvailable[int(afn1)] = -1
		print("SIZE:", len(afnAvailable))

	# Option: ?Optional
	elif request.method == 'POST' and opt == "5":
		newAfn = afnAvailable[int(afn1)].optional()
		afnAvailable[newAfn.getId()] = newAfn
		idAfnAvailable[newAfn.getId()] = newAfn.getId()
		# Remove AFN1
		idAfnAvailable[int(afn1)] = -1
		print("SIZE:", len(afnAvailable))

	# Option: SET TOKEN
	elif request.method == 'POST' and opt == "6":		
		number = addToken.token.data
		print("Add toke to:", afn1)
		print("Token:", number)
		afnAvailable[int(afn1)].setToken(number)

	# Option: TO AFD
	elif request.method == 'POST' and opt == "7":
		aux = CustomSet(afnAvailable[int(afn1)].getStates())
		afdNew = afnAvailable[int(afn1)].convertToAFD(aux)
		table = afdNew.getTable()
		afdNew.displayTable()
		show = int(1)

	# Option: SPECIAL JOIN -- Create select
	elif request.method == 'POST' and opt == "8":
		n = int(createSpecialJoin.number.data)
		print(n)
		show = int(2)

	# Option: SPECIAL JOIN -- CREATE SPECIAL JOIN
	elif request.method == 'POST' and opt == "9":
		print(len(selectSJ))
		use = [None] * len(selectSJ)
		for i in range(0, len(selectSJ)):
			use[i] = afnAvailable[int(selectSJ[i])]

		automatota = AFN.specialJoin(set(use))
		automatota.display()
	return render_template('convert.html', add=addForm, addT=addToken, addSJ=createSpecialJoin, idAfn=idAfnAvailable, afd=afdNew, afdTable=table, nSelect=n, showElement=show)


if __name__ == '__main__':
	app.run(debug = True, port = 5000)