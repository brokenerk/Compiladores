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

@app.route("/")
def index():
	return render_template('home.html')

@app.route("/aboutUs")
def aboutUs():
	return render_template('aboutus.html')

@app.route("/convert", methods = ['GET', 'POST'])
def convert():
	add_form = forms.AddForm(request.form)
	global afnAvailable
	if request.method == 'POST' and add_form.validate():
		print("Yes ")
		print(add_form.char.data)
		c = add_form.char.data
		afn = AFN.createBasic(c)
		afn.display()

	
	return render_template('convert.html', form = add_form)

if __name__ == '__main__':
	app.run(debug = True, port = 5000)