from flask_wtf import Form
from wtforms import StringField, SubmitField, validators

class LoginForm(Form):
	email = StringField("Email: ", [validators.DataRequired("Required"), validators.Email("Error in email")])
	password = StringField("Password: ", [validators.DataRequired("Required")])

	submit = SubmitField("Sign In")