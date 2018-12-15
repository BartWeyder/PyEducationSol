from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
#from flask import Flask, render_template, request, flash
from wtforms import validators, ValidationError

class ManageUsers(Form):
	name = StringField("Name: ",[validators.Length(1,100)])

	role = SelectField("Role: ", choices=[('user', 'Common User'), ('moderator', "Moderator")])

	submit = SubmitField("Filter")
