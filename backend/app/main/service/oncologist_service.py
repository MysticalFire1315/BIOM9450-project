from app.main.model.person import Person
from app.main.model.oncologist import Oncologist

def get_all_oncologists():
    return Oncologist.get_all()

def get_profile(id: int):
    x = Oncologist.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x