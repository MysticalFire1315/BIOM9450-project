from typing import Dict, Tuple

from app.main.model.user import User
from app.main.model.person import Person
from app.main.service.person_service import get_person_role

def check_link(user: User) -> Tuple[Dict[str, str], int]:
    return {"status": "success", "message": user.people_id is not None}, 200

def link_user(user: User, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # Check person_id exists
    person = Person.get_by_id(data.get("person_id"))
    user.people_id = person.id
    return {"status": "success", "message": "Successfully linked", "role": get_person_role(person)}, 200
