import cx_Oracle
from dao.credentials import username, password, databaseName

def add_role(rolename):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("role_handle.add_role", [status, rolename])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def delete_role(rolename):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("role_handle.delete_role", [status, rolename])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def filter_roles(rolename=None):
	query = "select * from TABLE(role_handle.filter_roles(:rolename))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, rolename=rolename)
		data = cursor.fetchall()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return data
