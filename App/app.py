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
	addForm = forms.AddForm(request.form)
	afn1 = request.form.get('afn1')
	afn2 = request.form.get('afn2')
	opt = request.form.get('option')
	print("-------------------------------------------------- OPTION:", opt)

	if request.method == 'POST' and opt == "0":
			c = addForm.char.data
			if c not in alphabet:
				afn = AFN.createBasic(c)
				afnAvailable[afn.getId()] = afn
				alphabet[c] = afn.getId()
				idAfnAvailable[afn.getId()] = afn.getId()
				print("SIZE:", len(afnAvailable))
				
	elif request.method == 'POST' and opt == "1":
		if len(afn1) > 0 and len(afn2) > 0:
			newAfn = afnAvailable[int(afn1)].join(afnAvailable[int(afn2)])
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	elif request.method == 'POST' and opt == "2":
		if len(afn1) > 0 and len(afn2) > 0:
			newAfn = afnAvailable[int(afn1)].concat(afnAvailable[int(afn2)])
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	elif request.method == 'POST' and opt == "3":
		if len(afn1) > 0:
			newAfn = afnAvailable[int(afn1)].positiveClosure()
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	elif request.method == 'POST' and opt == "4":
		if len(afn1) > 0:
			newAfn = afnAvailable[int(afn1)].kleeneClosure()
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	elif request.method == 'POST' and opt == "5":
		if len(afn1) > 0:
			newAfn = afnAvailable[int(afn1)].epsilonClosure()
			afnAvailable[newAfn.getId()] = newAfn
			idAfnAvailable[newAfn.getId()] = newAfn.getId()
			print("SIZE:", len(afnAvailable))

	elif request.method == 'POST' and opt == "6":
		if len(afn1) > 0:
		    print("Other option")

	return render_template('convert.html', add=addForm, idAfn=idAfnAvailable)


if __name__ == '__main__':
	app.run(debug = True, port = 5000)