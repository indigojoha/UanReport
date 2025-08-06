import app.server.Rights as Rights
import sqlite3

class Users:
	def __init__(self, db_path):
		self.db_path = db_path
		self._create_table()

	def _create_table(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS users (
				userid TEXT PRIMARY KEY,
				name TEXT NOT NULL,
				rights INTEGER NOT NULL
			)
		''')

		cursor.execute('SELECT COUNT(*) FROM users')
		if cursor.fetchone()[0] == 0:
			self.add_or_update_user_cursor('xPcjadIroO92dAN', 'Johanna', Rights.PASS_WARN_BAN, cursor)
			self.add_or_update_user_cursor('zgyf3HnHQaZWI13', 'Niku', Rights.PASS_WARN_BAN, cursor)

		conn.commit()
		cursor.close()

	def get_user(self, userid):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('SELECT name, rights FROM users WHERE userid = ?', (userid,))
		result = cursor.fetchone()
		cursor.close()
		return result if result else None

	def get_user_rights(self, userid):
		user = self.get_user(userid)
		return user[1] if user else Rights.NONE

	def add_or_update_user_cursor(self, userid, name, rights, cursor:sqlite3.Cursor):
		cursor.execute('''
			INSERT INTO users (userid, name, rights)
			VALUES (?, ?, ?)
			ON CONFLICT(userid) DO UPDATE SET
				name = excluded.name,
				rights = excluded.rights
		''', (userid, name, rights))

	def add_or_update_user(self, userid, name, rights):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			INSERT INTO users (userid, name, rights)
			VALUES (?, ?, ?)
			ON CONFLICT(userid) DO UPDATE SET
				name = excluded.name,
				rights = excluded.rights
		''', (userid, name, rights))
		conn.commit()
		cursor.close()
