from app.server.Paths import Paths
import os
import json
from datetime import date

class PlayerHandler:
	def __init__(self):
		self.JSON_PATH = ''
		self.suspensions = {}

	def suspend_player(self, player_id, days, reason):
		self.suspensions[player_id] = (days, reason, date.today().isoformat())
		return {'status': 'success', 'message': f'Player {player_id} suspended for {days} days due to {reason}'}

	def lift_suspension(self, player_id):
		if player_id in self.suspensions:
			del self.suspensions[player_id]

	def load_json(self):
		Paths.ensure_directories(self.JSON_PATH)

		if os.path.exists(self.JSON_PATH):
			with open(self.JSON_PATH, 'r', encoding='utf-8') as file:
				self.suspensions = json.load(file)
				file.close()
		else:
			print(f"File {self.JSON_PATH} not found. Using empty suspensions.")
			self.suspensions = {}

	def save_json(self):
		Paths.ensure_directories(self.JSON_PATH)

		with open(self.JSON_PATH, 'w', encoding='utf-8') as file:
			json.dump(self.suspensions, file, indent=4)
			file.flush()
			os.fsync(file.fileno())
			file.close()
