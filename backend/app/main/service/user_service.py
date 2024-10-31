from typing import Dict, Tuple

from app.main.model.user import User
from app.main.model.person import Person

def link_user(user: User, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # Check person_id exists
    try:
        person = Person.get_by_id(data.get("person_id"))
    except Person.NotFoundError:
        return {"status": "fail", "message": "Invalid person id"}, 400

    try:
        user.person_id = person.id
        return {"status": "success", "message": "Successfully linked"}, 200
    except AttributeError:
        return {"status": "fail", "message": "User already linked"}, 400