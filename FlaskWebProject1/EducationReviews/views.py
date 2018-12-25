"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from forms.UserForm import UserForm
from forms.CategoryForm import CategoryForm
from forms.TagForm import TagForm
from forms.PostForm import PostForm
from forms.MangePosts import ManagePosts
from forms.AddTagForm import AddTagForm
from forms.AnswerForm import AnswerForm
from forms.RoleForm import RoleForm
from flask import render_template, request, redirect, make_response, session, flash, url_for
from EducationReviews import app
import cx_Oracle
import dao.user_handle as uh
import dao.post_handle as ph
import dao.category_handle as ch
import dao.tag_handle as th
import dao.answer_handle as ah
import dao.role_handle as rh
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
    data = ph.filter_posts()
    return render_template(
        'all.html',
        title='Feed',
        year=datetime.now().year,
		data=data
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
		status = uh.add_user(user_id,  first_name + ' ' + last_name, hash_)
		if status!='ok': return render_template('404.html', error=status)
	else:
		status = uh.update_hash(user_id, hash_)
		if status!='ok': return render_template('404.html', error=status)
			
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
				status = uh.edit_user(uid, request.form['role'], request.form['name'], request.form['status'])
				if status != 'ok': render_template('404.html', error = status)

				from_url = request.args.get('from')
				args = request.args.get('args')
				flash("Information updated")
				return redirect(from_url + '?' + args)

			return render_template('404.html', error="Validation violated")

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/users/block/<uid>', methods = ["GET"])
def manage_users_block(uid):
	if check_hash() and get_role() == 'superuser':
		status = uh.block_user(uid)
		if status != 'ok': return render_template('404.html', error = status)
		from_url = request.args.get('from')
		args = request.args.get('args')
		flash("User blocked")
		return redirect(from_url + '?' + args)
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/users/unblock/<uid>', methods = ["GET"])
def manage_users_unblock(uid):
	if check_hash() and get_role() == 'superuser':
		status = uh.unblock_user(uid)
		if status != 'ok': return render_template('404.html', error = status)
		from_url = request.args.get('from')
		args = request.args.get('args')
		flash("User unblocked")
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
				status = ch.add_category(request.form['title'])
				if status != 'ok' : return render_template('404.html', error = status)
				response = make_response(redirect(url_for('manage_category')))
				flash("Category added")
				return response
			return render_template('404.html', error="Validation violated")

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/category/delete/<title>', methods = ["GET"])
def manage_category_delete(title):
	if check_hash() and get_role() == 'superuser':
		status = ch.delete_category(title)
		if status !='ok' : return render_template('404.html', error=status)
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
				status = th.add_tag(request.form['title'])
				if status != 'ok': return render_template('404.html', error=status)
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
		
		if request.method == "GET":
			return render_template('postform.html', form=form)
		if request.method == "POST":
			print('help')
			print(form.errors)
			if form.validate():
				user_id = uh.filter_users(None, None, session['key'])[0][0]
				pid, status = ph.add_post(user_id, request.form['title'], request.form['text'], request.form['category'])
				if status!='ok': return render_template('404.html', error=status)
				flash('Post added successfully')
				return redirect(url_for('view_post', pid=pid))
			
			return render_template('404.html', error="Validation violated")
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/posts', methods=["GET", "POST"])
def manage_posts():
	role = get_role()
	if check_hash(): #and (role == 'superuser' or role == 'moderator'):
		form = ManagePosts()
		categories = ch.filter_categories(None)
		category_list = []
		for category in categories:
			category_list.append((category[0], category[0]))
		form.category.choices = category_list
		if request.method == "GET":
			data = None
			if role == 'superuser' or role == 'moderator': data = ph.filter_posts(status_=datetime.now())
			if role == 'user': data = ph.filter_posts()
			new_data = []
			for rec in data:
				new_data.append((rec[0], uh.get_user(rec[1])[2], rec[2], rec[3],rec[4],rec[5],rec[6]))
				
			return render_template('posts.html', form=form, role=role, data=data)
				
		
		if request.method == "POST" and (role == 'superuser' or role == 'moderator'):
			try:
				categories = ch.filter_categories(None)
				category_list = []
				for category in categories:
					category_list.append((category[0], category[0]))
				form.category.choices = category_list
				
				users = uh.filter_users(None, request.form['author'], None)
				data = ph.filter_posts(users[0][0], request.form['title'], None, request.form['category'], datetime.now())
				for i in range(1,len(users)):
					dataset = ph.filter_posts(users[i][0], request.form['title'], None, 
								request.form['category'], datetime.now())
					for part in dataset:
						data.append(part)

				new_data = []
				for rec in data:
					new_data.append((rec[0], uh.get_user(rec[1])[2], rec[2], rec[3],rec[4],rec[5],rec[6]))

				form.author.data = request.form['author']
				form.category.data = request.form['category']
				form.title.data = request.form['title']
				
				return render_template('posts.html', form=form, role=role, data=new_data)
			except:
				return render_template('404.html', error = 'Cant load information')

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
					status = ph.edit_post(pid, request.form['title'], request.form['text'], request.form['category'])
					if status!='ok': return render_template('404.html', error='Error while editing')
					flash('Post edited successfully')
					return redirect(url_for('view_post', pid=pid))
			return render_template('404.html', error="Validation violated")
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/posts/<pid>/hide', methods = ["GET"])
def hide_post(pid):
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		status = ph.hide_post(pid)
		if status != 'ok': return render_template('404.html', error=status)
		flash("Post was hidden")
		return redirect(url_for('manage_posts'))

	return render_template('404.html', error = 'You have no rights for this action')
	
@app.route('/manage/posts/<pid>/publicate', methods = ["GET"])
def publicate_post(pid):
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		status = ph.publicate_post(pid)
		if status != 'ok': return render_template('404.html', error=status)
		flash("Post was published")
		return redirect(url_for('manage_posts'))

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/posts/<pid>/remove', methods = ["GET"])
def remove_post(pid):
	role = get_role()
	if check_hash():
		if  (role == 'user' and ph.get_post(pid)[1] == uh.user_by_hash(session['key'])) or role=='moderator' or role=='superuser':
			status = ph.hide_post(pid)
			if status!='ok': return render_template('404.html', error=status)
			flash("Post was removed")
			if role=='user':
				return redirect('/')
			return redirect(url_for('manage_posts'))

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/post/<pid>', methods = ["GET", "POST"])
def view_post(pid):

	role = get_role()
	
	answer_form = None
	tag_form = None
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		answer_form = AnswerForm()

	if (role == 'user' and ph.get_post(pid)[1] == uh.user_by_hash(session['key'])) or role=='moderator' or role=='superuser':
		tag_form = AddTagForm()
		p_data = None
		all_data = None
		try:
			p_data = ph.get_post_tags(pid)
			all_data = th.filter_tags(None)
		except:
			return render_template('404.html', error='Error while getting info')

		data = [value for value in all_data if value not in p_data]
		choices = []
		for rec in data:
			choices.append((rec[0], rec[0]))
		tag_form.tag.choices = choices

	if request.method == "GET":
		data = None
		author = None
		answer = None
		try:
			data = ph.get_post(pid)
			author = uh.get_user(data[1])[2]
			tags = ph.get_post_tags(pid)
			answer = ah.filter_answers(None, None, pid, None)
			if answer:
				answer = answer[0]
				if answer_form:
					answer_form.title.data = answer[3]
					answer_form.text.data = answer[4]
				l = list(answer)
				l[1] = uh.get_user(l[1])[2]
				answer = tuple(l)

		except:
			return render_template('404.html', error='Error while getting info')
		if data[4] == None and role == 'user':
			return render_template('404.html', error = 'Post not found')
		return render_template('post.html', post=data, author=author, tags=tags, answer=answer,
						 answer_form=answer_form, tag_form=tag_form)

	if request.method == "POST":
		if tag_form.validate(): 
			status = ph.add_tag_to_post(pid, request.form['tag'])
			if status != 'ok': return render_template('404.html', error=status)
		else: 
			return render_template('404.html', error="Validation violated")
						
		return redirect(url_for('view_post', _anchor='tag', pid=pid))

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/post/<pid>/tags', methods=["GET", "POST"])
def manage_tags(pid):
	if check_hash():
		role = get_role()
		if  (role == 'user' and ph.get_post(pid)[1] == uh.user_by_hash(session['key'])) or role=='moderator' or role=='superuser':
			form = AddTagForm()
			p_data = None
			all_data = None
			try:
				p_data = ph.get_post_tags(pid)
				all_data = th.filter_tags(None)
			except:
				return render_template('404.html', error='Error while getting info')

			data = [value for value in all_data if value not in p_data]
			choices = []
			for rec in data:
				choices.append((rec[0], rec[0]))
			form.tag.choices = choices	
			if request.method == "GET":
					return render_template('posttags.html', pid=pid, form=form, data=p_data)
					
			if request.method == "POST":
				if form.validate():
					status = ph.add_tag_to_post(pid, request.form['tag'])
					if status != 'ok': return render_template('404.html', error=status)
					
					return redirect(url_for('manage_tags', pid=pid))

				return render_template('404.html', error="Validation violated")

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/post/<pid>/remove/<tag>', methods = ['GET'])
def remove_tag_from_post(pid, tag):
	if check_hash():
		role = get_role()
		if  (role == 'user' and ph.get_post(pid)[1] == uh.user_by_hash(session['key'])) or role=='moderator' or role=='superuser':
			status = ph.delete_tag_from_post(pid, tag)
			if status != 'ok': return render_template('404.html', error = status)
			flash('Tag successfully deleted from post')
			return redirect(url_for('view_post',_anchor='tag', pid=pid))

	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/post/<pid>/add-answer', methods=["POST"])
def add_answer(pid):
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		form = AnswerForm()
		if request.method == "GET":
			try:
				post = ph.get_post(pid)
			except:
				return render_template('404.html', error = 'Error while getting post info')

			return render_template('answerform.html', form=form, data=post)
		if request.method == 'POST':
			status = "ok"
			author = uh.user_by_hash(session['key'])[0]
			status = ah.add_answer(author, pid, request.form['title'], request.form['text'])[1]
			if status != "ok": return render_template('404.html', error = status)
			flash('Answer successfully added')
			return redirect(url_for('view_post', pid=pid))
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/answer/edit/<aid>', methods=['POST'])
def edit_answer(aid):
	role = get_role()
	answer = ah.get_answer(aid)
	if check_hash() and (role == 'superuser' or (role == 'moderator' and \
		answer[1] == uh.user_by_hash(session['key']))):
		form = AnswerForm()
		if form.validate():
			status = ah.edit_answer(aid, request.form['title'], request.form['text'])
			if status != 'ok': return render_template('404.html', error=status)
			return redirect(url_for('view_post', pid=answer[2]))
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/answer/remove/<aid>', methods=['GET'])
def remove_answer(aid):
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		pid = ah.get_answer(aid)[2]
		status = ah.delete_answer(aid)
		if status != 'ok': return render_template('404.html', error=status)
		flash('Answer successfully deleted')
		if pid == None: return redirect('/')
		return redirect(url_for('view_post', pid=pid))
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/roles', methods=['GET', 'POST'])
def manage_roles():
	if check_hash() and get_role() == 'superuser':
		form = RoleForm()
		if method == 'GET':
			data = rh.filter_roles()
			return render_template('roles.html', data=data, form=form)
		if method == 'POST':
			if form.validate():
				status = rh.add_role(request.form['rolename'])
				if status != 'ok': return render_template('404.html', error=status)
				flash('Role added')
				return redirect(url_for('manage_roles'))
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/manage/roles/delete/<rolename>', methods=['GET'])
def delete_role(rolename):
	if check_hash() and get_role() == 'superuser':
		status = rh.delete_role(rolename)
		if status != 'ok': return render_template('404.html', error=status)
		flash('Role deleted')
		return redirect(url_for('manage_roles'))
	return render_template('404.html', error = 'You have no rights for this action')

@app.route('/admin')
def admin_page():
	role = get_role()
	if check_hash() and (role == 'superuser' or role == 'moderator'):
		return render_template('adminpage.html', role=role)