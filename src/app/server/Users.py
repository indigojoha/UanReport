import os
import json

class Users:
	def __init__(self):
		self.JSON_PATH = ''
		self.users = {}

	def get_user(self, userid):
		if userid in self.users:
			return self.users[userid]
		else:
			return None

	def get_user_rights(self, userid):
		user = self.get_user(userid)
		if user:
			return user[1]
		return -1

	def load_json(self):
		try:
			with open(self.JSON_PATH, 'r', encoding='utf-8') as file:
				data = json.load(file)
				self.users = {userid: [user_data['name'], user_data['rights']] for userid, user_data in data.items()}
				file.close()
		except FileNotFoundError:
			print(f"File {self.JSON_PATH} not found. Using default users.")
	
	def save_json(self):
		data = {userid: {'name': user[0], 'rights': user[1]} for userid, user in self.users.items()}

		with open(self.JSON_PATH, 'w', encoding='utf-8') as file:
			json.dump(data, file, indent=4)
			file.flush()
			os.fsync(file.fileno())
			file.close()