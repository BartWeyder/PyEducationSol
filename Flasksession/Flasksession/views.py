"""
Routes and views for the flask application.
"""

import datetime
from flask import render_template, request, make_response
from Flasksession import app
from wtf.form.login import LoginForm

@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/', methods=["GET", "POST"])
def login():
	form = LoginForm()

	if request.method == "GET":
		email = request.cookies.get("cookiename")
		if email == None:
			return render_template('Login.html', myform=form)
		else:
			return "already logged"

	if request.method == "POST":
		#form = request.form 
		if form.validate() == False:
			return render_template('Login.html', myform=form)
		else:
			#1 create response
			response = make_response("Logged in")
			expire_date = datetime.datetime.now()
			expire_date += datetime.timedelta(seconds=90)
			response.set_cookie("cookiename", request.form["email"], expires=expire_date)
			return response
