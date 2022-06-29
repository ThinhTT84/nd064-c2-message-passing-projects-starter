from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api

from app.udaconnect.personservice import PersonService
from app.udaconnect.services import LocationService, ConnectionService


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    config = config_by_name[env or "test"]
    app.config.from_object(config)
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)

    @app.before_request
    def before_request():
        g.personService = PersonService()
        g.locationService = LocationService()
        g.connectionService = ConnectionService()
        g.personService.init_config(config)
        g.locationService.init_config(config)
        g.connectionService.init_config(config)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
