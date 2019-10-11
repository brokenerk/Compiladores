from wtforms import Form, StringField, TextField, SelectField, TextAreaField, validators

class AddNFA(Form):
	symbol = StringField('Symbol: ', [validators.required(),validators.length(min=1, max=3)])

class SetToken(Form):
	token = StringField('Token: ', [validators.required(),validators.length(min=1, max=4)])

class LL1(Form):
	grammar = TextAreaField('Grammar: ', [validators.required(),validators.length(min=1)])
	string = StringField('String: ', [validators.required(),validators.length(min=1)])