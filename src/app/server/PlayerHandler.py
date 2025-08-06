import sqlite3
from datetime import date

class PlayerHandler:
	def __init__(self, db_path):
		self.db_path = db_path
		self._create_tables()

	def _create_tables(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS suspensions (
				player_id INTEGER PRIMARY KEY,
				days INTEGER NOT NULL,
				reason TEXT NOT NULL,
				date TEXT NOT NULL
			)
		''')
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS warnings (
				player_id INTEGER PRIMARY KEY,
				reason TEXT NOT NULL,
				date TEXT NOT NULL
			)
		''')
		conn.commit()
		cursor.close()

	def suspend_player(self, player_id, days, reason):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			INSERT INTO suspensions (player_id, days, reason, date)
			VALUES (?, ?, ?, ?)
			ON CONFLICT(player_id) DO UPDATE SET
				days = excluded.days,
				reason = excluded.reason,
				date = excluded.date
		''', (player_id, days, reason, date.today().isoformat()))
		conn.commit()
		cursor.close()
		return {'status': 'success'}

	def warn_player(self, player_id, reason):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			INSERT INTO warnings (player_id, reason, date)
			VALUES (?, ?, ?)
			ON CONFLICT(player_id) DO UPDATE SET
				reason = excluded.reason,
				date = excluded.date
		''', (player_id, reason, date.today().isoformat()))
		conn.commit()
		cursor.close()
		return {'status': 'success'}

	def get_suspension(self, player_id):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('SELECT days, reason, date FROM suspensions WHERE player_id = ?', (player_id,))
		result = cursor.fetchone()
		cursor.close()
		if result:
			return {'days': result[0], 'reason': result[1], 'date': result[2]}
		return None

	def get_warning(self, player_id):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('SELECT reason, date FROM warnings WHERE player_id = ?', (player_id,))
		result = cursor.fetchone()
		cursor.close()
		if result:
			return {'reason': result[0], 'date': result[1]}
		return None

	def lift_suspension(self, player_id):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('DELETE FROM suspensions WHERE player_id = ?', (player_id,))
		conn.commit()
		cursor.close()

	def lift_warning(self, player_id):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('DELETE FROM warnings WHERE player_id = ?', (player_id,))
		conn.commit()
		cursor.close()
