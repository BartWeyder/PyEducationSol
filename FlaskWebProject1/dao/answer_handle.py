import cx_Oracle
from dao.credentials import username, password, databaseName
from dao.user_handle import filter_users

def add_answer(user_id, pid_, answertitle, answertext):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callfunc("ANSWER_HANDLE.add_answer", cx_Oracle.NUMBER, [user_id, pid_, answertitle, answertext])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def edit_answer(aid, answertitle, answertext):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("ANSWER_HANDLE.edit_answer", [aid, answertitle, answertext])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def delete_answer(aid):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.callproc("ANSWER_HANDLE.delete_answer", [aid])
		connection.commit()
	except:
		raise
	finally:
		cursor.close()
		connection.close()

def get_answer(aid):
	if not aid: return None
	
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	answer = cursor.callfunc("ANSWER_HANDLE.get_answer", cx_Oracle.CURSOR, [aid]).fetchone()
	cursor.close()
	connection.close()

	return answer

def filter_answers(title, user_id, pid, answertext):
	query = "select * from TABLE(ANSWER_HANDLE.filter_answers(:title, :user_id, :pid, :answertext))" 
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	try:
		cursor.execute(query, title=title, user_id=user_id, pid=pid, answertext=answertext)
		data = cursor.fetchall()
	except:
		raise
	finally:
		cursor.close()
		connection.close()
	return data

def get_answer_by_username(name):
	users = filter_users(None, name, None)
	result = []
	for user in users:
		data = filter_answers(None, user[0], None)
		for item in data:
			l = list(item)
			l[1] = user[2]
			result.append(tuple(l))
	return result
