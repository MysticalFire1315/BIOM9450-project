from typing import Dict, Tuple

from app.main.model.oncologist import Oncologist
from app.main.model.patient import Patient
from app.main.model.person import Person
from app.main.model.researcher import Researcher


def create_person() -> Tuple[Dict[str, str], int]:
    return {"status": "fail", "message": "not implemented"}, 501


def get_person_role(person: Person):
    role_classes = {
        "patient": Patient,
        "oncologist": Oncologist,
        "researcher": Researcher,
    }

    for r, c in role_classes.items():
        try:
            c.get_by_people_id(person.id)
            return r
        except Exception:
            # Person doesn't have this role. Do nothing
            pass

    return "none"
