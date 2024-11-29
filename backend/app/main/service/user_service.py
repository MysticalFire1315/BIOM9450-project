from typing import Dict, List, Tuple

from app.main.model.person import Person
from app.main.model.user import User
from app.main.service.person_service import get_person_role
from app.main.util.database import db_get_cursor
from app.main.util.exceptions.errors import NotFoundError


def check_link(user: User) -> Tuple[Dict[str, str], int]:
    """Checks if the user is linked to a person.

    Args:
        user (User): The User object to check the link for.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing the status and a message.
    """

    return {"status": "success", "message": user.people_id is not None}, 200


def link_user(user: User, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """Links a user to a person.

    Args:
        user (User): The User object to link.
        data (Dict[str, str]): A dictionary containing the person ID to link to the user.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing the status, a message, and the role of the linked person.
    """

    # Check person_id exists
    person = Person.get_by_id(data.get("person_id"))
    user.people_id = person.id
    return {
        "status": "success",
        "message": "Successfully linked",
        "role": get_person_role(person),
    }, 201


def get_user(user: User) -> User:
    """Retrieves the user with their role.

    Args:
        user (User): The User object to retrieve the role for.

    Returns:
        User: The User object with the associated role.
    """

    try:
        user.role = get_person_role(Person.get_by_id(user.people_id))
    except NotFoundError:
        user.role = "none"
    return user


def user_history(user: User, num: int) -> List[Dict[str, str]]:
    """Retrieves the user's request history.

    Args:
        user (User): The User object to retrieve the history for.
        num (int): The number of recent requests to retrieve.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing request log details.
    """

    try:
        with db_get_cursor() as cur:
            cur.execute(
                """
                SELECT time_accessed, method, url_path, status_code FROM request_logs
                WHERE user_id = %s
                ORDER BY time_accessed DESC;
                """,
                (user.id,),
            )
            result = cur.fetchall()[:num]
    except Exception as e:
        raise e

    return [
        {
            "time_accessed": time_accessed,
            "method": method,
            "path": url_path,
            "response": status,
        }
        for time_accessed, method, url_path, status in result
    ]
