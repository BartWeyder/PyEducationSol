import cx_Oracle
from dao.credentials import username, password, databaseName
from dao.user_handle import filter_users
from datetime import datetime

def users_activity(date_from = None, date_till = datetime.now()):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	query = "select * from TABLE(analytics.users_activity(:date_from, :date_till))" 
	cursor.execute(query, date_from=date_from, date_till=date_till)
	data = cursor.fetchall()
	return data

def tag_use_rate(date_from = None, date_till = datetime.now()):
	connection = cx_Oracle.connect(username, password, databaseName)
	cursor = connection.cursor()
	query = "select * from TABLE(analytics.tag_use_rate(:date_from, :date_till))" 
	cursor.execute(query, date_from=date_from, date_till=date_till)
	data = cursor.fetchall()
	return data
	