"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from forms.UserForm import UserForm
from flask import render_template, request, redirect, make_response, session, flash, url_for
from EducationReviews import app
import cx_Oracle
import dao.user_handle as uh
from forms.ManageUsers import ManageUsers
from validators.credentials import check_credentials, check_hash, get_role
import json
 
username = 'kizim'
password = 'kizim'
databaseName = "localhost:1521/xe"
 
#connection = cx_Oracle.connect (username,password,databaseName)


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
	if check_hash() == True:
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
	hash_ = request.args.get('hash')
	auth_array = [user_id, first_name, last_name, username, photo_url, auth_date, hash_]

	result = check_credentials(auth_array)

	if result == 1:
		return render_template("404.html", error="Data is not from Telegram")
	if result == 2:
		return render_template("404.html", error="Credentials are outdated. Please re-login")

	response = make_response(redirect('/me'))
	
	response.set_cookie("educationreview_credits", hash_, expires=datetime.now() + timedelta(days=1))
	session['key'] = hash_
	

	data = uh.get_user(user_id)
	if data == None:
		uh.add_user(user_id,  first_name + ' ' + last_name, hash_)
	else:
		uh.update_hash(user_id, hash_)
			
	return response

@app.route('/me', methods=["GET"])
def me():

	if check_hash() == True:
		user_record = uh.filter_users(None, None, session['key'])
		return render_template("me.html", user=user_record[0])

	response = make_response(redirect('/login'))
	response.set_cookie("educationreview_credits", '', expires=0)
	return response

@app.route('/logout', methods=["GET"])
def logout():
	session.pop('key', None)
	response = make_response(redirect('/'))
	response.set_cookie("educationreview_credits", '', expires=0)
	return response

@app.route('/manage/users', methods = ["GET", "POST"])
def manage_users():
	if check_hash() and get_role() == 'superuser':
		if request.method == "GET":
			form = ManageUsers()
			name = request.args.get('name')
			role = request.args.get('role')

			data = uh.filter_users(role, name, None)
			return render_template('users.html', data = data, form=form)

		if request.method == "POST":
			response = make_response(redirect(url_for('manage_users', name=request.form['name'], role=request.form['role'])))
			flash("Filters applied")
			return response

	return render_template('404.html', error = 'You have no rights for this action')
	

@app.route('/manage/users/edit/<uid>', methods = ["GET", "POST"])
def manage_users_edit(uid):
	if check_hash() and get_role() == 'superuser':
		if request.method == "GET":

			user = uh.get_user(uid)
			if user:
				form = UserForm()
				form.role.data = user[1]
				form.name.data = user[2]
				form.status.data = user[5]
				return render_template('userform.html', user=user, form=form)
			return render_template('404.html', error = 'User does not exist')


		if request.method == "POST":
			try:
				uh.edit_user(uid, request.form['role'], request.form['name'], request.form['status'])
			except:
				return render_template('404.html', error = 'Something went wrong with information update')

			from_url = request.args.get('from')
			args = request.args.get('args')
			flash("Information updated")
			return redirect(from_url + '?' + args)

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/users/block/<uid>', methods = ["GET"])
def manage_users_block(uid):
	if check_hash() and get_role() == 'superuser':
		try:
			uh.block_user(uid)
		except:
			return render_template('404.html', error = 'Something went wrong during blocking')
		from_url = request.args.get('from')
		args = request.args.get('args')
		flash("User blocked")
		return redirect(from_url + '?' + args)
	return render_template('404.html', error = 'You have no rights for this action')