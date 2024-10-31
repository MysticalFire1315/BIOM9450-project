from typing import Dict, Tuple

from app.main.service.auth_service import login_user, logout_user, register_user
from app.main.util.dto import AuthDto
from flask import request
from flask_restx import Resource

api = AuthDto.api

@api.errorhandler(User.AlreadyExistsError)

@api.route("/register")
class RegisterAPI(Resource):
    @api.doc("register a user")
    @api.expect(AuthDto.user_register, validate=True)
    @api.response(201, 'User successfully created.')
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return register_user(post_data)


@api.route("/login")
class LoginAPI(Resource):
    @api.doc("login a user")
    @api.expect(AuthDto.user_login, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return login_user(post_data)


@api.route("/logout")
class LogoutAPI(Resource):
    @api.doc("logout a user")
    def post(self) -> Tuple[Dict[str, str], int]:
        auth_header = request.headers.get("Authorization")
        return logout_user(auth_header)
