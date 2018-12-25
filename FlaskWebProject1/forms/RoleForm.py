from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms import validators, ValidationError

class RoleForm(Form):
	rolename = StringField("Role name: ",[validators.Length(1,20), validators.DataRequired("Role name can not be empty")])
	submit = SubmitField("Submit")

