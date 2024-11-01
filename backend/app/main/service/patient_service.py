from typing import Dict, Tuple
from app.main.model.patient import Patient
from app.main.model.person import Person, Role, Sex

def create_patient(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # First check if person_id is present - if not, create new person
    person_id = data.get("person_id")
    if not person_id:
        person_data = data.get("person")
        person = Person.new_person(
            person_data.get("firstname"),
            person_data.get("lastname"),
            person_data.get("date_of_birth"),
            Sex.from_str(person_data.get("sex")),
            Role.PATIENT
        )

    try:
        Patient.new_patient(
            person_id or person.id,
            data.get("photo"),
            data.get("address"),
            data.get("country"),
            data.get("emergency_contact_name"),
            data.get("emergency_contact_phone")
        )
    except error:
        person.delete()
        raise error

    return {"status": "success", "message": "Successfully created"}, 201
