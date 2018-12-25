import cx_Oracle
from dao.credentials import username, password, databaseName

def add_category(title):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("CATEGORY_HANDLE.add_category", [status,title])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def delete_category(title):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	status = cursor.var(cx_Oracle.STRING)
	cursor.callproc("CATEGORY_HANDLE.delete_category", [status,title])
	connection.commit()
	cursor.close()
	connection.close()
	return status.getvalue()

def get_category(title):
	if not title: return None
	
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	category = cursor.callfunc("CATEGORY_HANDLE.get_category", cx_Oracle.CURSOR, [title]).fetchone()
	cursor.close()
	connection.close()

	return category

def filter_categories(title=None):
	query = "select * from TABLE(CATEGORY_HANDLE.filter_categories(:title))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, title=title)
		data = cursor.fetchall()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return data
