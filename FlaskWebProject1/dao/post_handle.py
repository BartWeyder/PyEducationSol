import cx_Oracle
from dao.credentials import username, password, databaseName
from dao.category_handle import filter_categories

def add_post(uid, title, text, category):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		pid = cursor.callfunc("POST_HANDLE.add_post", cx_Oracle.NUMBER, [uid, title, text, category])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return pid

def edit_post(pid, title, text, category):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.edit_post", [pid, title, text, category])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def delete_post(pid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.delete_post", [pid])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def publicate_post(pid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.set_status", [pid, 1])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def hide_post(pid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.set_status", [pid, 0])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def remove_post(pid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.set_status", [pid, 2])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def add_tag_to_post(pid, tag):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.add_tag_to_post", [pid, tag])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def delete_tag_from_post(pid, tag):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.delete_tag_from_post", [pid, tag])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def get_post(pid):
	if not pid: return None
	
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	post = cursor.callfunc("POST_HANDLE.get_post", cx_Oracle.CURSOR, [pid]).fetchone()
	cursor.close()
	connection.close()

	return post

def filter_posts(uid_, title_, text_, category_, status_):
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