from typing import Dict, Tuple

from app.main.model.oncologist import Oncologist
from app.main.model.patient import Patient
from app.main.model.person import Person
from app.main.model.researcher import Researcher


def create_person() -> Tuple[Dict[str, str], int]:
    """Creates a new person entry in the database.

    Returns:
        Tuple[Dict[str, str], int]: A tuple containing a response message and a status code.
    """

    return {"status": "fail", "message": "not implemented"}, 501


def get_person_role(person: Person) -> str:
    """Retrieves the role of a person.

    Args:
        person (Person): The Person object to retrieve the role for.

    Returns:
        str: The role of the person. Possible values are "patient", "oncologist", "researcher", or "none".
    """

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
