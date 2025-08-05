from .auth_routes import auth_bp
from .report_routes import report_bp
from .action_routes import action_bp
from flask import send_from_directory
import os

def register_routes(app):
	app.register_blueprint(auth_bp)
	app.register_blueprint(report_bp)
	app.register_blueprint(action_bp)

	@app.route('/')
	def index():
		return send_from_directory(os.path.join(app.root_path, '../static'), 'index.html')
