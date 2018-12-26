from flask_wtf import Form
from wtforms import DateField, SubmitField
from wtforms import validators, ValidationError

class VisualizationDatesForm(Form):
	date_from = DateField("Date From: ", [])
	
	date_till = DateField("Date Till: ", [])
	
	submit = SubmitField("Show")

