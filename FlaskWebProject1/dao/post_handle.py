import cx_Oracle
from dao.credentials import username, password, databaseName

def add_post(uid, title, text, category):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("POST_HANDLE.add_post", [uid, title, text, category])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

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
		cursor.callproc("POST_HANDLE.publicate_post", [pid])
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
		cursor.callproc("POST_HANDLE.hide_post", [pid])
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

def filter_posts(uid, title, text, category):
	query = "select * from TABLE(POST_HANDLE.filter_posts(:uid, :title, :text, :category))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, uid=uid, title=title, text=text, category=category)
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