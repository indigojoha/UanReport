from app.services import USERS

def verify_user(userid):
	return userid and USERS.get_user(userid)
