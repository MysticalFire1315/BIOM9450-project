from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import config_by_name
from flask.app import Flask

from .util.logging import setup_logging

flask_bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    setup_logging()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config_by_name[config_name])
    flask_bcrypt.init_app(app)

    return app
