from app.server.Users import Users
from app.server.PlayerHandler import PlayerHandler
from app.server.ReportRegistry import ReportRegistry

USERS = Users()
PHANDLER = PlayerHandler()
REPORTS = ReportRegistry()
SOLVED = ReportRegistry()

def init_services():
	USERS.JSON_PATH = 'data/BigBugBrawl/users.json'
	USERS.load_json()
	USERS.save_json()

	PHANDLER.JSON_PATH = 'data/BigBugBrawl/suspensions.json'
	PHANDLER.load_json()
	PHANDLER.save_json()

	REPORTS.JSON_PATH = 'data/BigBugBrawl/reports.json'
	REPORTS.load_json()
	REPORTS.save_json()

	SOLVED.JSON_PATH = 'data/BigBugBrawl/solved_reports.json'
	SOLVED.load_json()
	SOLVED.save_json()
