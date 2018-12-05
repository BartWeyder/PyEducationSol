import cx_Oracle
 
 
username = 'kizim'
password = 'kizim'
databaseName = "localhost:1521/xe"
 
connection = cx_Oracle.connect (username,password,databaseName)
 

 
"""------------QUERY 1------------------------------"""
 
#query = 'SELECT \'Hello from Oracle!\' FROM DUAL'
#print(query)
#cursor.execute (query)
cursor = connection.cursor()
user = cursor.callfunc("USER_HANDLE.GET_USER", cx_Oracle.CURSOR, [12])
#data = cursor.fetchone ()[0]
print (user.fetchone())
first_name = 'Bob'
last_name = 'Bobbovich'
hash = 'A123'
#user_record = cursor.callfunc("USER_HANDLE.filter_users", cx_Oracle.CURSOR, ['user', 'S', hash])
query = "select * from TABLE(USER_HANDLE.filter_users(NULL, NULL, '%s'))" % hash
a = cursor.execute(query)
l = a.fetchone()
print(l)
 
"""------------QUERY 2------------------------------"""
#query = 'select * from TABLE(user_handle.filter_users(NULL, NULL, NULL))'
#print(query)
#cursor.execute (query)
 
#data_ = cursor.fetchone()
#print (data_)
 
"""-------------------------------------------------"""
 
cursor.close ()
 
connection.close ()
