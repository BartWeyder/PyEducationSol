from flask_wtf import Form
from wtforms import StringField, SelectField, DecimalField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError

class UserForm(Form):
	name = StringField("Name: ",[validators.Length(1,100), validators.DataRequired("Name can not be empty")])
	
	role = SelectField("Role: ", choices=[('user', 'Common User'), ('moderator', "Moderator")])

	status = DecimalField("Status: ", [validators.NumberRange(0,1), validators.DataRequired("Status can not be empty")])

	submit = SubmitField("Submit")
