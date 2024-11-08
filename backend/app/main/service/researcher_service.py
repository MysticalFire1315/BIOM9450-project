from app.main.model.person import Person
from app.main.model.researcher import Researcher

def get_profile(id: int):
    x = Researcher.get_by_people_id(id)
    x.person = Person.get_by_id(id)
    return x

def get_all_researchers():
    return Researcher.get_all()