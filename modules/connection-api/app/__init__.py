from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.udaconnect.personservice import PersonService

db = SQLAlchemy()
personService = PersonService()

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    config = config_by_name[env or 'development']
    app.config.from_object(config)
    api = Api(app, title="UdaConnect Connection API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    personService.init_config(config)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
