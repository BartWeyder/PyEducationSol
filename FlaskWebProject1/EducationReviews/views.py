"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from forms.UserForm import UserForm
from forms.CategoryForm import CategoryForm
from forms.TagForm import TagForm
from forms.PostForm import PostForm
from forms.MangePosts import ManagePosts
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
		form = ManageUsers()
		if request.method == "GET":
			name = request.args.get('name')
			role = request.args.get('role')

			data = uh.filter_users(role, name, None)
			return render_template('users.html', data = data, form=form)

		if request.method == "POST":
			if form.validate():
				response = make_response(redirect(url_for('manage_users', name=request.form['name'], role=request.form['role'])))
				flash("Filters applied")
				return response
			return render_template('404.html', error="Validation violated")
	return render_template('404.html', error = 'You have no rights for this action')
	

@app.route('/manage/users/edit/<uid>', methods = ["GET", "POST"])
def manage_users_edit(uid):
	if check_hash() and get_role() == 'superuser':
		form = UserForm()
		if request.method == "GET":

			user = uh.get_user(uid)
			if user:
				form.role.data = user[1]
				form.name.data = user[2]
				form.status.data = user[5]
				return render_template('userform.html', user=user, form=form)
			return render_template('404.html', error = 'User does not exist')


		if request.method == "POST":
			if form.validate():
				try:
					uh.edit_user(uid, request.form['role'], request.form['name'], request.form['status'])
				except:
					return render_template('404.html', error = 'Something went wrong with information update')

				from_url = request.args.get('from')
				args = request.args.get('args')
				flash("Information updated")
				return redirect(from_url + '?' + args)

			return render_template('404.html', error="Validation violated")

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
		form = CategoryForm()
		if request.method == "GET":
			title = request.args.get('title')
			if title: form.title.data = title

			data = ch.filter_categories(title)
			return render_template('category.html', data = data, form=form)

		if request.method == "POST":
			if form.validate():

				response = make_response(redirect(url_for('manage_category', title=request.form['title'])))
				flash("Filters applied")
				return response
			return render_template('404.html', error="Validation violated")

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/category/add', methods = ["GET", "POST"])
def manage_category_add():
	if check_hash() and get_role() == 'superuser':
		form = CategoryForm()
		if request.method == "GET":
			return render_template('categoryform.html', form=form)

		if request.method == "POST":
			if form.validate():
				try:
					ch.add_category(request.form['title'])
				except:
					return render_template('404.html', error = 'Something went wrong while creation')
				response = make_response(redirect(url_for('manage_category')))
				flash("Category added")
				return response
			return render_template('404.html', error="Validation violated")

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
		form = CategoryForm()
		if request.method == "GET":
			title = request.args.get('title')
			if title: form.title.data = title

			try:
				data = th.filter_tags(title)
			except:
				return render_template('404.html', error = 'Can not get information :(')
			return render_template('tag.html', data = data, form=form)

		if request.method == "POST":
			if form.validate():
				response = make_response(redirect(url_for('manage_tag', title=request.form['title'])))
				flash("Filters applied")
				return response
			return render_template('404.html', error="Validation violated")

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/tag/add', methods = ["GET", "POST"])
def manage_tag_add():
	if check_hash() and get_role() == 'superuser':
		form = TagForm()	
		if request.method == "GET":
			return render_template('tagform.html', form=form)

		if request.method == "POST":
			if form.validate():
				try:
					th.add_tag(request.form['title'])
				except:
					return render_template('404.html', error = 'Something went wrong while creation')
				response = make_response(redirect(url_for('manage_tag')))
				flash("Tag added")
				return response
			return render_template('404.html', error="Validation violated")

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

@app.route('/post/add', methods = ["GET", "POST"])
def add_post():
	if check_hash():
		form = PostForm()
		
		#form.category.choices = category_list
		if request.method == "GET":
			return render_template('postform.html', form=form)
		if request.method == "POST":
			print('help')
			print(form.errors)
			if form.validate():
				try:
					user_id = uh.filter_users(None, None, session['key'])[0][0]
					pid = ph.add_post(user_id, request.form['title'], request.form['text'], request.form['category'])
					return redirect(url_for('view_post', pid=pid))
				except:
					return render_template('404.html', error="Error while creation")
			
			return render_template('404.html', error="Validation violated")
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/posts', methods=["GET", "POST"])
def manage_posts():
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		form = ManagePosts()
		categories = ch.filter_categories(None)
		category_list = []
		for category in categories:
			category_list.append((category[0], category[0]))
		form.category.choices = category_list
		if request.method == "GET":
				
			data = ph.filter_posts(None,None,None,None,None)
			new_data = []
			for rec in data:
				new_data.append((rec[0], uh.get_user(rec[1])[2], rec[2], rec[3],rec[4],rec[5],rec[6]))
				
			return render_template('posts.html', form=form, role=role, data=data)
				
		
		if request.method == "POST":
#if form.validate():
			try:
				
				categories = ch.filter_categories(None)
				category_list = []
				for category in categories:
					category_list.append((category[0], category[0]))
				form.category.choices = category_list
				
				users = uh.filter_users(None, request.form['author'], None)#[:-1][0]
				data = ph.filter_posts(users[0][0], request.form['title'], None, request.form['category'], None)
				for i in range(1,len(users)):
					dataset = ph.filter_posts(users[i][0], request.form['title'], None, 
								request.form['category'], NULL)
					for part in dataset:
						data.append(part)

				new_data = []
				for rec in data:
					new_data.append((rec[0], uh.get_user(rec[1])[2], rec[2], rec[3],rec[4],rec[5],rec[6]))
				
				

				#for rec in data:
				#	rec[1] = uh.get_user(rec[1])[2]

				form.author.data = request.form['author']
				form.category.data = request.form['category']
				form.title.data = request.form['title']
				
				return render_template('posts.html', form=form, role=role, data=new_data)
			except:
				return render_template('404.html', error = 'Cant load information')
		#return render_template('404.html', error="Validation violated")

	return render_template('404.html', error = 'You have no rights for this action')


@app.route('/post/edit/<pid>', methods = ["GET", "POST"])
def edit_post(pid):
	if check_hash():
		form = PostForm()
		categories = ch.filter_categories(None)
		category_list = []
		for category in categories:
			category_list.append((category[0], category[0]))
		form.category.choices = category_list
		data = ph.get_post(pid)
		if get_role() == 'superuser' or data[0] == uh.user_by_hash(session['key']):
			if request.method == "GET":
				form.title.data = data[2]
				form.text.data = data[3]
				form.category.data = data[6]
				return render_template("postform.html", form=form)
			if request.method == "POST":
				if form.validate():
					try:
						ph.edit_post(pid, request.form['title'], request.form['text'], request.form['category'])
						flash('Post edited successfully')
						return redirect(url_for('view_post', pid=pid))
					except:
						return render_template('404.html', error='Error while editing')
			return render_template('404.html', error="Validation violated")
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/posts/<pid>/hide', methods = ["GET"])
def hide_post(pid):
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		try:
			ph.hide_post(pid)
			flash("Post was hidden")
			return redirect(url_for('manage_posts'))
		except:
			return render_template('404.html', error='Error while hiding')

	return render_template('404.html', error = 'You have no rights for this action')
	
@app.route('/manage/posts/<pid>/publicate', methods = ["GET"])
def publicate_post(pid):
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		try:
			ph.publicate_post(pid)
			flash("Post was published")
			return redirect(url_for('manage_posts'))
		except:
			return render_template('404.html', error='Error while hiding')

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/posts/<pid>/remove', methods = ["GET"])
def remove_post(pid):
	role = get_role()
	if check_hash():
		if  (role == 'user' and ph.get_post(pid)[1] == uh.user_by_hash(session['key'])) or role=='moderator' or role=='superuser':
			try:
				ph.publicate_post(pid)
				flash("Post was removed")
				if role=='user':
					return redirect('/')
				return redirect(url_for('manage_posts'))
			except:
				return render_template('404.html', error='Error while hiding')

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/post/<pid>', methods = ["GET"])
def view_post(pid):
	if check_hash():
		data = None
		author = None
		try:
			data = ph.get_post(pid)
			author = uh.get_user(data[1])[2]
		except:
			return render_template('404.html', error='Error while getting info')
		if data[4] != 1 and get_role() == 'user':
			return render_template('404.html', error = 'Post not found')
		return render_template('post.html', post=data, author=author)
	return render_template('404.html', error = 'You have no rights for this action')
