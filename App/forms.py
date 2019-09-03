from wtforms import Form 
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class AddForm(Form):
	char = StringField('Name ',
		[ 
			validators.length(min=1, max=5, message='No valid!'),
			validators.Required(message="We need it.")
		]
		)
	