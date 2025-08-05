from flask import Blueprint, request, jsonify
from app.services import REPORTS, SOLVED
from app.utils.helpers import verify_user
from app.server.ReportRegistry import Report
import hashlib
from datetime import datetime

report_bp = Blueprint('report', __name__, url_prefix='/api')

@report_bp.route('/submit_report', methods=['POST'])
def submit_report():
	data = request.get_json()
	reporter = data.get('reporter')
	reported = data.get('reported')
	reason = data.get('reason')
	date = data.get('date')
	teams = data.get('teams')

	if reporter and reported and reason and date and teams:
		report_id = hashlib.sha256(
			f"{reporter}{reported}{reason}{date}{teams}{datetime.now().isoformat()}".encode()
		).hexdigest()

		report = Report(reporter, reported, reason, date, teams)
		REPORTS.add(report_id, report)
		REPORTS.save_json()
		return jsonify({'report_id': report_id}), 201

	return jsonify({'error': 'Invalid report data'}), 400

@report_bp.route('/get_report_list', methods=['GET'])
def get_report_list():
	if not verify_user(request.args.get('userid')):
		return jsonify({'error': 'Invalid user ID'}), 403

	resolved = request.args.get('resolved', 'false').lower() == 'true'
	report_store = SOLVED if resolved else REPORTS
	return jsonify(list(report_store.reports.keys())), 200

@report_bp.route('/get_report', methods=['GET'])
def get_report():
	if not verify_user(request.args.get('userid')):
		return jsonify({'error': 'Invalid user ID'}), 403

	report_id = request.args.get('reportid')
	resolved = request.args.get('resolved', 'false').lower() == 'true'
	report_store = SOLVED if resolved else REPORTS

	if report_id:
		report = report_store.get(report_id)
		if report:
			return jsonify(report.to_dict()), 200

	return jsonify({'error': 'Report not found'}), 404
