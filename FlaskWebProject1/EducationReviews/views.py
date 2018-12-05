"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from flask import render_template, request, redirect, make_response, session, g
from EducationReviews import app
import cx_Oracle
from validators.credentials import check_credentials, check_hash
import json
 
username = 'kizim'
password = 'kizim'
databaseName = "localhost:1521/xe"
 
connection = cx_Oracle.connect (username,password,databaseName)


@app.route('/')
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
	    title='contact',
	    year=datetime.now().year,
	    message='your contact page.'
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

@app.route('/login', methods=["GET"])
def login():
	if check_hash(connection) == True:
		return redirect('/me')
	
	return render_template('login.html', title="Login", year=datetime.now().year, message='Login via Telegram')

		

@app.route('/check', methods=["GET"])
def check():
	user_id = request.args.get('id')
	first_name = request.args.get('first_name')
	last_name = request.args.get('last_name')
	username = request.args.get('username')
	photo_url = request.args.get('photo_url')
	auth_date = request.args.get('auth_date')
	hash = request.args.get('hash')
	auth_array = [user_id, first_name, last_name, username, photo_url, auth_date, hash]

	result = check_credentials(auth_array)

	if result == 1:
		return render_template("404.html", error="Data is not from Telegram")
	if result == 2:
		return render_template("404.html", error="Credentials are outdated. Please re-login")

	response = make_response(redirect('/me'))
	
	response.set_cookie("educationreview_credits", hash, expires=datetime.now() + timedelta(days=1))
	session['key'] = hash
	cursor = connection.cursor()

	data = cursor.callfunc("USER_HANDLE.GET_USER", cx_Oracle.CURSOR, [user_id]).fetchone()
	if data == None:
		cursor.callproc("USER_HANDLE.add_user", [user_id, 'user', first_name + ' ' + last_name, hash])
	else:
		cursor.callproc("USER_HANDLE.update_hash", [user_id, hash])
			
	cursor.close()
	connection.commit()
	return response

@app.route('/me', methods=["GET"])
def me():

	if check_hash(connection) == True:
		cursor = connection.cursor()

		query = "select * from TABLE(USER_HANDLE.filter_users(NULL, NULL, '%s'))" % session['key']
		user_record = cursor.execute(query).fetchone()
		
		cursor.close()
		return render_template("me.html", user=user_record)

	response = make_response(redirect('/login'))
	response.set_cookie("educationreview_credits", '', expires=0)
	return response

@app.route('/logout', methods=["GET"])
def logout():
	session.pop('key', None)
	response = make_response(redirect('/'))
	response.set_cookie("educationreview_credits", '', expires=0)
	return response

