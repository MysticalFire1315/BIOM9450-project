from app.main.model.person import Person
from app.main.model.researcher import Researcher

def get_profile(person: Person):
    r = Researcher.get_by_people_id(person.id)
    r.person = person
    return r
