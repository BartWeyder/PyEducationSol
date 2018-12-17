from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError

class AnswerForm(Form):
	title = StringField("Answer Title: ",[validators.Length(1,256)])

	text = TextAreaField("Answer Text: ", [validators.Length(10, 2000), 
									  validators.DataRequired("Text must be at least 10 symbols length")])
	
	submit = SubmitField("Submit")
