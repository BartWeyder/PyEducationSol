import cx_Oracle
from dao.credentials import username, password, databaseName
from dao.category_handle import filter_categories

def add_post(uid, title, text, category):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	pid = cursor.callfunc("POST_HANDLE.add_post", cx_Oracle.NUMBER, [status, uid, title, text, category])
	connection.commit()
	cursor.close()
	connection.close()
	return pid, status.getvalue()

def edit_post(pid, title, text, category):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("POST_HANDLE.edit_post", [status, pid, title, text, category])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def delete_post(pid):
	#connection = cx_Oracle.connect(username, password, databaseName)
	#cursor = connection.cursor()
	#status = cursor.var(cx_Oracle.STRING)
	#cursor.callproc("POST_HANDLE.delete_post", [status, pid])
	#connection.commit()
	#cursor.close()
	#connection.close()
	#return status.getvalue()
	hide_post(pid)

def publicate_post(pid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("POST_HANDLE.publicate", [status, pid])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def hide_post(pid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("POST_HANDLE.hide_post", [status, pid])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

#def remove_post(pid):
#	connection = cx_Oracle.connect(username, password, databaseName)
#	cursor = connection.cursor()
#	status = cursor.var(cx_Oracle.STRING)
#	cursor.callproc("POST_HANDLE.set_status", [status, pid, 2])
#	connection.commit()
#	cursor.close()
#	connection.close()
#	return status.getvalue()

def add_tag_to_post(pid, tag):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("POST_HANDLE.add_tag_to_post", [status, pid, tag])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def delete_tag_from_post(pid, tag):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("POST_HANDLE.delete_tag_from_post", [status, pid, tag])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def get_post(pid):
	if not pid: return None
	
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	post = cursor.callfunc("POST_HANDLE.get_post", cx_Oracle.CURSOR, [pid]).fetchone()
	cursor.close()
	connection.close()

	return post

def filter_posts(uid_=None, title_=None, text_=None, category_=None, status_=None):
	query = "select * from TABLE(POST_HANDLE.filter_posts(:uid_, :title_, :text_, :category_, :status_))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, uid_=uid_, title_=title_, text_=text_, category_=category_, status_=status_)
		data = cursor.fetchall()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return data

def get_post_tags(pid):
	query = "select * from TABLE(POST_HANDLE.get_post_tags(:pid))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, pid=pid)
		data = cursor.fetchall()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return data

def get_all():
	categories = filter_categories(None)
	category_list = []
	for category in categories:
		category_list.append((category[0], category[0]))
	return category_list