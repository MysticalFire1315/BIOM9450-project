from app.main.model.user import User
from app.main.model.person import Person
from app.main.util.database import db_get_cursor
from typing import Dict, Tuple


def register_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.new_user(
        data.get("email"), data.get("username"), data.get("password")
    )

    return {
        "status": "success",
        "message": "Successfully registered.",
        "Authorization": user.encode_auth_token().decode(),
    }, 201


def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.get_by_login(data.get("email"), data.get("password"))

    return {
        "status": "success",
        "message": "Successfully logged in.",
        "Authorization": user.encode_auth_token(),
    }, 200


def logout_user(token: str) -> Tuple[Dict[str, str], int]:
    # Check token can be used to login
    get_logged_in_user(token)
    with db_get_cursor() as cur:
        cur.execute("INSERT INTO blacklist_tokens (token) VALUES (%s)", (token,))
    return {"status": "success", "message": "Successfully logged out"}, 200


def get_logged_in_user(token: str) -> User:
    print(token)
    return User.decode_auth_token(token)


def get_logged_in_person(token: str) -> Person:
    resp = get_logged_in_user(token)
    return Person.get_by_id(resp.people_id)
