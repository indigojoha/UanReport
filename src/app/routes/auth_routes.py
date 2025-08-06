from datetime import date, datetime
from flask import Blueprint, request, jsonify
from app.services import USERS, PHANDLER

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/try_login', methods=['POST'])
def try_login():
	data = request.get_json()
	userid = data.get('userid')
	user = USERS.get_user(userid)
	if user and len(user) == 2:
		return jsonify({'name': user[0], 'rights': user[1]}), 200
	return jsonify({'name': None, 'rights': -1}), 404

@auth_bp.route('/player_connection_permission', methods=['GET'])
def player_connection_permission():
	steamID = request.args.get('steamid')

	suspension = PHANDLER.get_suspension(steamID)
	if suspension:
		if suspension['days'] == 0:
			return jsonify({'result': 'banned', 'extra': {'reason': suspension['reason'], 'date': suspension['date']}}), 200
		else:
			suspended_date = datetime.fromisoformat(suspension['date']).date()
			days_passed = (date.today() - suspended_date).days
			if days_passed < suspension['days']:
				return jsonify({'result': 'suspended', 'extra': {'days_remaining': suspension['days'] - days_passed, 'reason': suspension['reason'], 'date': suspension['date']}}), 200
			else:
				PHANDLER.lift_suspension(steamID)
				return jsonify({'result': 'lifted', 'extra': None}), 200

	warning = PHANDLER.get_warning(steamID)
	if warning:
		result = jsonify({'result': 'warned', 'extra': {'reason': warning['reason'], 'date': warning['date']}})
		PHANDLER.lift_warning(steamID)
		return result, 200

	return jsonify({'result': 'permitted', 'extra': None}), 200
