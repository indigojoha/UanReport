from datetime import date, datetime
from flask import Blueprint, request, jsonify, make_response
from app.services import USERS, PHANDLER
import json

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

	def make_json_response(payload: dict):
		resp = make_response(json.dumps(payload))
		resp.headers['Content-Type'] = 'application/json'
		resp.headers['Content-Length'] = str(len(resp.get_data()))
		return resp

	suspension = PHANDLER.get_suspension(steamID)
	if suspension:
		if suspension['days'] == 0:
			return make_json_response({'result': 'banned', 'extra': {'reason': suspension['reason'], 'date': suspension['date']}})
		else:
			suspended_date = datetime.fromisoformat(suspension['date']).date()
			days_passed = (date.today() - suspended_date).days
			if days_passed < suspension['days']:
				return make_json_response({'result': 'suspended', 'extra': {'days_remaining': suspension['days'] - days_passed, 'reason': suspension['reason'], 'date': suspension['date']}})
			else:
				PHANDLER.lift_suspension(steamID)
				return make_json_response({'result': 'lifted', 'extra': None})

	warning = PHANDLER.get_warning(steamID)
	if warning:
		result = make_json_response({'result': 'warned', 'extra': {'reason': warning['reason'], 'date': warning['date']}})
		PHANDLER.lift_warning(steamID)
		return result, 200

	return make_json_response({'result': 'permitted', 'extra': None})
