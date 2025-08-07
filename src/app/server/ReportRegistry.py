import sqlite3
from datetime import date

class Report:
	def __init__(self, reporter, reported, reason, date, teams):
		self.reporter = reporter
		self.reported = reported
		self.reason = reason
		self.date = date
		self.teams = teams # despite the name, it's a single string 
		self.resolution = ''

	def to_tuple(self):
		return (
			self.reporter,
			self.reported,
			self.reason,
			self.date,
			self.teams,
			self.resolution
		)

	def to_dict(self):
		return {
			'reporter': self.reporter,
			'reported': self.reported,
			'reason': self.reason,
			'date': self.date,
			'teams': self.teams,
			'resolution': self.resolution
		}

class ReportRegistry:
	def __init__(self, db_path):
		self.db_path = db_path
		self._create_table()

	def _create_table(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS reports (
				report_id TEXT PRIMARY KEY,
				reporter TEXT NOT NULL,
				reported TEXT NOT NULL,
				reason TEXT NOT NULL,
				date TEXT NOT NULL,
				teams TEXT NOT NULL,
				resolution TEXT
			)
		''')
		conn.commit()
		cursor.close()

	def add(self, report_id, report: Report):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			INSERT INTO reports (report_id, reporter, reported, reason, date, teams, resolution)
			VALUES (?, ?, ?, ?, ?, ?, ?)
			ON CONFLICT(report_id) DO UPDATE SET
				reporter = excluded.reporter,
				reported = excluded.reported,
				reason = excluded.reason,
				date = excluded.date,
				teams = excluded.teams,
				resolution = excluded.resolution
		''', (report_id, *report.to_tuple()))
		conn.commit()
		cursor.close()

	def get(self, report_id) -> Report:
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			SELECT reporter, reported, reason, date, teams, resolution
			FROM reports WHERE report_id = ?
		''', (report_id,))
		row = cursor.fetchone()
		cursor.close()

		if row:
			report = Report(row[0], row[1], row[2], row[3], row[4])
			report.resolution = row[5]
			return report
		return None

	def remove(self, report_id):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('DELETE FROM reports WHERE report_id = ?', (report_id,))
		conn.commit()
		cursor.close()

	def clear(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('DELETE FROM reports')
		conn.commit()
		cursor.close()

	def list_all(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
			SELECT report_id, reporter, reported, reason, date, teams, resolution
			FROM reports
		''')
		rows = cursor.fetchall()
		cursor.close()

		reports = []
		for row in rows:
			reports.append(row[0])

		return reports
