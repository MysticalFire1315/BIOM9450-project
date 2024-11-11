from flask import Flask, request, make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import config_by_name, key
from flask.app import Flask

from .util.logging import setup_logging
from .util.database import db_get_cursor
import jwt
import logging
import textwrap

flask_bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    setup_logging(config_name)
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

    # Log all requests to database
    @app.after_request
    def log_request(response):
        try:
            token = request.headers.get("Authorization")
            payload = jwt.decode(token, key)["sub"]
        except Exception:
            payload = None

        details = {
            "method": request.method,
            "url_path": request.path,
            "remote_addr": request.remote_addr,
            "agent": request.user_agent.string,
            "status": response.status_code,
            "user_id": payload,
        }

        l = logging.getLogger(__name__)
        l.warn(request.path)

        with db_get_cursor() as cur:
            cur.execute("SELECT * FROM blacklist_tokens WHERE token = %s;", (token,))
            details["user_id"] = None if cur.fetchone() is not None else details["user_id"]
            if payload:
                cur.execute("SELECT * FROM users WHERE id = %s;", (payload,))
                details["user_id"] = None if cur.fetchone() is None else details["user_id"]
            cur.execute("""
                INSERT INTO request_logs (method, url_path, remote_addr, agent, status_code, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, tuple(details.values()))

        logger = logging.getLogger("requests")
        logger.info(textwrap.dedent("""
                Request:        {} {}
                IP:             {}
                User ID:        {}
                Raw Agent:      {}
                Response Code:  {}
            """.format(
                details["method"],
                details["url_path"],
                details["remote_addr"],
                details["user_id"],
                details["agent"],
                details["status"]
            )
        ))
        return response

    return app
