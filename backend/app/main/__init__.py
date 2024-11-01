from flask import Flask, request, make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import config_by_name
from flask.app import Flask

from .util.logging import setup_logging

flask_bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    setup_logging()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://192.168.209.129:8080"]}}, supports_credentials=True)
    app.config.from_object(config_by_name[config_name])
    flask_bcrypt.init_app(app)


    # Global before_request handler to handle all OPTIONS requests
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            origin = request.headers.get('Origin')
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = origin if origin in ["http://localhost:8080", "http://192.168.209.129:8080"] else None
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response

    return app
