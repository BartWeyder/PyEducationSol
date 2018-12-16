import cx_Oracle
from dao.credentials import username, password, databaseName

def add_tag(title):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("TAG_HANDLE.add_tag", [title])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def delete_tag(title):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("TAG_HANDLE.delete_tag", [title])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def get_tag(title):
	if not title: return None
	
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	tag = cursor.callfunc("TAG_HANDLE.get_tag", cx_Oracle.CURSOR, [title]).fetchone()
	cursor.close()
	connection.close()

	return tag

def filter_tags(title):
	query = "select * from TABLE(TAG_HANDLE.filter_tags(:title))" 
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
