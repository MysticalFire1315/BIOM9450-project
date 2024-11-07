from typing import Dict, Tuple

from app.main.model.user import User
from app.main.model.person import Person

def link_user(user: User, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # Check person_id exists
    person = Person.get_by_id(data.get("person_id"))
    user.people_id = person.id
    return {"status": "success", "message": "Successfully linked"}, 200
