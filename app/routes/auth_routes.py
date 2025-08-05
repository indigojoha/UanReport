from flask import Blueprint, request, jsonify
from app.services import USERS

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/try_login', methods=['POST'])
def try_login():
	data = request.get_json()
	userid = data.get('userid')
	user = USERS.get_user(userid)
	if user and len(user) == 2:
		return jsonify({'name': user[0], 'rights': user[1]}), 200
	return jsonify({'name': None, 'rights': -1}), 404
