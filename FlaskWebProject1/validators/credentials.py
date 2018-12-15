import hmac
import hashlib
from time import time
from flask import session, request
from dao.user_handle import filter_users

def check_credentials(auth_array):
	BOT_TOKEN = b"785636304:AAFl-095ihh8eOTr6grLYCHydPN0MacDbY4";
	check_arr = ['id=' + auth_array[0], 'first_name=' + auth_array[1], 'last_name=' + auth_array[2],
	   'username=' + auth_array[3], 'photo_url=' + auth_array[4], 'auth_date=' + auth_array[5]]
	check_arr.sort()
	check_string = '\n'.join(check_arr)
	print(check_string)
	key = hashlib.sha256(BOT_TOKEN).digest()
	h = hmac.new(key, check_string.encode(), hashlib.sha256)
	if auth_array[6] != h.hexdigest():
		return 1
	if time() - float(auth_array[5]) > 8400:
		return 2
	return 0

def check_hash():
	
	if 'key' in session:
		hash_ = session['key']
	else:
		hash_ = request.cookies.get("educationreview_credits")
		if hash_ == None:
			return False

	user_record = filter_users(None, None, hash_)

	if user_record != None:
		session['key'] = hash_
		return True
	session.pop('key', None)
	return False
	
def get_role():

	hash_ = session['key']
	user_record = filter_users(None, None, hash_)[0]
	if user_record != None:
		return user_record[1]
	return None


