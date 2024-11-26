from typing import Dict, Tuple

from app.main.model.person import Person
from app.main.model.user import User
from app.main.util.database import db_get_cursor


def register_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Registers a new user.

    Args:
        data (Dict[str, str]): A dictionary containing user registration data.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a response message and a status code.
    """

    user = User.new_user(data.get("email"), data.get("username"), data.get("password"))

    return {
        "status": "success",
        "message": "Successfully registered.",
        "Authorization": user.encode_auth_token().decode(),
    }, 201


def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Logs in a user.

    Args:
        data (Dict[str, str]): A dictionary containing user login data.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a response message and a status code.
    """

    user = User.get_by_login(data.get("email"), data.get("password"))

    return {
        "status": "success",
        "message": "Successfully logged in.",
        "Authorization": user.encode_auth_token().decode(),
    }, 200


def logout_user(token: str) -> Tuple[Dict[str, str], int]:
    """Logs out a user by blacklisting their token.

    Args:
        token (str): The authentication token to blacklist.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a response message and a status code.
    """

    # Check token can be used to login
    get_logged_in_user(token)
    with db_get_cursor() as cur:
        cur.execute("INSERT INTO blacklist_tokens (token) VALUES (%s)", (token,))
    return {"status": "success", "message": "Successfully logged out"}, 200


def get_logged_in_user(token: str) -> User:
    """Retrieves the logged-in user from the token.

    Args:
        token (str): The authentication token.

    Returns:
        User: The user associated with the authentication token.
    """

    return User.decode_auth_token(token)


def get_logged_in_person(token: str) -> Person:
    """Retrieves the logged-in person from the token.

    Args:
        token (str): The authentication token.

    Returns:
        Person: The person associated with the authentication token.
    """

    resp = get_logged_in_user(token)
    return Person.get_by_id(resp.people_id)
