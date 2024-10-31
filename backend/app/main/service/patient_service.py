from typing import Dict, Tuple
from app.main.model.patient import Patient
from app.main.model.person import Person

def create_patient(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    # First check if person_id is present - if not, create new person
    person_id = data.get("person_id")
    if not person_id:
        person = Person.new_person()

    patient = Patient.new_patient(
        data.get()
    )

    return {
        "status": "success",
        "message": "Successfully created"
    }, 201