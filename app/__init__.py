from flask import Flask
from .routes import register_routes
from .services import init_services

def create_app():
	app = Flask(__name__, static_folder='../static', static_url_path='')

	init_services()
	register_routes(app)

	return app
