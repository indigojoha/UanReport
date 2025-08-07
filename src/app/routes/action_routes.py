from flask import Blueprint, request, jsonify
from app.services import USERS, REPORTS, RESOLVED, PHANDLER
from app.utils.helpers import verify_user
from app.server.ReportRegistry import Report
import re

action_bp = Blueprint('action', __name__, url_prefix='/api')

# format: name (id)
def parse_name(name: str):
	match = re.match(r'^(.*)\s+\((\d+)\)$', name)
	if match:
		text, number = match.groups()
		return text.strip(), int(number.strip())
	return name, None

@action_bp.route('/take_action', methods=['POST'])
def take_action():
	if not verify_user(request.args.get('userid')):
		return jsonify({'error': 'Invalid user ID'}), 403

	data = request.get_json()
	reportID = data.get('reportid')
	action = data.get('action') # 0 = pass, 1 = warn, 2 = suspend, 3 = ban 
	extra = data.get('extra', None)

	if not (reportID and action is not None):
		return jsonify({'error': 'Missing report ID or action'}), 400

	report: Report = REPORTS.get(reportID)
	if not report:
		return jsonify({'error': 'Report not found'}), 404

	required_rights = {
		0: 1, # pass 
		1: 1, # warn 
		2: 2, # suspend 
		3: 3, # ban 
	}

	if action not in required_rights:
		return jsonify({'error': 'Invalid action code "' + str(action) + '"'}), 400

	if USERS.get_user_rights(request.args.get('userid')) < required_rights[action]:
		return jsonify({'error': 'Insufficient rights for this action'}), 403

	if action == 0: # pass 
		report.resolution = 'pass'

	elif action == 1: # warn 
		report.resolution = 'warn'

	elif action == 2: # suspend 
		if not extra or 'days' not in extra:
			return jsonify({'error': 'Missing suspension duration'}), 400
		handle, steamid = parse_name(report.reported)
		if steamid is None:
			return jsonify({'error': 'Invalid reported player ID. "' + report.reported + '", "' + handle + '" #' + str(steamid)}), 400

		PHANDLER.suspend_player(steamid, extra['days'], report.reason)
		report.resolution = 'suspend'
		report.days = extra['days']

	elif action == 3: # ban 
		handle, steamid = parse_name(report.reported)
		if steamid is None:
			return jsonify({'error': 'Invalid reported player ID. "' + report.reported + '", "' + handle + '" #' + str(steamid)}), 400

		PHANDLER.suspend_player(steamid, 0, report.reason)
		report.resolution = 'ban'

	RESOLVED.add(reportID, report)
	REPORTS.remove(reportID)

	return '', 204
