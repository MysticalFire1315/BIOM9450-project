from app.main.model.user import User
from app.main.model.person import Person
from app.main.util.database import db_get_cursor
from typing import Dict, Tuple, Union
from flask import current_app
import traceback


def register_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    try:
        user = User.new_user(
            data.get("email"), data.get("username"), data.get("password")
        )

        return {
            "status": "success",
            "message": "Successfully registered.",
            "Authorization": user.encode_auth_token().decode(),
        }, 201
    except User.AlreadyExistsError:
        return {"status": "fail", "message": "User already exists. Please log in"}, 409
    except User.BadInputError:
        return {"status": "fail", "message": "Invalid arguments. Try again"}, 400


def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    try:
        user = User.get_by_login(data.get("email"), data.get("password"))

        return {
            "status": "success",
            "message": "Successfully logged in.",
            "Authorization": user.encode_auth_token().decode(),
        }, 200
    except User.NotFoundError:
        return {
            "status": "fail",
            "message": "email or password does not match",
        }, 401


def logout_user(token: str) -> Tuple[Dict[str, str], int]:
    resp = get_logged_in_user(token)
    if type(resp) is tuple:
        return resp

    with db_get_cursor() as cur:
        cur.execute("INSERT INTO blacklist_tokens (token) VALUES (%s)", (token,))
    return {"status": "success", "message": "Successfully logged out"}, 200


def get_logged_in_user(token: str) -> Union[User, Tuple[Dict[str, str], int]]:
    try:
        return User.decode_auth_token(token)
    except (User.TokenExpiredError, User.TokenBlacklistedError):
        message = "Token expired"
    except (User.TokenInvalidError, User.NotFoundError):
        message = "Token invalid"
    except Exception:
        current_app.logger.error(traceback.format_exc())
        message = "Provide a valid auth token"
    return {"status": "fail", "message": message}, 401


def get_logged_in_person(token: str) -> Union[Person, Tuple[Dict[str, str], int]]:
    resp = get_logged_in_user(token)
    if type(resp) is tuple:
        return resp
    try:
        return Person.get_by_id(resp.person_id)
    except Person.NotFoundError:
        return {"status": "fail", "message": "User not linked"}, 403
