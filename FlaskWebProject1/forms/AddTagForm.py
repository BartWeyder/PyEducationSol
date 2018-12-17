from flask_wtf import Form
from wtforms import SelectField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError

class AddTagForm(Form):
	tag = SelectField("Select Tag: ", [validators.DataRequired("Tag can not be empty")])
	
	submit = SubmitField("Add")
