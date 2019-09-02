from flask import Flask
from flask import render_template
from AFN import AFN
from AFD import AFD
from CustomSet import CustomSet
epsilon = '\u03B5'

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('home.html')

@app.route("/aboutUs")
def aboutUs():
	return render_template('aboutus.html')

@app.route("/convert")
def convert():
	return render_template('convert.html')

if __name__ == '__main__':
	app.run(debug = True, port = 5000)