from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, DecimalField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError
from dao.post_handle import get_all

class PostForm(Form):
	title = StringField("Post Title: ",[validators.Length(1,256), validators.DataRequired("Title can not be empty")])

	text = TextAreaField("Post Text: ", [validators.Length(10, 1000), 
									  validators.DataRequired("Text must be at least 10 symbols length")])
	
	category = SelectField("Category: ", choices=get_all())

	submit = SubmitField("Submit")
