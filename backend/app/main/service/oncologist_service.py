from app.main.model.person import Person
from app.main.model.oncologist import Oncologist

def get_profile(person: Person):
    o = Oncologist.get_by_people_id(person.id)
    o.person = person
    return o
