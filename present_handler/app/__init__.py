from flask import Flask
from flask_cors import CORS
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    CORS(app)

    from .services.present_handler import p_handler as p_handler_blueprint
    app.register_blueprint(p_handler_blueprint)

    return app

