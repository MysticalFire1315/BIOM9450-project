from app.main.model.oncologist import Oncologist
from app.main.model.person import Person


def get_all_oncologists():
    return [Person.get_by_id(x.people_id) for x in Oncologist.get_all()]


def get_profile(id: int):
    x = Oncologist.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x
