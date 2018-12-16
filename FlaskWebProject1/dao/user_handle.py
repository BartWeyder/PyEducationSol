import cx_Oracle
from dao.credentials import username, password, databaseName

def get_user(id):
	if not id: return None
	
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	user = cursor.callfunc("USER_HANDLE.GET_USER", cx_Oracle.CURSOR, [id]).fetchone()
	cursor.close()
	connection.close()

	return user

def filter_users(rolename, name, hash_):

	query = "select * from TABLE(USER_HANDLE.filter_users(:role, :name, :hash_))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, role=rolename, name=name, hash_=hash_)
		data = cursor.fetchall()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return data

def add_user(id, name, hash_):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("USER_HANDLE.add_user", [id, 'user', name, hash_])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	
def edit_user(id, rolename, name, status):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("USER_HANDLE.edit_user", [id, rolename, name, status])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def delete_user (id):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("USER_HANDLE.delete_user", [id])
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def update_hash(id, hash_):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("USER_HANDLE.update_hash", [id, hash_])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def get_hash (id):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	hash_ = None
	try:
		hash_ = cursor.callfunc("USER_HANDLE.get_hash", cx_Oracle.STRING, [id])
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return hash_

def block_user(id):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("USER_HANDLE.block_user", [id])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def user_by_hash(hash_):
	return filter_users(None, None, hash_)[0]