import os
import json

class Report:
	def __init__(self, reporter, reported, reason, date, teams):
		self.reporter = reporter
		self.reported = reported
		self.reason = reason
		self.date = date
		self.teams = teams
		self.resolution = ''
	
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
	def __init__(self):
		self.JSON_PATH = ''
		self.reports = {}

	def add(self, report_id, report):
		self.reports[report_id] = report

	def get(self, report_id) -> Report:
		return self.reports.get(report_id)

	def remove(self, report_id):
		if report_id in self.reports:
			del self.reports[report_id]

	def load_json(self):
		try:
			with open(self.JSON_PATH, 'r', encoding='utf-8') as file:
				data = json.load(file)
				for report_id, report_data in data.items():
					report = Report(
						report_data['reporter'],
						report_data['reported'],
						report_data['reason'],
						report_data['date'],
						report_data['teams'],
					)
					report.resolution = report_data.get('resolution', '')
					self.add(report_id, report)
				file.close()
		except FileNotFoundError:
			print(f"File {self.JSON_PATH} not found. Using empty report registry.")
			self.reports = {}

	def save_json(self):
		data = {report_id: report.to_dict() for report_id, report in self.reports.items()}

		with open(self.JSON_PATH, 'w', encoding='utf-8') as file:
			json.dump(data, file, indent=4)
			file.flush()
			os.fsync(file.fileno())
			file.close()
