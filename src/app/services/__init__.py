from app.server.Users import Users
from app.server.PlayerHandler import PlayerHandler
from app.server.ReportRegistry import ReportRegistry

_PREFIX = '/mnt/data/BigBugBrawl'
# _PREFIX = 'data/BigBugBrawl'

USERS = Users(f'{_PREFIX}/users.db')
PHANDLER = PlayerHandler(f'{_PREFIX}/players.db')
REPORTS = ReportRegistry(f'{_PREFIX}/reports.db')
RESOLVED = ReportRegistry(f'{_PREFIX}/resolved_reports.db')

def init_services():
	pass
