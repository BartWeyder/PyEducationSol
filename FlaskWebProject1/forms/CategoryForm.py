from flask_wtf import Form
from wtforms import StringField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError

class CategoryForm(Form):
	title = StringField("Category Title: ",[validators.Length(1,40), validators.DataRequired("Title can not be empty")])
	submit = SubmitField("Submit")
