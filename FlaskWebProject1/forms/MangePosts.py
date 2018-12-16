from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError

class ManagePosts(Form):
	title = StringField("Name: ",[validators.Length(1,256)])
	
	author = StringField("Author Name: ",[validators.Length(1,100)])

	category = SelectField("Category: ", choices=[])

	submit = SubmitField("Filter")
