"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from forms.UserForm import UserForm
from forms.CategoryForm import CategoryForm
from forms.TagForm import TagForm
from flask import render_template, request, redirect, make_response, session, flash, url_for
from EducationReviews import app
import cx_Oracle
import dao.user_handle as uh
import dao.post_handle as ph
import dao.category_handle as ch
import dao.tag_handle as th
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

@app.route('/manage/category', methods = ["GET", "POST"])
def manage_category():
	if check_hash() and get_role() == 'superuser':
		if request.method == "GET":
			form = CategoryForm()
			title = request.args.get('title')
			if title: form.title.data = title

			data = ch.filter_categories(title)
			return render_template('category.html', data = data, form=form)

		if request.method == "POST":
			response = make_response(redirect(url_for('manage_category', title=request.form['title'])))
			flash("Filters applied")
			return response

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/category/add', methods = ["GET", "POST"])
def manage_category_add():
	if check_hash() and get_role() == 'superuser':
		if request.method == "GET":
			form = CategoryForm()
			return render_template('categoryform.html', form=form)

		if request.method == "POST":
			try:
				ch.add_category(request.form['title'])
			except:
				return render_template('404.html', error = 'Something went wrong while creation')
			response = make_response(redirect(url_for('manage_category')))
			flash("Category added")
			return response

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/category/delete/<title>', methods = ["GET"])
def manage_category_delete(title):
	if check_hash() and get_role() == 'superuser':
		try:
			ch.delete_category(title)
		except:
			return render_template('404.html', error = 'Something went wrong while deletion')
		args = request.args.get('args')
		response = make_response(redirect(url_for('manage_category') + '?' + args))
		flash("Category deleted")
		return response
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/tag', methods = ["GET", "POST"])
def manage_tag():
	if check_hash() and get_role() in ('superuser', 'moderator'):
		if request.method == "GET":
			form = CategoryForm()
			title = request.args.get('title')
			if title: form.title.data = title

			try:
				data = th.filter_tags(title)
			except:
				return render_template('404.html', error = 'Can not get information :(')
			return render_template('tag.html', data = data, form=form)

		if request.method == "POST":
			response = make_response(redirect(url_for('manage_tag', title=request.form['title'])))
			flash("Filters applied")
			return response

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/tag/add', methods = ["GET", "POST"])
def manage_tag_add():
	if check_hash() and get_role() == 'superuser':
		if request.method == "GET":
			form = TagForm()
			return render_template('tagform.html', form=form)

		if request.method == "POST":
			try:
				th.add_tag(request.form['title'])
			except:
				return render_template('404.html', error = 'Something went wrong while creation')
			response = make_response(redirect(url_for('manage_tag')))
			flash("Tag added")
			return response

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/tag/delete/<title>', methods = ["GET"])
def manage_tag_delete(title):
	if check_hash() and get_role() == 'superuser':
		try:
			th.delete_tag(title)
		except:
			return render_template('404.html', error = 'Something went wrong while deletion')
		args = request.args.get('args')
		response = make_response(redirect(url_for('manage_tag') + '?' + args))
		flash("Tag deleted")
		return response
	return render_template('404.html', error = 'You have no rights for this action')
#@app.route('/post/add', methods = ["GET", "POST"])
#def add_post():
#	if check_hash():
#		if request.method == "GET":
#			return
#		if request.method == "POST":
#			try:
#				user_id = uh.filter_users(None, None, session['key'])[0][0]
#				ph.add_post(user_id, request.form['title'], request.form['text'], request.form['category'])

#	return redirect('/login')