from app.services import USERS

def verify_user(userid, min_rights: int = 0):
	return userid and USERS.get_user(userid) and USERS.get_user_rights(userid) >= min_rights
