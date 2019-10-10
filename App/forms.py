from wtforms import Form 
from wtforms import StringField, TextField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class AddForm(Form):
	char = StringField('Symbol: ', 
		[
			validators.length(min=1, max=1)
		]
		)
class AddToken(Form):
	token = StringField('Token: ', 
		[
			validators.length(min=1, max=3)
		])

class CreateSpecialJoin(Form):
	number = StringField('Number: ', 
		[
			validators.length(min=1, max=3)
		])