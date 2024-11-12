from typing import Dict, Tuple, List

from app.main.model.user import User
from app.main.model.person import Person
from app.main.service.person_service import get_person_role
from app.main.util.exceptions.errors import NotFoundError
from app.main.util.database import db_get_cursor

def check_link(user: User) -> Tuple[Dict[str, str], int]:
    return {"status": "success", "message": user.people_id is not None}, 200

def link_user(user: User, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # Check person_id exists
    person = Person.get_by_id(data.get("person_id"))
    user.people_id = person.id
    return {"status": "success", "message": "Successfully linked", "role": get_person_role(person)}, 200

def get_user(user: User) -> User:
    try:
        user.role = get_person_role(Person.get_by_id(user.people_id))
    except NotFoundError:
        user.role = "none"
    return user

def user_history(user: User, num: int) -> List[Dict[str, str]]:
    try:
        with db_get_cursor() as cur:
            cur.execute("""
                SELECT time_accessed, method, url_path, status_code FROM request_logs
                WHERE user_id = %s
                ORDER BY time_accessed DESC;
            """, (user.id,))
            result = cur.fetchall()[:num]
    except Exception as e:
        raise e

    return [{"time_accessed": time_accessed, "method": method, "path": url_path, "response": status} for time_accessed, method, url_path, status in result]
