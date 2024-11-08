from typing import Dict, Tuple
from app.main.model.patient import Patient
from app.main.model.person import Person, Sex
from app.main.util.exceptions.errors import CustomError

def create_patient(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    person_data = data.get("person")
    person = Person.new_person(
        person_data.get("firstname"),
        person_data.get("lastname"),
        person_data.get("date_of_birth"),
        Sex.from_str(person_data.get("sex"))
    )

    try:
        p = Patient.new_patient(
            person.id,
            data.get("photo"),
            data.get("address"),
            data.get("country"),
            data.get("emergency_contact_name"),
            data.get("emergency_contact_phone")
        )
        return {"status": "success", "message": "Successfully created", "id": p.people_id}, 201
    except CustomError as error:
        person.delete()
        raise error

def get_profile(id: int):
    x = Patient.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x

def get_all_patients():
    return Patient.get_all()